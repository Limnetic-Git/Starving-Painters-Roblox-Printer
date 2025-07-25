from PIL import Image, ImageColor

def hex_to_rgb(hex_color):
    return ImageColor.getcolor(hex_color, "RGB")

def get_difference(color1, color2):
    r_dif = max([color1[0], color2[0]]) - min([color1[0], color2[0]])
    g_dif = max([color1[1], color2[1]]) - min([color1[1], color2[1]])
    b_dif = max([color1[2], color2[2]]) - min([color1[2], color2[2]])
    return r_dif + g_dif + b_dif

def create_masks(hex_array):
    colors_on_picture = []
    masks = {}
    for x in range(32):
        for y in range(32):
            if not hex_array[x][y] in colors_on_picture:
                colors_on_picture.append(hex_array[x][y])
                new_mask = eval(str(hex_array.copy()))
                for x_ in range(32):
                    for y_ in range(32):
                        if new_mask[x_][y_] != hex_array[x][y]:
                            new_mask[x_][y_] = None
                masks[hex_array[x][y]] = new_mask
    return masks, colors_on_picture
    
def optimize_masks(masks, colors_on_picture, intensity):
    new_masks = masks.copy()
    new_colors_on_picture = colors_on_picture.copy()
    i = 0
    while i < len(new_colors_on_picture):
        i_color = hex_to_rgb(new_colors_on_picture[i])
        j = i + 1
        while j < len(new_colors_on_picture):
            j_color = hex_to_rgb(new_colors_on_picture[j])
            dif = get_difference(i_color, j_color)
            if dif <= intensity:
                for x in range(32):
                    for y in range(32):
                        if new_masks[new_colors_on_picture[j]][x][y] is not None:
                            new_masks[new_colors_on_picture[i]][x][y] = new_colors_on_picture[i]
                del new_masks[new_colors_on_picture[j]]
                new_colors_on_picture.pop(j)
            else:
                j += 1
        i += 1
    
    return new_masks, new_colors_on_picture
                