# Importing required packages
import re
import os
import string
import PySimpleGUI as sg
import plotly.graph_objects as go
from datetime import datetime


# Making list of colors and getting the working directory info
references = ["white", "red", "blue", "yellow",
              "purple", "green", "gray", "orange",
              "brown"]

folder = os.getcwd()

# 'FUNCTIONS FOR THE PROGRAM'

# Function to create the intro page to the program


def main_layout():
    m_layout = [
        [sg.Push(), sg.Text('Welcome to Plate Planner'), sg.Push()],
        [sg.Push(), sg.Text('Please Choose Your Plate Layout'), sg.Push()],
        [sg.HorizontalSeparator()],
        [sg.Push(), sg.Button('6-Well Plate Layout', k='-6Well_Layout-'), sg.Push()],
        [sg.Push(), sg.Button('12-Well Plate Layout', k='-12Well_Layout-'), sg.Push()],
        [sg.Push(), sg.Button('24-Well Plate Layout', k='-24Well_Layout-'), sg.Push()],
        [sg.Push(), sg.Button('48-Well Plate Layout', k='-48Well_Layout-'), sg.Push()],
        [sg.Push(), sg.Button('Custom Layout', k='-CUSTOM-'), sg.Push()],
        [sg.Text()],
        [sg.Button("", k="-Egg-", border_width=0, button_color="#64778d"),
         sg.Push(),
         sg.Button('Quit', k='-Quit-')]
    ]
    return m_layout

# Function to create the keys for the plate layout


def creating_keys(rows, columns):
    columns = columns
    rows_letters = string.ascii_uppercase[0:rows]
    label_keys = []
    color_keys = []
    rows_colors = []
    columns_colors = []

    for i in range(columns):
        i += 1
        label_keys_test = []
        color_key_test = []
        for j in rows_letters:
            key = "-{row}{col}-".format(row=j, col=i)
            label_keys_test.append(key)
            ckey = "-{row}{col}c-".format(row=j, col=i)
            color_key_test.append(ckey)
        label_keys.append(label_keys_test)
        color_keys.append(color_key_test)

    for i in rows_letters:
        rows_colors_key = "-row{letter}_color-".format(letter=i)
        rows_colors.append(rows_colors_key)

    for i in range(columns):
        i += 1
        columns_colors_key = '-column{col}_color-'.format(col=i)
        columns_colors.append(columns_colors_key)

    return label_keys, color_keys, rows_colors, columns_colors

# Function to create the plate layout


def layout_maker(nrows, ncolumns, title):

    wells_key, colors_key, rows_key, columns_key = creating_keys(rows=nrows, columns=ncolumns)

    letters = string.ascii_uppercase[0:nrows]

    first = [[sg.Text(s=(0, 2))]] + \
            [[sg.Text(letters[j], font=("Arial Bold", 13), pad=(5, 15)),
              sg.Combo(references, "white", k=rows_key[j], s=(6, 7), change_submits=True)]
             for j in range(nrows)] + \
            [[sg.Button("Save", k="-Save-"), sg.Button("Quit", k="-Quit-")]]

    layout_list = [sg.Column(first, element_justification='left'), sg.VerticalSeparator()]

    for i in range(ncolumns):
        full_column_layout = [[sg.Text(str(i+1), font=("Arial Bold", 13)),
                               sg.Combo(references, "white", k=columns_key[i], s=(6, 7), change_submits=True)]]
        cell_layout = [[sg.Input(s=25, k=j)] for j in wells_key[i]]

        color_cell_layout = [[sg.Combo(references, "white", k=j)] for j in colors_key[i]]

        for k in range(len(cell_layout)):
            full_column_layout.append(cell_layout[k])
            full_column_layout.append(color_cell_layout[k])

        layout_list.append(sg.Column(full_column_layout, element_justification='left'))

        display_layout = [[sg.Button('Change folder', s=(10, 1), k='-FOLDER-'),
                           sg.Push(),
                           sg.Text(title, font=('Arial Bold', 15), justification='center'),
                           sg.Push(), sg.Button("Return Main Menu", k='-Return-')], [sg.HorizontalSeparator()],
                          [layout_list]]

    return [display_layout], wells_key, colors_key, rows_key, columns_key


# Function to change saving location
def saving_location():

    change_folder = sg.popup_get_folder('Choose folder to save',
                                        title='Saving File',
                                        default_path=folder)

    if change_folder is None and change_folder == os.getcwd():
        change_folder = os.getcwd()

    if change_folder is None and change_folder != os.getcwd():
        change_folder = folder

    return change_folder

# Function to change the name of the color to a color that is more visually appealing


def color_changer(string):
    new_col = []
    for color in string:
        if color == "red":
            new_col.append("tomato")
        if color == "blue":
            new_col.append("royalblue")
        if color == "white":
            new_col.append("white")
        if color == "yellow":
            new_col.append("gold")
        if color == "purple":
            new_col.append("darkviolet")
        if color == "green":
            new_col.append("lightgreen")
        if color == "gray":
            new_col.append("silver")
        if color == "orange":
            new_col.append("darkorange")
        if color == "brown":
            new_col.append("sienna")
    return new_col

# Function to make and print the table


def table_maker(header, cells, cell_colors, file_name,
                height, width, scale):

    fig = go.Figure(data=[go.Table(  # Making the graphical table
        header=dict(
            values=header,  # Providing the header values
            line_color='black',
            fill_color="grey",
            align=['center'],
            font=dict(color='black', size=14)
        ),
        cells=dict(  # Making the cells of the tables
            values=cells,  # Providing the values for each cell of the table
            line_color='black',
            fill_color=cell_colors,  # The color for each cell background
            align=['center'],
            font=dict(color='black', size=15)
        ))
    ], layout=dict(autosize=True))


    # Saving on default directory
    # Height, Width, and Scale arguments where meant to be adjustable
    # But they were hard to adjust, thus they were fixed to a value that works
    # For all the tables (mainly the 48 well plate table)
    # If you can make it work in a dynamic fashion, please edit -RICS

    fig.write_image(file_name, height=height, width=width, scale=scale, format='png', engine='kaleido')

# Making mock layout to prevent error due to if condition below


wells_key, colors_key, rows_key, columns_key = creating_keys(rows=1, columns=1)

# MAIN LAYOUT


layout = main_layout()

# WINDOW


window = sg.Window(title="Plate Planner - by RICS", layout=layout)

# EVENT/HANDLING

while True:
    event, values = window.read()

    # Closing Program

    if event in (sg.WIN_CLOSED, '-Quit-'):
        break

    # Changing folder

    if event == '-FOLDER-':
        folder = saving_location()

    # Returning to Main Windows

    if event == '-Return-':
        window.close()
        layout_return = main_layout()
        window = sg.Window(title="Plate Planner - by RICS", layout=layout_return)

# PLATE LAYOUTS EVENTS

    if event == '-6Well_Layout-':
        window.close()
        plate_layout, wells_key, colors_key, rows_key, columns_key = layout_maker(nrows=2,
                                                                                  ncolumns=3,
                                                                                  title="6 Well Plate Layout")
        file_name = "6 Well Plate Layout.png"
        window = sg.Window(title="Plate Planner - by RICS", layout=plate_layout)

    if event == '-12Well_Layout-':
        window.close()
        plate_layout, wells_key, colors_key, rows_key, columns_key = layout_maker(nrows=3,
                                                                                  ncolumns=4,
                                                                                  title="12 Well Plate Layout")
        file_name = "12 Well Plate Layout.png"
        window = sg.Window(title='Plate Planner - by RICS', layout=plate_layout)

    if event == '-24Well_Layout-':
        window.close()
        plate_layout, wells_key, colors_key, rows_key, columns_key = layout_maker(nrows=4,
                                                                                  ncolumns=6,
                                                                                  title='24 Well Plate Layout')
        file_name = "24 Well Plate Layout.png"
        window = sg.Window(title='Plate Planner - by RICS', layout=plate_layout)

    if event == '-48Well_Layout-':
        window.close()
        plate_layout, wells_key, colors_key, rows_key, columns_key = layout_maker(nrows=6,
                                                                                  ncolumns=8,
                                                                                  title='48 Well Plate Layout')
        file_name = "48 Well Plate Layout.png"
        window = sg.Window(title='Plate Planner - by RICS', layout=plate_layout)

# CUSTOM LAYOUT

    # This makes a new window to get the values required to generate the custom plate layout

    if event == '-CUSTOM-':
        window.close()
        values_layout = [
            [sg.Push(), sg.Text('Please Choose the Number of Rows and Columns'), sg.Push()],
            [sg.HorizontalSeparator()],
            [sg.Push(), sg.Text('Number of Rows'), sg.Input('2', k='-nrows-', s=(4, 2)), sg.Push()],
            [sg.Push(), sg.Text('Number of Columns'), sg.Input('3', k='-ncolumns-', s=(4, 2)), sg.Push()],
            [sg.Push(), sg.Button('Done', k='-Done-'),
             sg.Button('Return', k='-Return-'),
             sg.Button('Quit', k='-Quit-'), sg.Push()]
        ]
        window = sg.Window(title='Plate Planner - by RICS', layout=values_layout)

    # Generating the actual layout

    if event == "-Done-":
        window.close()
        n_rows = int(values['-nrows-'])
        n_columns = int(values['-ncolumns-'])
        plate_layout, wells_key, colors_key, rows_key, columns_key = layout_maker(nrows=n_rows,
                                                                                  ncolumns=n_columns,
                                                                                  title="Custom Plate Layout")
        file_name = "Custom Plate Layout.png"
        window = sg.Window(title='Plate Planner - by RICS', layout=plate_layout)

    # Updating the whole row if the color was changed at the row letter

    if event in rows_key:
        row_letter = re.search("[A-Z]", event).group()
        keys_to_change = []
        for group_set in colors_key:
            for element in group_set:
                if row_letter in element:
                    keys_to_change.append(element)
        for key in keys_to_change:
            window[key].Update(values[event])

    # Updating the whole column if the color was changed at the column number

    if event in columns_key:
        column_number = re.search(r"\d+", event).group()
        keys_to_change = []
        for group_set in colors_key:
            for element in group_set:
                if column_number in element:
                    keys_to_change.append(element)
        for key in keys_to_change:
            window[key].Update(values[event])

    # Making the table and saving it as a png

    if event == '-Save-':

        # Preparing the list that will become the rows in the table
        row_letter = []
        for rows in rows_key:
            searching = re.search("[A-Z]", rows).group()
            row_letter.append(searching)

        # Making a variable list to add the information

        cells_values = [row_letter]

        # Checking if any well was left blank and editing for NaN

        for group_set in wells_key:
            string_elements = [values[k] for k in group_set]
            for position, character in enumerate(string_elements):
                if character == "":
                    string_elements[position] = "NaN"
            cells_values.append(string_elements)

        # Preparing the variable for the table function

        # Getting the date information to add to the table

        now = datetime.now()
        date = now.strftime("%m/%d/%Y")  # adjusted to US format
        date = "<b>" + date + "</b>"  # making them bold

        # Making the header value for the plate

        header_values = [date]

        for columns in columns_key:
            searching = re.search(r"\d+", columns).group()
            searching = "<b>" + searching + "</b>"
            header_values.append(searching)

        # Making the cell information value for the six well plate

        cell_col = [['grey'] * len(rows_key)]

        for group_set in colors_key:
            colors = [values[k] for k in group_set]
            colors = color_changer(colors)
            cell_col.append(colors)

        # Making the file name
        # Hard-coding location until adding a select path section
        save_name = f'{folder}\\{file_name}'

        # Making the plate and saving it

        if len(header_values) <= 4:
            height_val = None
            width_val = None

        if 4 < len(header_values) <= 5:
            height_val = 700
            width_val = 800

        if 5 < len(header_values) <= 7:
            height_val = 900
            width_val = 1000

        if 7 < len(header_values) <= 9:
            height_val = 1000
            width_val = 1500

        if len(header_values) > 9:
            height_val = 1500
            width_val = 2000


        table_maker(header=header_values, cells=cells_values,
                    cell_colors=cell_col, file_name=save_name,
                    height=height_val, width=width_val, scale=2)

    # EASTER SECTION

    if event == "-Egg-":
        sg.popup("Congratulations, You found me!",
                 "Where you looking for me? If not, how did you find me?",
                 "I'm not even close to the Quit button. Someone told you I exist, right?",
                 "Hmmmmm.... so much uncertainty... so much doubts on this outcome.",
                 "Anyway, do not forget to have your presentation ready for lab meeting.",
                 "You have some nice results for the PIs, right?... right?!",
                 "Thankfully for me, I schedule an unnecessary update during lab meeting, so I'm on the clear!",
                 "Oh well, I overstayed my welcome. Click on OK and I will be on my way.",
                 title="Programa hecho por Ismael Cabrera")

# Close

window.close()
