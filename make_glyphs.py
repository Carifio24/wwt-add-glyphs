from math import ceil
from string import ascii_letters, digits

from lxml.etree import Element, SubElement, tostring
from wand.drawing import Color, Drawing
from wand.image import Image

def get_size_width(extent_width, horizontal_spacing, n_cols):
    column_spacing_term = 2 * horizontal_spacing / (n_cols + 1)
    return extent_width + column_spacing_term

def get_size_height(extent_height, image_height):
    return extent_height + round((image_height * 0.01), 1)

# characters = digits + ascii_letters + " -+:/" 
characters = digits + ascii_letters + ' '

# For comparison with the original image
characters = " 0hr123456789-+JanuyFebMcApilgstSmOoNvDBCEdqVjxGHILPRTU"

image_file = "glyphs2.png"
xml_file = "glyphs2.xml"
image_width = 2048
font_height = 171

n_cols = 8
n_glyphs = len(characters)
n_rows = ceil(n_glyphs / n_cols)
n_rows = 8
row_height = 256
image_height = row_height * n_rows

padding = 28
horizontal_padding = padding
horizontal_spacing = int(image_width / n_cols)
vertical_padding = padding
vertical_spacing = row_height - font_height

# Draw the glyph image
character_data = {}
x = horizontal_padding
# y0 = int(font_height - (vertical_spacing / 2)) + vertical_padding  # Note that the y position is the glyph baseline
y0 = 0
y = y0
color = Color("rgba(255, 255, 255, 1)")
horizontal_addition = 3
with Drawing() as draw, Image(width=image_width, height=image_height, background=Color('transparent'), format="PNG32") as image:
    draw.font_size = font_height 
    draw.font_family = "Microsoft Sans Serif"
    draw.fill_color = color
    draw.font_style = "normal"

    # stroke_width = 3
    # draw.stroke_width = stroke_width
    # draw.stroke_color = color

    for char in characters:
        
        metrics = draw.get_font_metrics(image, char)
        width = round(metrics.text_width) if char != ' ' else 30
        height = round(metrics.text_height)
        with Image(width=width, height=height, background=Color("transparent")) as char_img:
            with Drawing() as char_ctx:
                char_ctx.font_family = draw.font_family
                char_ctx.font_size = draw.font_size
                char_ctx.fill_color = draw.fill_color
                char_ctx.text(0, int(metrics.ascender), char)
                char_ctx(char_img)
            
            new_width = width + horizontal_addition
            char_img.resize(new_width, height)
            image.composite(char_img, left=x, top=y)
            
 
        character_data[char] = (x, y, new_width, height)
        # draw.text(x, y, char)
        x += horizontal_spacing

        if x >= image_width:
            x = horizontal_padding
            y += row_height

    draw(image)
    image.alpha_channel = True
    image.save(filename=f"PNG32:{image_file}")

# Create the XML file
precision = 8
root = Element("GlyphItems")
for char, (x, y, width, height) in character_data.items():
    element = SubElement(root, "GlyphItem")
    is_space = char == ' '
    uv_height = 0 if is_space else round(height / image_height, precision)
    uv_width = round(width / image_width, precision)
    uv_left = round(x / image_width, precision)
    uv_top = round((y - y0) / image_height, precision)
    size_width = round(get_size_width(width, horizontal_spacing, n_cols), 4)
    size_height = round(get_size_height(height, image_height), 4)
    width = size_width if is_space else width

    element.set("Glyph", char)
    element.set("UVHeight", str(uv_height))
    element.set("UVWidth", str(uv_width))
    element.set("UVTop", str(uv_top))
    element.set("UVLeft", str(uv_left))
    element.set("ExtentsWidth", str(width))
    element.set("ExtentsHeight", str(height))
    element.set("SizeWidth", str(size_width))
    element.set("SizeHeight", str(size_height))

with open(xml_file, 'w') as f:
    f.write(tostring(root, pretty_print=True).decode())
