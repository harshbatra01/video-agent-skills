"""AI roto: track a player through a clip with SAM 2 and write a clean matte (free, local GPU).

usage: python roto.py CLIP OUT_MATTE.mp4 [--in SEC --out SEC] [--box x0,y0,x1,y1 | --point x,y] [--pick largest|center]
                      [--width W (default: source width)] [--preview OUT_PREVIEW.mp4]
as a module: make_matte(clip, out, t0, t1, box=[x0,y0,x1,y1] | point=[x,y], stats=True) -> dict with per-frame shape stats
  (the SAM 2 model is loaded once per process and reused)
- With no prompt it runs a person detector on the first frame and takes the largest (or most central) person.
- The SAM 2 mask is refined with a guided filter against the real frame, so edges follow hair, shirt and boots,
  then lightly smoothed over time to stop edge flicker.
- Output: grey matte video (white = player), same frame rate and range as the source section, for a Luma Matte
  in After Effects or Track Matte Key in Premiere. --preview writes the player over grey for a quick check.
Run without -I (torch, sam2, torchvision live in the user site-packages).
"""
import sys, os, subprocess, tempfile, shutil
import numpy as np
import av, torch
import torch.nn.functional as Fn
from PIL import Image

KIT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CKPT = os.path.join(KIT, "models", "sam2.1_hiera_large.pt")
CFG = "configs/sam2.1/sam2.1_hiera_l.yaml"

def arg(name, default=None, cast=str):
    a = sys.argv
    return cast(a[a.index(name) + 1]) if name in a else default

def read_frames(path, t0, t1, width):
    c = av.open(path); s = c.streams.video[0]; s.thread_type = "AUTO"; fps = float(s.average_rate)
    if t0 > 0: c.seek(int(max(0, t0 - 1) / s.time_base), stream=s)
    frames, times = [], []
    for fr in c.decode(s):
        t = float(fr.pts * s.time_base)
        if t < t0 - 0.5 / fps: continue
        if t1 is not None and t >= t1 - 0.5 / fps: break
        w = width or fr.width; h = int(round(fr.height * w / fr.width / 2) * 2)
        frames.append(fr.reformat(width=w, height=h, format="rgb24").to_ndarray()); times.append(t)
    c.close()
    read_frames.times = times
    return fps, frames

def detect_person(img, pick="largest"):
    import torchvision
    from torchvision.models.detection import fasterrcnn_resnet50_fpn_v2, FasterRCNN_ResNet50_FPN_V2_Weights
    w = FasterRCNN_ResNet50_FPN_V2_Weights.DEFAULT
    m = fasterrcnn_resnet50_fpn_v2(weights=w).eval().cuda()
    x = torch.from_numpy(img).permute(2, 0, 1).float().div(255).cuda()
    with torch.no_grad():
        r = m([x])[0]
    keep = [(b.tolist(), float(s)) for b, l, s in zip(r["boxes"], r["labels"], r["scores"]) if int(l) == 1 and float(s) > 0.6]
    if not keep: return None, []
    H, W = img.shape[:2]
    if pick == "center":
        best = min(keep, key=lambda bs: abs((bs[0][0] + bs[0][2]) / 2 - W / 2) + abs((bs[0][1] + bs[0][3]) / 2 - H / 2) - 0.5 * (bs[0][3] - bs[0][1]))
    else:
        best = max(keep, key=lambda bs: (bs[0][2] - bs[0][0]) * (bs[0][3] - bs[0][1]))
    return best[0], keep

def box_mean(x, r):
    k = 2 * r + 1
    return Fn.avg_pool2d(Fn.pad(x, (r, r, r, r), mode="replicate"), k, stride=1)

def guided(I, p, r=8, eps=1e-3):
    """fast guided filter on GPU. I: (1,3,H,W) guide 0-1, p: (1,1,H,W) mask 0-1"""
    out = []
    for c in range(3):
        Ic = I[:, c:c + 1]
        mI, mp = box_mean(Ic, r), box_mean(p, r)
        cov = box_mean(Ic * p, r) - mI * mp; var = box_mean(Ic * Ic, r) - mI * mI
        a = cov / (var + eps); b = mp - a * mI
        out.append(box_mean(a, r) * Ic + box_mean(b, r))
    return torch.stack(out, 0).mean(0).clamp(0, 1)

def main():
    clip, outp = sys.argv[1], sys.argv[2]
    box = arg("--box"); point = arg("--point")
    if box: box = [float(v) for v in box.split(",")]
    print(make_matte(clip, outp, arg("--in", 0.0, float), arg("--out", None, float), box=box, point=point,
                     pick=arg("--pick", "largest"), width=arg("--width", None, int), preview=arg("--preview")))

_PRED = {}
def predictor():
    if not _PRED:
        from sam2.build_sam import build_sam2_video_predictor
        _PRED["p"] = build_sam2_video_predictor(CFG, CKPT, device="cuda")
    return _PRED["p"]

def make_matte(clip, outp, t0=0.0, t1=None, box=None, point=None, pick="largest", width=None, preview=None, stats=False, prompt_t=None):
    """SAM 2 matte for clip[t0:t1] -> outp (grey video, same size as the source unless width is given).
    box / point in SOURCE pixels. Returns a summary line, or with stats=True a dict: src0 (source time of matte frame 0),
    fps, size and per-frame [src t, area, cx, cy, x0, y0, x1, y1, ux, uy] in source pixels (u = centre of the upper 45%
    of the shape: head + shoulders, steadier than the full centroid when legs and arms swing)."""
    fps, frames = read_frames(clip, t0, t1, width); ftimes = read_frames.times
    pf = 0 if prompt_t is None else int(np.argmin([abs(t - prompt_t) for t in ftimes]))   # prompt where he is clearest
    if not frames: raise SystemExit("no frames in range")
    H, W = frames[0].shape[:2]
    src_w = av.open(clip).streams.video[0].codec_context.width; k = W / src_w
    if box is not None:
        box = [v * k for v in box]
    elif point is not None:
        if isinstance(point, str): point = [float(v) for v in point.split(",")]
        point = [v * k for v in point]
    else:
        box, cands = detect_person(frames[pf], pick)
        if box is None: raise SystemExit("no person found on the first frame: pass --box or --point")
    tmp = tempfile.mkdtemp(prefix="sam2_")
    try:
        for i, f in enumerate(frames):
            Image.fromarray(f).save(os.path.join(tmp, f"{i:05d}.jpg"), quality=95)
        pred = predictor()
        probs = [None] * len(frames)
        with torch.inference_mode(), torch.autocast("cuda", dtype=torch.bfloat16):
            st = pred.init_state(video_path=tmp, offload_video_to_cpu=True)
            if box:
                pred.add_new_points_or_box(st, frame_idx=pf, obj_id=1, box=np.array(box, np.float32))
            else:
                pred.add_new_points_or_box(st, frame_idx=pf, obj_id=1, points=np.array([point], np.float32), labels=np.array([1], np.int32))
            for fi, ids, logits in pred.propagate_in_video(st, start_frame_idx=pf):
                probs[fi] = torch.sigmoid(logits[0, 0].float())
            if pf > 0:                                   # and backwards to the start of the range
                for fi, ids, logits in pred.propagate_in_video(st, start_frame_idx=pf, reverse=True):
                    probs[fi] = torch.sigmoid(logits[0, 0].float())
            pred.reset_state(st)
        # refine + temporal smooth + write
        enc = ["-c:v", "h264_nvenc", "-preset", "p6", "-cq", "12"]
        cmd = ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "gray", "-s", f"{W}x{H}", "-r", f"{fps}", "-i", "-"] + enc + ["-pix_fmt", "yuv420p", outp]
        p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
        prv = None
        if preview:
            pcmd = ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", f"{fps}", "-i", "-"] + enc + ["-pix_fmt", "yuv420p", preview]
            prv = subprocess.Popen(pcmd, stdin=subprocess.PIPE)
        prev = None; areas = []; rows = []
        ys = torch.arange(H, device="cuda", dtype=torch.float32)[:, None]; xs = torch.arange(W, device="cuda", dtype=torch.float32)[None, :]
        for i, f in enumerate(frames):
            m = probs[i] if probs[i] is not None else torch.zeros((H, W), device="cuda")
            I = torch.from_numpy(f).permute(2, 0, 1)[None].float().cuda() / 255
            a = guided(I, m[None, None], r=max(4, W // 240), eps=2e-3)[0, 0]
            a = ((a - 0.15) / 0.7).clamp(0, 1)                       # firm up the core, keep soft edges
            if prev is not None: a = 0.75 * a + 0.25 * prev        # light temporal smoothing
            prev = a; areas.append(float(a.mean()))
            if stats:
                m_ = (a > 0.5).float(); n_ = float(m_.sum())
                if n_ < 30: rows.append([round(ftimes[i], 4), 0, 0, 0, 0, 0, 0, 0, 0, 0])
                else:
                    rr = torch.nonzero(m_.sum(1)).flatten(); cc_ = torch.nonzero(m_.sum(0)).flatten()
                    y0_, y1_, x0_, x1_ = float(rr[0]), float(rr[-1]), float(cc_[0]), float(cc_[-1])
                    up = m_[: int(y0_ + 0.45 * (y1_ - y0_)) + 1]; nu = float(up.sum()) or 1.0
                    vals = [float((m_ * xs).sum()) / n_, float((m_ * ys).sum()) / n_, x0_, y0_, x1_, y1_,
                            float((up * xs).sum()) / nu, float((up * ys[: up.shape[0]]).sum()) / nu]
                    rows.append([round(ftimes[i], 4), round(n_ / (H * W), 4)] + [round(v / k, 1) for v in vals])
            g = (a * 255).byte().cpu().numpy()
            p.stdin.write(g.tobytes())
            if prv:
                comp = (f.astype(np.float32) * (g[..., None] / 255) + 70 * (1 - g[..., None] / 255)).astype(np.uint8)
                prv.stdin.write(comp.tobytes())
        p.stdin.close(); p.wait()
        if prv: prv.stdin.close(); prv.wait()
        ar = np.array(areas)
        if stats:
            return dict(file=outp, src0=round(ftimes[0], 4), fps=fps, w=int(W / k), h=int(round(H / k)), rows=rows)
        return f"wrote {outp}: {len(frames)} frames {W}x{H} @ {fps:.2f}; matte area mean {ar.mean():.3f}, min {ar.min():.3f}, max {ar.max():.3f}"
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

if __name__ == "__main__":
    main()
