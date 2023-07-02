import openpyxl
from openpyxl import Workbook
from openpyxl.styles import PatternFill

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

songs = ["hotline bling", "woohoo", "vacation", "abba"]
how_many = len(songs)


def unicolor_column(sheet, column, how_long, width, color):
    fill = PatternFill(start_color=color, end_color=color, fill_type="solid")
    
    for i in range(how_long):
        sheet.cell(row=i+1, column=column).value = ""
        sheet.cell(row=i+1, column=column).fill = fill
        
    sheet.column_dimensions[sheet.cell(row=1, column=column).column_letter].width = width


# coluumn 1 for gray squares
unicolor_column(sheet, 1, how_many, 6, "FF0000")
    
# column 2 for songs
for i, song in enumerate(songs):
    sheet.cell(row=i+1, column=2).value = song
    
# column 3 for black border
unicolor_column(sheet, 3, how_many, 3, "000000")

for i in range(how_many):
    sheet.cell(row=i+1, column=4).value = how_many - i

# Save the workbook with the changes
workbook.save("output.xlsx")