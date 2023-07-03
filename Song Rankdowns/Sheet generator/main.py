import openpyxl
from openpyxl import Workbook
from openpyxl.styles import PatternFill
from helpers import *
import inflect
p = inflect.engine()



# Create a new workbook
workbook = Workbook()

# Save the workbook to a file
workbook.save("output.xlsx")

# Load the workbook from the saved file
workbook = openpyxl.load_workbook("output.xlsx")

# Select the active sheet
sheet = workbook.active


"""# Add inputs to the sheet
sheet["A1"] = "Name"
sheet["B1"] = "Age"

sheet["A2"] = "Joooooooooooooooo"
sheet["B2"] = 25

sheet["A3"] = "Jane"
sheet["B3"] = 30


# Rescale column A to fit the content
sheet.column_dimensions['A'].width = 15

# Rescale column B to fit the content
sheet.column_dimensions['B'].width = 5"""








songs = ["hotline bling", "woohoo", "vacation", "bruja", "bruja", "bruja", "bruja", "bruja", "bruja", "bruja", "bruja", "bruja", "bruja", "anaconda", "MASS OF THE FERMENTING DERGS"]
users = ["joe", "jane", "sasha velour"]
nominations_num = 6

general_colors = ['red', 'orange', 'yellow','green']
top3_colors = ['bronze', 'silver', 'gold']

color_ranges = get_color_ranges(len(songs) - 3, general_colors) + top3_colors

colors_guide = {
    "red": {
        "primary": "EA9999",
        "secondary": "F4CCCC"
    },
    "orange": {
        "primary": "F9CB9C",
        "secondary": "FCE5CD"
    },
    "yellow": {
        "primary": "FFE599",
        "secondary": "FFF2CC"
    },
    "green": {
        "primary": "B6D7A8",
        "secondary": "D9EAD3"
    },
    "bronze": {
        "primary": "B45F06",
        "secondary": "E69138"
    },
    "silver": {
        "primary": "B7B7B7",
        "secondary": "D9D9D9"
    },
    "gold": {
        "primary": "BF9000",
        "secondary": "F1C232"
    }
}





# coluumn 1 for gray squares
unicolor_column2(sheet, column=1, start=0, end=len(songs)+1, width=3, color="808080")
    
# column 2 for songs
for i, song in enumerate(songs):
    sheet.cell(row=i+2, column=2).value = song
    
# column 3 for black border
unicolor_column(sheet, 3, len(songs), 3, "000000")

def scoreboard(sheet, songs, color_ranges):
    # in D and E columns
    D = 4
    E = 5

    sheet.cell(row=1, column=D).value = "Place:"
    sheet.cell(row=1, column=E).value = "Score:"

    # D for place
    for i in range(len(songs)):
        sheet.cell(row=i+2, column=D).value = p.ordinal(len(songs) - i)

        color = colors_guide[color_ranges[i]]["primary"]
        fill = PatternFill(start_color=color, end_color=color, fill_type="solid")
        sheet.cell(row=i+2, column=D).fill = fill

    # E for songs
    for i in range(len(songs)):
        sheet.cell(row=i+2, column=E).value = ""

        color = colors_guide[color_ranges[i]]["secondary"]
        fill = PatternFill(start_color=color, end_color=color, fill_type="solid")
        sheet.cell(row=i+2, column=E).fill = fill

scoreboard(sheet, songs, color_ranges)

# column 6 for black border
unicolor_column2(sheet, column=6, start=0, end=len(songs)+1, width=3, color="000000")




# next... nominations, hell

def nominations(sheet, songs, users):
    # starting from G column (7th column)
    col = 7

    counter = len(songs)

    color = colors_guide["yellow"]["secondary"]
    noms_fill = PatternFill(start_color=color, end_color=color, fill_type="solid")


    for i in range(len(general_colors)):
        # important columns
        first = col + 3*i
        second = col + 3*i + 1
        last = col + 3*i + 2

        # important rows
        after_noms_row = nominations_num + 2

        # important colors
        color = colors_guide[general_colors[i]]["primary"]
        decision_fill_prim = PatternFill(start_color=color, end_color=color, fill_type="solid")
        color = colors_guide[general_colors[i]]["secondary"]
        decision_fill_sec = PatternFill(start_color=color, end_color=color, fill_type="solid")



        # header
        sheet.cell(row=1, column=first).value = "Nominated Song:"
        sheet.cell(row=1, column=second).value = "Nominated Song Link:"

        # nominations
        for j in range(nominations_num):
            sheet.cell(row=j+2, column=first).value = "h"
            sheet.cell(row=j+2, column=first).fill = noms_fill
            sheet.cell(row=j+2, column=second).value = "h"
            sheet.cell(row=j+2, column=second).fill = noms_fill

        # gap row
        sheet.cell(row=after_noms_row, column=first).value = "EMPTY"
        sheet.cell(row=after_noms_row, column=second).value = "EMPTY"

        # decisions
        how_many_colors = len([color for color in color_ranges if color == general_colors[i]])

        

        for j in range(how_many_colors):
            new_row = after_noms_row + (len(users)+3)*j + 1

            sheet.cell(row=new_row, column=first).value = f"{p.ordinal(counter)} Place Vote:"
            sheet.cell(row=new_row, column=first).fill = decision_fill_prim
            sheet.cell(row=new_row, column=second).value = "Explain Why You're Voting This Song:"
            sheet.cell(row=new_row, column=second).fill = decision_fill_prim
            counter -= 1

            for k in range(len(users)):
                sheet.cell(row=new_row+1+k, column=first).value = f"{users[k]}'s Vote: "
                sheet.cell(row=new_row+1+k, column=first).fill = decision_fill_sec
                sheet.cell(row=new_row+1+k, column=second).value = "opinion"
                sheet.cell(row=new_row+1+k, column=second).fill = decision_fill_sec

            elem_row = new_row + len(users) + 1
            sheet.cell(row=elem_row, column=first).value = "Eliminated Song: "
            sheet.cell(row=elem_row+1, column=first).value = "EMPTY"

    # add bronze, silver and gold
    for i in range(3):
        pass



            




# nominations(sheet, songs, users)
decision_space(sheet, 7, 7, 3, colors_guide["yellow"]["primary"], colors_guide["yellow"]["secondary"], users)


# Save the workbook with the changes
workbook.save("output.xlsx")