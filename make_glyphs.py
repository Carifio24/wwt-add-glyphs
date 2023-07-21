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
image_file = "glyphs2.png"
xml_file = "glyphs2.xml"
image_width = 2048
font_height = 171

n_cols = 8
n_glyphs = len(characters)
n_rows = ceil(n_glyphs / n_cols)
row_height = 256
image_height = row_height * n_rows
horizontal_padding = 36
horizontal_spacing = int(image_width / n_cols)
vertical_spacing = row_height - font_height

# Draw the glyph image
character_data = {}
x = horizontal_padding
y = font_height  # Start at font_height as the y position is the bottom of the glyph
with Drawing() as draw, Image(width=image_width, height=image_height) as image:
    draw.font_size = font_height 
    draw.font_family = "Microsoft Sans Serif"
    draw.fill_color = Color("white")
    for char in characters:
        metrics = draw.get_font_metrics(image, char)
        if x >= image_width:
            x = horizontal_padding
            y += row_height
        width = round(metrics.text_width) if char != ' ' else 0
        character_data[char] = (x, y, width, round(metrics.text_height))
        draw.text(x, y, char)
        x += horizontal_spacing

    draw(image)
    image.save(filename=image_file)

# Create the XML file
precision = 8
root = Element("GlyphItems")
for char, (x, y, width, height) in character_data.items():
    element = SubElement(root, "GlyphItem")
    is_space = char == ' '
    uv_height = 0 if is_space else round(height/ image_height, precision)
    uv_width = round(width / image_width, precision)
    uv_left = round(x / image_width, precision)
    uv_top = round((y - font_height) / image_height, precision)
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
