"""Generate favicon set and Open Graph card in the site's ledger style."""
from PIL import Image, ImageDraw, ImageFont

PAPER = (244, 241, 234)
INK = (29, 37, 51)
INK60 = (91, 100, 114)
RED = (181, 56, 42)
RULE = (201, 195, 180)

GEORGIA = "/System/Library/Fonts/Supplemental/Georgia.ttf"
GEORGIA_BOLD = "/System/Library/Fonts/Supplemental/Georgia Bold.ttf"
MENLO = "/System/Library/Fonts/Menlo.ttc"

logo = Image.open("assets/modelup-t.png")

# ---- favicon: crop the M badge from the logo ----
top = logo.crop((0, 0, logo.width, int(logo.height * 0.63)))
bbox = top.getbbox()
badge = top.crop(bbox)

def favicon(size, pad_ratio=0.12):
    """Badge on paper tile with hairline ink border."""
    im = Image.new("RGBA", (size, size), PAPER + (255,))
    d = ImageDraw.Draw(im)
    bw = max(1, size // 32)
    d.rectangle([0, 0, size - 1, size - 1], outline=INK, width=bw)
    pad = int(size * pad_ratio)
    inner = size - 2 * pad
    b = badge.copy()
    b.thumbnail((inner, inner), Image.LANCZOS)
    im.paste(b, ((size - b.width) // 2, (size - b.height) // 2), b)
    return im

favicon(32).save("assets/favicon-32.png")
favicon(16, pad_ratio=0.08).save("assets/favicon-16.png")
favicon(180, pad_ratio=0.16).save("assets/apple-touch-icon.png")

# ---- OG card 1200x630 ----
W, H = 1200, 630
im = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(im)

d.rectangle([16, 16, W - 17, H - 17], outline=INK, width=3)
M = 70  # inner margin

mono = ImageFont.truetype(MENLO, 22)
mono_sm = ImageFont.truetype(MENLO, 19)
serif = ImageFont.truetype(GEORGIA_BOLD, 84)
serif_sm = ImageFont.truetype(GEORGIA, 30)

# kicker
d.text((M, 64), "FRACTIONAL CFO · FINANCIAL MODELING", font=mono, fill=RED)
kw = d.textlength("FRACTIONAL CFO · FINANCIAL MODELING", font=mono)
d.line([M + kw + 24, 76, W - M, 76], fill=RULE, width=2)

# headline with red underline under "smart money."
y = 140
d.text((M, y), "Where smart models", font=serif, fill=INK)
y2 = y + 104
d.text((M, y2), "meet ", font=serif, fill=INK)
mw = d.textlength("meet ", font=serif)
hook = "smart money."
d.text((M + mw, y2), hook, font=serif, fill=INK)
hw = d.textlength(hook, font=serif)
uy = y2 + 100
d.line([M + mw, uy, M + mw + hw, uy], fill=RED, width=7)

# lede
d.text((M, uy + 44), "Investor-ready models, dashboards, and business plans for founders.",
       font=serif_sm, fill=INK60)

# bottom band: logo badge + wordmark left, folio right
by = H - 150
d.line([M, by, W - M, by], fill=RULE, width=2)
b = badge.copy()
b.thumbnail((72, 72), Image.LANCZOS)
im.paste(b, (M, by + 28), b)
wm = ImageFont.truetype(GEORGIA_BOLD, 40)
d.text((M + b.width + 24, by + 40), "ModelUp", font=wm, fill=INK)
folio = "№ 01 — FREE 30-MIN CONSULT"
fw = d.textlength(folio, font=mono_sm)
d.text((W - M - fw, by + 50), folio, font=mono_sm, fill=INK60)

im.save("assets/og.png")
print("wrote favicon-16/32, apple-touch-icon, og.png", badge.size)
