import time
import board
import neopixel
from PIL import Image, ImageDraw, ImageFont

# 1. Panel Configuration
MATRIX_WIDTH = 32
MATRIX_HEIGHT = 8
NUM_PIXELS = MATRIX_WIDTH * MATRIX_HEIGHT

# 2. Setup your text and colors
TEXT_TO_SHOW = " HELLO PARENTS "
TEXT_COLOR = (255, 0, 0)      # Red (R, G, B)
BACKGROUND_COLOR = (0, 0, 0)  # Off
BRIGHTNESS = 0.15             # 15% brightness

# 3. Initialize the NeoPixel strip on GPIO 18
pixels = neopixel.NeoPixel(
    board.D18,
    NUM_PIXELS,
    brightness=BRIGHTNESS,
    auto_write=False,
    pixel_order=neopixel.GRB
)

# 4. Map coordinates assuming vertical pixel layout
def get_pixel_index(x, y):
    if x % 2 == 0:
        return (x * MATRIX_HEIGHT) + y
    else:
        return (x * MATRIX_HEIGHT) + (MATRIX_HEIGHT - 1 - y)

# 5. Create an image in memory to draw the text onto
try:
    font = ImageFont.load_default()
except IOError:
    font = None

text_width = len(TEXT_TO_SHOW) * 6
total_image_width = text_width + (MATRIX_WIDTH * 2)

# Create a slightly taller buffer so we don't look outside image bounds
image = Image.new("RGB", (total_image_width, MATRIX_HEIGHT + 4), BACKGROUND_COLOR)
draw = ImageDraw.Draw(image)

# Drawing at -2 vertically pushes the text up by 2 lights on the matrix
draw.text((MATRIX_WIDTH, -2), TEXT_TO_SHOW, fill=TEXT_COLOR, font=font)

# 6. Infinite Scroll Loop
print("Scrolling text (shifted 2 pixels up)... Press Ctrl+C to stop.")
try:
    while True:
        for x_offset in range(text_width + MATRIX_WIDTH):
            pixels.fill((0, 0, 0))

            for y in range(MATRIX_HEIGHT):
                for x in range(MATRIX_WIDTH):
                    # Sample cleanly starting from the top row (0)
                    pixel_color = image.getpixel((x + x_offset, y))
                    pixel_index = get_pixel_index(x, y)

                    if pixel_index < NUM_PIXELS:
                        pixels[pixel_index] = pixel_color

            pixels.show()
            time.sleep(0.05)

except KeyboardInterrupt:
    pixels.fill((0, 0, 0))
    pixels.show()
    print("\nStopped.")
