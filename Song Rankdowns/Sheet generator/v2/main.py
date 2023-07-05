from openpyxl import Workbook
from openpyxl.styles import PatternFill
import inflect
p = inflect.engine()

from excel_helpers import *
from general_helpers import get_color_ranges_with_specials
from config import *



workbook = Workbook()
sheet = workbook.active

color_ranges = get_color_ranges_with_specials(songs, general_colors, top3_colors)

black_border(sheet, 1)
song_list(
    sheet=sheet, 
    r=1, 
    c=2, 
    songs=songs
)
black_border(sheet, 3)
scoreboard(
    sheet=sheet, 
    r=1, 
    c=4,
    color_ranges=color_ranges
)
black_border(sheet, 6)
showtime(
    sheet=sheet, 
    r=1, 
    c=7, 
    general_colors=general_colors, 
    special_colors=top3_colors, 
    color_ranges=color_ranges, 
    users=users, 
    how_many_noms=4
)

workbook.save("outputv2.xlsx")