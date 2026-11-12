"""Generates input_image.png - a procedural sunset-over-a-mountain-lake landscape.

Used as the input image for Lab Task 04 (no external download needed).
Run:  python generate_input_image.py
"""
import numpy as np
from PIL import Image, ImageDraw
from scipy.ndimage import gaussian_filter, gaussian_filter1d, map_coordinates

W, H, S = 960, 640, 2            # final size and supersampling factor
w, h = W * S, H * S
rng = np.random.default_rng(7)
yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
horizon = int(0.60 * h)          # water line
sx, sy = 0.66 * w, 0.375 * h      # sun centre


def stops(t, pts):
    out = np.zeros(t.shape + (3,), np.float32)
    for c in range(3):
        out[..., c] = np.interp(t, [p[0] for p in pts], [p[1][c] for p in pts])
    return out


def smooth(a, lo, hi):
    t = np.clip((a - lo) / (hi - lo), 0, 1)
    return t * t * (3 - 2 * t)


# ---- sky ----------------------------------------------------------------
t = np.clip(yy / horizon, 0, 1)
sky = stops(t, [(0.0, (16, 14, 56)), (0.25, (56, 36, 108)), (0.5, (148, 60, 128)),
                (0.72, (232, 98, 98)), (0.88, (255, 158, 88)), (1.0, (255, 208, 132))])

# stars
st = (rng.random((h, w)) > 0.9994).astype(np.float32)
st = gaussian_filter(st, 1.2) * 60 * (1 - smooth(yy, 0.05 * h, 0.35 * h))
sky += st[..., None]

# sun glow + disc
d = np.hypot(xx - sx, yy - sy)
glow = np.exp(-(d / (0.30 * h)) ** 1.2)[..., None] * np.array([255, 150, 70], np.float32) * 0.75
sky = sky + glow
disc = np.clip((0.050 * h - d) / 3 + 0.5, 0, 1)[..., None]
sky = sky * (1 - disc) + np.array([255, 247, 216], np.float32) * disc

# clouds
n = np.zeros((h, w), np.float32)
for sig, wgt in [((40, 220), 1.0), ((18, 90), 0.55), ((8, 40), 0.3)]:
    g = gaussian_filter(rng.standard_normal((h, w)).astype(np.float32), sig)
    n += wgt * g / g.std()
n /= 1.85
band = smooth(yy, 0.04 * h, 0.14 * h) * (1 - smooth(yy, 0.36 * h, 0.52 * h))
cm = smooth(n, 0.15, 1.15) * band
lit = np.clip(1 - np.abs(xx - sx) / (0.75 * w), 0, 1) * 0.55 + np.clip(yy / (0.5 * h), 0, 1) * 0.55
lit = np.clip(lit, 0, 1)[..., None]
cloud = np.array([86, 48, 112], np.float32) * (1 - lit) + np.array([255, 150, 108], np.float32) * lit
sky = sky * (1 - cm[..., None] * 0.85) + cloud * (cm[..., None] * 0.85)


# ---- mountains ----------------------------------------------------------
def ridge(base, amp, rough_seed, dip=0.0):
    r = np.random.default_rng(rough_seed)
    f = np.zeros(w, np.float32)
    for o in range(6):
        g = gaussian_filter1d(r.standard_normal(w).astype(np.float32), w / (7 * 2 ** o), mode="reflect")
        f += (0.55 ** o) * g / g.std()
    f /= 1.6
    xs = np.arange(w, dtype=np.float32)
    y = base * h + amp * h * f + dip * h * np.exp(-((xs - sx) / (0.13 * w)) ** 2)
    return np.minimum(y, horizon - 6)


layers = [  # base, amp, seed, dip, colour, haze
    (0.43, 0.050, 11, 0.07, (150, 82, 140), 0.60),
    (0.50, 0.050, 23, 0.00, (78, 44, 100), 0.40),
    (0.555, 0.040, 37, 0.00, (40, 28, 72), 0.25),
]
scene = sky.copy()
for base, amp, seed, dip, col, haze in layers:
    ry = ridge(base, amp, seed, dip)[None, :]
    tv = np.clip((yy - ry) / np.maximum(horizon - ry, 1), 0, 1)[..., None]
    mist = np.array([255, 160, 110], np.float32)
    c = np.array(col, np.float32) * (1 - haze * tv) + mist * (haze * tv * 0.9)
    m = (np.clip((yy - ry) / 2.0 + 0.5, 0, 1) * (yy < horizon))[..., None]
    scene = scene * (1 - m) + c * m
scene[horizon:] = 0  # rows below the horizon are rebuilt as water

# ---- water --------------------------------------------------------------
dy = yy[horizon:] - horizon
depth = dy / (h - horizon)
phase = gaussian_filter(rng.standard_normal((h - horizon, w)).astype(np.float32), (2, 60))
phase /= phase.std()
src_y = 2 * horizon - yy[horizon:] + (1.5 + 8 * depth) * np.sin(yy[horizon:] * 0.22) + 2.5 * depth * phase
src_x = xx[horizon:] + (3 + 22 * depth) * np.sin(yy[horizon:] * 0.13 + 6 * phase)
src_y = np.clip(src_y, 0, horizon - 1)
refl = np.stack([map_coordinates(scene[..., c], [src_y, src_x], order=1, mode="nearest") for c in range(3)], -1)
water = refl * 0.82 + np.array([14, 24, 58], np.float32) * 0.18
deep = np.array([14, 16, 44], np.float32)
water = water * (1 - 0.55 * depth[..., None]) + deep * (0.55 * depth[..., None])
streak = np.exp(-((xx[horizon:] - sx) / (0.012 * w + 0.07 * dy)) ** 2)
streak *= np.clip(0.55 + 0.6 * np.sin(yy[horizon:] * 0.30 + 3 * phase), 0, 1) * np.exp(-dy / (0.30 * h))
water += streak[..., None] * np.array([255, 190, 110], np.float32) * 0.9
scene[horizon:] = water

# ---- foreground silhouettes (PIL, supersampled) --------------------------
img = Image.fromarray(np.clip(scene, 0, 255).astype(np.uint8))
dr = ImageDraw.Draw(img)
dark = (9, 8, 22)


def pine(x, yb, ph, pw):
    dr.rectangle([x - pw * 0.04, yb - ph * 0.12, x + pw * 0.04, yb], fill=dark)
    tiers = 6
    for i in range(tiers):
        top = yb - ph + i * ph * 0.14
        bot = yb - ph * 0.10 - (tiers - 1 - i) * ph * 0.10 + ph * 0.10
        half = pw * (0.22 + 0.78 * (i + 1) / tiers) / 2
        dr.polygon([(x, top), (x - half, bot), (x + half, bot)], fill=dark)


# left bank
bank = [(0, 0.86 * h), (0.07 * w, 0.82 * h), (0.16 * w, 0.835 * h), (0.27 * w, 0.87 * h),
        (0.36 * w, 0.915 * h), (0.45 * w, 0.955 * h), (0.5 * w, h), (0, h)]
dr.polygon(bank, fill=dark)
for x, ph, pw in [(0.025, 0.40, 0.085), (0.075, 0.30, 0.065), (0.13, 0.46, 0.10), (0.19, 0.26, 0.055),
                  (0.235, 0.34, 0.07), (0.295, 0.17, 0.04)]:
    yb = np.interp(x * w, [p[0] for p in bank[:7]], [p[1] for p in bank[:7]]) + 6
    pine(x * w, yb, ph * h, pw * w)
# right: small islet with cabin
isl = [(0.70 * w, 0.935 * h), (0.76 * w, 0.905 * h), (0.86 * w, 0.90 * h), (0.95 * w, 0.915 * h),
       (w, 0.93 * h), (w, h), (0.66 * w, h)]
dr.polygon(isl, fill=dark)
cx, cb = 0.84 * w, 0.905 * h
dr.rectangle([cx - 38, cb - 46, cx + 38, cb + 2], fill=dark)
dr.polygon([(cx - 50, cb - 44), (cx, cb - 88), (cx + 50, cb - 44)], fill=dark)
dr.rectangle([cx - 18, cb - 34, cx + 2, cb - 14], fill=(255, 196, 96))
dr.rectangle([cx + 14, cb - 62, cx + 24, cb - 46], fill=dark)
pine(0.77 * w, 0.915 * h, 0.22 * h, 0.05 * w)
pine(0.93 * w, 0.93 * h, 0.30 * h, 0.065 * w)
# window glow on water
# birds
for bx, by, s in [(0.22, 0.20, 16), (0.26, 0.17, 12), (0.30, 0.215, 10), (0.50, 0.12, 11), (0.55, 0.15, 8)]:
    x0, y0 = bx * w, by * h
    for sgn in (-1, 1):
        dr.line([(x0, y0), (x0 + sgn * s, y0 - s * 0.55), (x0 + sgn * 2 * s, y0 + s * 0.05)],
                fill=(22, 14, 40), width=3, joint="curve")

img = img.resize((W, H), Image.LANCZOS)

# ---- finishing: vignette + grain ----------------------------------------
a = np.asarray(img).astype(np.float32)
Y, X = np.mgrid[0:H, 0:W].astype(np.float32)
vig = 1 - 0.28 * (((X - W / 2) / (W / 2)) ** 2 + ((Y - H / 2) / (H / 2)) ** 2) / 2
a = a * vig[..., None] + rng.normal(0, 1.6, a.shape).astype(np.float32)
Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).save("input_image.png", optimize=True)
print("saved input_image.png", (W, H))
