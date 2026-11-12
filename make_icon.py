from PIL import Image, ImageDraw, ImageFilter

S = 2048
img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
draw = ImageDraw.Draw(img)

# Закруглённый квадрат (современная форма иконки приложения)
pad = 120
draw.rounded_rectangle((pad, pad, S - pad, S - pad), radius=420, fill=(11, 14, 30, 255), outline=(45, 62, 130, 255), width=24)

# Мягкое космическое свечение за планетой
glow = Image.new("RGBA", (S, S), (0, 0, 0, 0))
g_draw = ImageDraw.Draw(glow)
g_draw.ellipse((460, 460, S - 460, S - 460), fill=(108, 62, 235, 130))
glow = glow.filter(ImageFilter.GaussianBlur(140))
img = Image.alpha_composite(img, glow)
draw = ImageDraw.Draw(img)

# Звёзды
for x, y, r in [(480, 520, 14), (1560, 480, 18), (1600, 1460, 14), (450, 1500, 12), (1024, 340, 12)]:
    draw.ellipse((x - r, y - r, x + r, y + r), fill=(215, 235, 255, 255))

# Планета с объёмным бликом
cx, cy, pr = S // 2, S // 2, 460
draw.ellipse((cx - pr, cy - pr, cx + pr, cy + pr), fill=(96, 52, 220, 255))
draw.ellipse((cx - pr + 55, cy - pr + 45, cx + pr - 130, cy + pr - 130), fill=(138, 92, 255, 255))

# Неоновое орбитальное кольцо
ring = Image.new("RGBA", (S, S), (0, 0, 0, 0))
r_draw = ImageDraw.Draw(ring)
r_draw.arc((240, 760, S - 240, S - 760), start=342, end=198, fill=(0, 229, 255, 255), width=68)
ring = ring.rotate(-22, resample=Image.Resampling.BICUBIC)
img = Image.alpha_composite(img, ring)

# Сжатие со сглаживанием в icon.ico и preview-иконку
final = img.resize((512, 512), Image.Resampling.LANCZOS)
final.save("icon.ico", format="ICO", sizes=[(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)])
print("Готово: icon.ico создан!")
