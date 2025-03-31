from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageEnhance, ImageFilter
import matplotlib.pyplot as plt
import numpy as np

# Load logo
logo_path = "sc-logo-circle.png"
logo = Image.open(logo_path).convert("RGBA")

# Create base image
size = 800
base = Image.new("RGBA", (size, size), "white")
draw = ImageDraw.Draw(base)
center = size // 2
outer_radius = size // 2 - 20
inner_radius = outer_radius - 80

# Draw outer and inner circles
draw.ellipse((center - outer_radius, center - outer_radius, center + outer_radius, center + outer_radius), outline="blue", width=8)
draw.ellipse((center - inner_radius, center - inner_radius, center + inner_radius, center + inner_radius), outline="blue", width=6)

# Resize and paste logo
logo_size = inner_radius * 2 - 40
logo = logo.resize((logo_size, logo_size), Image.Resampling.LANCZOS)
base.paste(logo, (center - logo_size // 2, center - logo_size // 2), logo)

# Font setup
# font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
# font = ImageFont.truetype(font_path, 26)

# Function to draw readable arc text
def draw_arc_text(draw, text, radius, position, font, upward=True):
    text_width = sum(font.getlength(c) for c in text)
    angle_offset = text_width / (2 * np.pi * radius) * 360 / 2
    angle = -angle_offset if upward else 180 + angle_offset

    for char in text:
        w = font.getlength(char)
        angle_rad = np.radians(angle)
        x = position[0] + radius * np.cos(angle_rad)
        y = position[1] + radius * np.sin(angle_rad)

        char_img = Image.new("RGBA", (100, 100), (255, 255, 255, 0))
        d = ImageDraw.Draw(char_img)
        d.text((50 - w / 2, 30), char, font=font, fill="blue")
        rotated_char = char_img.rotate(-angle if upward else -angle + 180, center=(50, 50), resample=Image.Resampling.BICUBIC)
        base.paste(rotated_char, (int(x) - 50, int(y) - 50), rotated_char)

        angle += (w / (2 * np.pi * radius)) * 360

# Add arc text
# draw_arc_text(draw, "CODE UNIVERSITY OF APPLIED SCIENCES", outer_radius - 20, (center, center), font, upward=True)
# draw_arc_text(draw, "STUDENT COUNCIL", outer_radius - 20, (center, center), font, upward=False)

# Create grunge texture
grunge = base.convert("L").convert("RGBA")
texture = Image.effect_noise((size, size), 80).convert("L")
texture = ImageEnhance.Contrast(texture).enhance(2.0)
texture = ImageOps.invert(texture).convert("RGBA")
texture = texture.resize(base.size).convert("RGBA")

# Apply texture
grunge_stamp = Image.blend(base.convert("RGBA"), texture, alpha=0.25)
grunge_stamp = grunge_stamp.filter(ImageFilter.GaussianBlur(0.5))

# Show result
grunged_image = grunge_stamp.convert("RGB")
plt.imshow(grunged_image)
plt.axis("off")
plt.show()
