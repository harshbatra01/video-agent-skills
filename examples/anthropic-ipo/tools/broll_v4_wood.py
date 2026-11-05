import numpy as np
rng = np.random.default_rng(11)


def wood2(w, h):
    "Soft plank grain: noise stretched along the wood, darker toward the edges."
    from PIL import Image as I
    def layer(cols, rows): return np.asarray(I.fromarray(((rng.normal(0, 1, (rows, cols)) + 3) * 42).clip(0, 255).astype(np.uint8)).resize((w, h), I.BICUBIC), np.float32) / 255
    v = .55 * layer(6, 26) + .3 * layer(14, 90) + .15 * layer(40, 320)
    a = np.stack([46 + v * 86, 30 + v * 58, 20 + v * 38], -1); y, x = np.mgrid[0:h, 0:w]; g = 1.08 - .7 * np.clip(np.hypot((x - w / 2) / (w / 2), (y - h / 2) / (h / 2)) / 1.414, 0, 1) ** 1.5
    return I.fromarray(np.clip(a * g[..., None], 0, 255).astype(np.uint8))
