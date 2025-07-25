from PIL import Image, ImageColor
from collections import defaultdict


def get_most_common_hex_color(masks, colors_on_picture):
    colors = [0] * len(colors_on_picture)
    for i in range(len(colors_on_picture)):
        for x in range(32):
            for y in range(32):
                if masks[colors_on_picture[i]][x][y] != None:
                    colors[i] += 1
    max_color = 0
    for i in range(len(colors)):
        if colors[i] == max(colors):
            max_color = i
    return colors_on_picture[max_color]


def image_to_hex_array(image_path):
    img = Image.open(image_path)
    img = img.convert('RGB')
    width, height = img.size
    hex_array = []
    for y in range(height):
        row = []
        for x in range(width):
            r, g, b = img.getpixel((x, y))
            hex_color = "#{:02x}{:02x}{:02x}".format(r, g, b)
            row.append(hex_color)
        hex_array.append(row)
    
    return hex_array



