"""Frame grabbing via VLC (no ffmpeg on this machine)."""
import subprocess, os, glob, shutil, tempfile
VLC = os.environ.get('VLC_PATH') or next((p for p in (r'C:\Program Files\VideoLAN\VLC\vlc.exe', '/Applications/VLC.app/Contents/MacOS/VLC') if os.path.exists(p)), r'C:\Program Files\VideoLAN\VLC\vlc.exe')
SCRATCH = r"C:\Users\Kanishk\AppData\Local\Temp\claude\C--VISION-IMMUFIX-repair-ENCODED-RUSHES\b6d96195-2992-4138-a685-9dc3b5c5abcd\scratchpad\work"
def grab(video, t0, dur=0.0, every=1, outdir=None, prefix='f', fast=False):
    """Save frames from t0 to t0+dur (every Nth decoded frame). Returns sorted list of png paths."""
    outdir = outdir or tempfile.mkdtemp(dir=SCRATCH)
    os.makedirs(outdir, exist_ok=True)
    for f in glob.glob(os.path.join(outdir, prefix + '_*.png')): os.remove(f)
    t1 = t0 + max(dur, 0.04)
    slow = [] if fast else ['--no-drop-late-frames', '--no-skip-frames', '--rate=0.1']
    cmd = [VLC, '--intf', 'dummy', '--dummy-quiet', '--vout', 'dummy', '--no-audio', '--avcodec-hw=none', *slow,
           '--video-filter=scene', '--scene-format=png', f'--scene-ratio={every}', f'--scene-prefix={prefix}_',
           f'--scene-path={outdir}', f'--start-time={t0:.3f}', f'--stop-time={t1:.3f}', '--play-and-exit', video, 'vlc://quit']
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=300)
    return sorted(glob.glob(os.path.join(outdir, prefix + '_*.png')))
