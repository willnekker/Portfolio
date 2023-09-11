
#-----Statement of Authorship----------------------------------------#
#
#  This is an individual assessment item for QUT's teaching unit
#  IFB104, "Building IT Systems", Semester 1, 2023.  By submitting
#  this code I agree that it represents my own work.  I am aware of
#  the University rule that a student must not act in a manner
#  which constitutes academic dishonesty as stated and explained
#  in QUT's Manual of Policies and Procedures, Section C/5.3
#  "Academic Integrity" and Section E/2.1 "Student Code of Conduct".
#
#  Put your student number here as an integer and your name as a
#  character string:
#
student_number = 11548045
student_name   = "Willem Nekker"
#
#  NB: Files submitted without a completed copy of this statement
#  will not be marked.  All files submitted will be subjected to
#  software plagiarism analysis using the MoSS system
#  (http://theory.stanford.edu/~aiken/moss/).
#
#--------------------------------------------------------------------#



#-----Assessment Task 2 Description----------------------------------#
#
#  In this assessment task you will combine your knowledge of Python
#  programming, HTML-style mark-up languages, pattern matching,
#  database management, and Graphical User Interface design to produce
#  a robust, interactive "app" that allows its user to view and save
#  data from multiple online sources.
#
#  See the client's briefings accompanying this file for full
#  details.
#
#  Note that this assessable assignment is in multiple parts,
#  simulating incremental release of instructions by a paying
#  "client".  This single template file will be used for all parts,
#  together with some non-Python support files.
#
#--------------------------------------------------------------------#



#-----Set up---------------------------------------------------------#
#
# This section imports standard Python 3 modules sufficient to
# complete this assignment.  Don't change any of the code in this
# section, but you are free to import other Python 3 modules
# to support your solution, provided they are standard ones that
# are already supplied by default as part of a normal Python/IDLE
# installation.
#
# However, you may NOT use any Python modules that need to be
# downloaded and installed separately, such as "Beautiful Soup" or
# "Pillow", because the markers will not have access to such modules
# and will not be able to run your code.  Only modules that are part
# of a standard Python 3 installation may be used.

# A function for exiting the program immediately (renamed
# because "exit" is already a standard Python function).
from sys import exit as abort

# A function for opening a web document given its URL.
# [You WILL need to use this function in your solution,
# either directly or via the "download" function below.]
from urllib.request import urlopen

# Some standard Tkinter functions.  [You WILL need to use
# SOME of these functions in your solution.]  You may also
# import other widgets from the "tkinter" module, provided they
# are standard ones and don't need to be downloaded and installed
# separately.  (NB: Although you can import individual widgets
# from the "tkinter.tkk" module, DON'T import ALL of them
# using a "*" wildcard because the "tkinter.tkk" module
# includes alternative versions of standard widgets
# like "Label" which leads to confusion.  If you want to use
# a widget from the tkinter.ttk module name it explicitly,
# as is done below for the progress bar widget.)
from tkinter import *
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText
from tkinter.ttk import Progressbar

# Functions for finding occurrences of a pattern defined
# via a regular expression.  [You do not necessarily need to
# use these functions in your solution, because the problem
# may be solvable with the string "find" function, but it will
# be difficult to produce a concise and robust solution
# without using regular expressions.]
from re import *

# A function for displaying a web document in the host
# operating system's default web browser (renamed to
# distinguish it from the built-in "open" function for
# opening local files).  [You WILL need to use this function
# in your solution.]
from webbrowser import open as urldisplay

# All the standard SQLite database functions.  [You WILL need
# to use some of these in your solution.]

## WHY DOESNT SQLITE 3 IMPORT!!!!!!!!
from sqlite3 import *
import sqlite3

#
#--------------------------------------------------------------------#



#-----Validity Check-------------------------------------------------#
#
# This section confirms that the student has declared their
# authorship.  You must NOT change any of the code below.
#

if not isinstance(student_number, int):
    print('\nUnable to run: No student number supplied',
          '(must be an integer)\n')
    abort()
if not isinstance(student_name, str):
    print('\nUnable to run: No student name supplied',
          '(must be a character string)\n')
    abort()

#
#--------------------------------------------------------------------#



#-----Supplied Function----------------------------------------------#
#
# Below is a function you can use in your solution if you find it
# helpful.  You are not required to use this function, but it may
# save you some effort.  Feel free to modify the function or copy
# parts of it into your own code.
#

# A function to download and save a web document.  The function
# returns the downloaded document as a character string and
# optionally saves it as a local file.  If the attempted download
# fails, an error message is written to the shell window and the
# special value None is returned.  However, the root cause of the
# problem is not always easy to diagnose, depending on the quality
# of the response returned by the web server, so the error
# messages generated by the function below are indicative only.
#
# Parameters:
# * url - The address of the web page you want to download.
# * target_filename - Name of the file to be saved (if any).
# * filename_extension - Extension for the target file, usually
#      "html" for an HTML document or "xhtml" for an XML
#      document.
# * save_file - A file is saved only if this is True. WARNING:
#      The function will silently overwrite the target file
#      if it already exists!
# * char_set - The character set used by the web page, which is
#      usually Unicode UTF-8, although some web pages use other
#      character sets.
# * incognito - If this parameter is True the Python program will
#      try to hide its identity from the web server. This can
#      sometimes be used to prevent the server from blocking access
#      to Python programs. However we discourage using this
#      option as it is both unreliable and unethical to
#      override the wishes of the web document provider!

import re

def download(url, target_filename='filename',
             target_directory='Assignment-2', 
             filename_extension='html',
             save_file=True,
             char_set='UTF-8',
             incognito=True):
    # Import the function for opening online documents and
    # the class for creating requests
    from urllib.request import urlopen, Request

    # Import an exception sometimes raised when a web server
    # denies access to a document
    from urllib.error import HTTPError

    # Import an exception raised when a web document cannot
    # be downloaded due to some communication error
    from urllib.error import URLError

    # Open the web document for reading (and make a "best
    # guess" about why if the attempt fails, which may or
    # may not be the correct explanation depending on how
    # well behaved the web server is!)
    
    if incognito:
        # Pretend to be a web browser instead of
        # a Python script (NOT RELIABLE OR RECOMMENDED!)
        request = Request(url)
        request.add_header('User-Agent',
                               'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ' +
                               'AppleWebKit/537.36 (KHTML, like Gecko) ' +
                               'Chrome/42.0.2311.135 Safari/537.36 Edge/12.246')
    else:
        request = url
    web_page = urlopen(request)

    # Read the contents as a character string
    try:
        web_page_contents = web_page.read().decode(char_set)
    except UnicodeDecodeError as error:
        print("\nUnable to decode document from URL '")
        print("Error message was:", error, "\n")
        return None
    except Exception as error:
        print("\nSomething went wrong when trying to decode")
        print("Error message was:", error, "\n")
        return None

    # Optionally write the contents to a local text file
    # (overwriting the file if it already exists!)
    if save_file == True:
        try:
            # Correct way to join directory, filename, and extension
            file_path = target_directory + '/' + target_filename + '.' + filename_extension
            text_file = open(file_path, 'w', encoding=char_set)
            text_file.write(web_page_contents)
            text_file.close()
        except Exception as error:
            print("\nUnable to write to file '" + target_filename + "'")
            print("Error message was:", error, "\n")

    # Return the downloaded document to the caller
    return web_page_contents

#
#--------------------------------------------------------------------#



#-----Student's Solution---------------------------------------------#
#
# Put your solution below.
import sqlite3
from tkinter import *
from tkinter import messagebox
import re
import webbrowser

# Create the main window
task_2_main_window = Tk()
task_2_main_window.title("Wills Reviews")
task_2_main_window.configure()
task_2_main_window.config(bg='#DEDED7')
review_status_text = "Please Select an Entertainment Option ..."
Summary_Button_Text = ""
#how to show error message processed before errors can happen
def show_error_message(message):
    messagebox.showerror("Error", message)

#update radio button selection
def updateRadioButtonSelection(variable, value):
    global review_status_text
    review_status_text = value
    review_status.config(text=review_status_text)

# create label and label frame for review status
review_status_frame = LabelFrame(task_2_main_window, font=("Arial", 14), text="Review Status", padx=10, pady=20)
review_status_frame.grid(row=0, column=0, columnspan=1, padx=10, pady=10) 
review_status_frame.config(bg='#DEDED7')
review_status = Label(review_status_frame, text=(review_status_text), font=("Arial", 12))
review_status.config(bg='#DEDED7')
review_status.pack()


#frame created for options (radio triple j etc)
options_frame = LabelFrame(task_2_main_window, font=("Arial", 14), text="Entertainment Options", padx=40, pady=40)
options_frame.grid_propagate(False)
options_frame.config(bg='#DEDED7')
options_frame.config(width=500, height=200)

#setup of radio button selection
RadioButtonSelection = StringVar()
RadioButtonSelection.set(' ')
review_status_text = (RadioButtonSelection.get())

#where selected value is stored
Option_1_text = "Radio - Triple J"
Option_2_text = "Theatre - The Tivoli"
Option_3_text = "Games - MetaCritic"

#radiobuttons for this
option1 = Radiobutton(options_frame, text = Option_1_text, variable = RadioButtonSelection, value = Option_1_text, command = lambda: updateRadioButtonSelection(RadioButtonSelection, RadioButtonSelection.get()))
option2 = Radiobutton(options_frame, text = Option_2_text, variable = RadioButtonSelection, value = Option_2_text, command = lambda: updateRadioButtonSelection(RadioButtonSelection, RadioButtonSelection.get()))
option3 = Radiobutton(options_frame, text = Option_3_text, variable = RadioButtonSelection, value = Option_3_text, command = lambda: updateRadioButtonSelection(RadioButtonSelection, RadioButtonSelection.get()))
option1.config(bg='#DEDED7')
option2.config(bg='#DEDED7')
option3.config(bg='#DEDED7')

#position radio buttons
option1.grid(row = 0, column = 0, sticky = 'w')
option2.grid(row = 1, column = 0, sticky = 'w')
option3.grid(row = 2, column = 0, sticky = 'w')

def SummaryButtonOnclick():
    global Summary_Button_Text
    Summary_Button_Text = " "
    global review_status_text

    try:
        selected_option = RadioButtonSelection.get()
        if selected_option == Option_1_text:
            Summary_Button_Text = f"The song to be reviewed is {TripleJTitle}, and the author is {TripleJAuthor}"
        elif selected_option == Option_2_text:
            Summary_Button_Text = f"The next event coming up is by {TheTivoliName}, and they are from the {TheTivoliNationality} region"
        elif selected_option == Option_3_text:
            Summary_Button_Text = f"The game to be reviewed is {metacriticAuthor}, and it came out on {metacriticTitle}"
        else:
            show_error_message(f"Please Select an Entertainment Option {selected_option}")
            return

        review_status.config(text=Summary_Button_Text)
    except Exception as error:
        show_error_message(f"An error occurred in SummaryButtonOnclick:\n{error}")


def DetailButtonOnClick():
    try:
        #find selected option
        selected_option = RadioButtonSelection.get()
        if selected_option == " ":
            show_error_message("Please select an entertainment option.")
            return

        #set url based on whats selected (inside the function)
        url_mapping = {
            'Radio - Triple J': 'https://www.abc.net.au/triplej/',
            'Games - MetaCritic': 'https://www.metacritic.com/browse/games/release-date/new-releases/all/date',
            'Theatre - The Tivoli': 'https://www.tivoli.com/events'
        }
        url = url_mapping.get(selected_option, '')
        
        #open url in web browser
        if url:
            webbrowser.open(url)

    except Exception as error:
        show_error_message(f"An error occurred while trying to open the webpage:\n{error}")
    






#Summary Button
Show_Summary = Button(options_frame, text="Show Summary", command=SummaryButtonOnclick)
Show_Summary.config(bg='#DEDED7')
Show_Summary.grid(row=0, column=1, pady=10)

#detail button
Show_Details = Button(options_frame, text="Show Details", command=DetailButtonOnClick)
Show_Details.config(bg='#DEDED7')
Show_Details.grid(row=2, column=1, pady=10)

#position the LabelFrame inside the main window
options_frame.grid(row=1, column=0)


#create listbox with frame as parent
menuOptions_frame = LabelFrame(task_2_main_window, font=("Arial", 14), text="Rating", padx=40, pady=40)
menuOptions_frame.grid(row=1, column=1, padx=10, pady=10)
menuOptions_frame.config(bg='#DEDED7')
selected = StringVar()
menuOptionsList = ["1 Star", "2 Star", "3 Star", "4 Star", "5 Star"]
menuOptions = OptionMenu(menuOptions_frame, selected, *menuOptionsList)
selected.set("Choose Rating")
menuOptions.config(bg='#DEDED7')
menuOptions.pack()
number_of_stars = Label()


#button selection of enter for database
def on_button_click_enter_enter():
    try:
        selected_option = RadioButtonSelection.get()
        if selected_option == " ":
            show_error_message("Please select an entertainment option.")
            return

        rating = selected.get()
        if rating == "Choose Rating":
            show_error_message("Please choose a rating.")
            return
        
        #connect to databse
        conn = sqlite3.connect('Assignment-2\media_reviews.db')
        cursor = conn.cursor()
        summary = Summary_Button_Text
        
        #set url based on whats selected (inside the function)
        url_mapping = {
            'Radio - Triple J': 'https://www.abc.net.au/triplej/',
            'Theatre - The Tivoli': 'https://www.tivoli.com/events',
            'Games - MetaCritic': 'https://www.metacritic.com/browse/games/release-date/new-releases/all/date'
        }
        url = url_mapping.get(selected_option, '')

        #insert into database
        cursor.execute("INSERT INTO reviews (review, event_source, event_summary, url) VALUES (?, ?, ?, ?)",
                       (rating, selected_option, summary, url))

        conn.commit()
        conn.close()

    except sqlite3.Error as error:
        show_error_message(f"An error occurred while accessing the database:\n{error}")
    except Exception as error:
        show_error_message(f"An unexpected error occurred:\n{error}")

#button selection
confirm_selection = Button(menuOptions_frame, text="Enter", command=on_button_click_enter_enter)
confirm_selection.config(bg='#DEDED7')
confirm_selection.pack()

#insert image
image_frame = LabelFrame(task_2_main_window)

#variable for photo so it's easy to change
photo = PhotoImage(file="Assignment-2\images\WillsReviews.png")

#image on far right
image_label = Label(image_frame, image = photo)
image_label.grid(row = 0, column = 0, rowspan = 2)
image_frame.grid(row = 0, column = 2, rowspan = 2)


def url_to_filename(url):
    #remove the http and "www" prefix if present
    cleaned_url = url.replace("https://", "").replace("http://", "").replace("www.", "")

    #replace invalid characters with underscores
    filename = re.sub(r"[^\w\d.]+", "_", cleaned_url)

    return filename

#definition to open file, read file, search file for "Fact" (thing in between start and end position)
def search_file(filename, target_directory, start_code, end_code):
    try:
        #Combine directory name, filename and extension
        file_path = target_directory + '/' + filename + '.html'
        text_file = open(file_path, 'r', encoding='utf-8')
        contents = text_file.read()
        text_file.close()
        start_spot = contents.find(start_code)
        if start_spot != -1:
            end_spot = contents.find(end_code, start_spot)
            global Fact
            Fact = (contents[start_spot + len(start_code):end_spot])
    except FileNotFoundError as error:
        show_error_message(f"File not found:\n{error}")
    except Exception as error:
        show_error_message(f"An unexpected error occurred:\n{error}")

#URL for Triple J
url = 'https://www.abc.net.au/triplej/featured-music'
filename = url_to_filename(url)

#For triple J title
start_code = '<span class="KeyboardFocus_keyboardFocus__uwAUh" data-component="KeyboardFocus">'
end_code = '</span>'
download(url, target_filename=filename, target_directory='Assignment-2')
search_file(filename, 'Assignment-2', start_code, end_code)
TripleJTitle = Fact

#For triple J author
start_code = '<p class="Typography_base__k7c9F TracklistCard_secondaryTitle__e1gyh Typography_sizeMobile16__Wygfe Typography_lineHeightMobile24__xwyV0 Typography_regular__Aqp4p Typography_colourInherit__xnbjy" data-component="Text">'
end_code = '</p>'
download(url, target_filename=filename, target_directory='Assignment-2')
search_file(filename, 'Assignment-2', start_code, end_code)
TripleJAuthor = Fact


#The Tivoli Title
url = 'https://thetivoli.com.au/events'
filename = url_to_filename(url)

#The Tivoli Name
start_code = '<div class="image-title">'

end_code = '</div>'
download(url, target_filename=filename, target_directory='Assignment-2')
search_file(filename, 'Assignment-2', start_code, end_code)
TheTivoliName = Fact

# The Tivoli Nationality
start_code = '<div class="image-nationality font-trim-light">'
end_code = '</div'
download(url, target_filename=filename, target_directory='Assignment-2')
search_file(filename, 'Assignment-2', start_code, end_code)
TheTivoliNationality = Fact

#Metacritic URL
url = 'https://www.metacritic.com/browse/games/release-date/new-releases/all/date'
filename = url_to_filename(url)

#Metacritic Title
start_code = 'class="title"><h3>'
end_code = '</h3'
download(url, target_filename=filename, target_directory='Assignment-2')
search_file(filename, 'Assignment-2', start_code, end_code)
metacriticAuthor = Fact

#Metacritic Author
start_code = '<span>'
end_code = '</span>'

download(url, target_filename=filename, target_directory='Assignment-2')
search_file(filename, 'Assignment-2', start_code, end_code)
metacriticTitle = Fact

task_2_main_window.mainloop()


