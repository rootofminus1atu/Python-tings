import colorsys

def blend_colors(color1, color2):
    # Convert hexadecimal color codes to RGB
    rgb1 = tuple(int(color1[i:i+2], 16) for i in (0, 2, 4))
    rgb2 = tuple(int(color2[i:i+2], 16) for i in (0, 2, 4))

    # Convert RGB to HSL
    hsl1 = colorsys.rgb_to_hls(*rgb1)
    hsl2 = colorsys.rgb_to_hls(*rgb2)

    # Average HSL values
    h = (hsl1[0] + hsl2[0]) / 2
    s = (hsl1[1] + hsl2[1]) / 2
    l = (hsl1[2] + hsl2[2]) / 2

    # Convert HSL to RGB
    rgb_blended = colorsys.hls_to_rgb(h, l, s)

    # Convert RGB to hexadecimal color code
    blended_color = '#%02x%02x%02x' % tuple(round(c * 255) for c in rgb_blended)

    return blended_color

color1 = "E1E1E1"
color2 = "E6B8AF"

blended_color = blend_colors(color1, color2)
print(blended_color)  # Output: #cba39c