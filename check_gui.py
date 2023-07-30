from tkinter import Tk, filedialog, Button, messagebox, Label, Text
from main_script import publish
import openpyxl
import sys
import pandas as pd

openai_api_key = ''
site_url = ''
username = ''
password = ''
content = ''
max_tokens = ''

# Read credentials from config.txt file
try:
    with open('config.txt', 'r') as file:
        lines = file.readlines()
        for line in lines:
            if line.startswith('openai_api_key'):
                openai_api_key = line.split('=')[1].strip()
            elif line.startswith('site_url'):
                site_url = line.split('=')[1].strip()
            elif line.startswith('username'):
                username = line.split('=')[1].strip()
            elif line.startswith('password'):
                password = line.split('=')[1].strip()
            elif line.startswith('max_tokens'):
                max_tokens = int( line.split('=')[1].strip())
except FileNotFoundError:
    print("Config file not found. Please make sure 'config.txt' exists in the same directory as your script.")
    exit(1)
except Exception as e:
    print(f"An error occurred while reading the config file: {str(e)}")
    exit(1)


def select_file():
    global content
    root = Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(filetypes=[('Excel files', '*.xlsx')])
    if file_path:
        content = file_path
        messagebox.showinfo("File Selected", f"Selected file: {content}")


def start_processing():
    if not content:
        messagebox.showerror("Error", "No file selected. Please select an Excel file first.")
        return

    try:
        # Read the XLSX file into a pandas DataFrame
        df = pd.read_excel(content)

        # Get the total number of rows
        total_rows = len(df)

        # Create a text widget to display the processing information
        text_widget = Text(root, width=40, height=14, font=("Arial", 12))
        text_widget.place(relx=0.5, rely=0.40, anchor="center")

        # Iterate through each row in the DataFrame
        for index, row in df.iterrows():
            topic = row['topic'].upper()
            tags = row['tags'].split(',')
            points = row['points']
            slug = row['slug']
            catagory = row['catagory'].split(',')
            status = row['status']

            text_widget.delete("1.0", "end")  # Clear the text widget
            text_widget.insert("end", f"Processing Article {index+1}/{total_rows}\n\n")
            text_widget.update()  # Update the text widget

            try:
                publish(openai_api_key, site_url, username, password, topic, tags, points, slug, catagory, status, max_tokens)
                text_widget.insert("end", "Published Successfully\n\n")
            except Exception as e:
                text_widget.insert("end", f"Error: {str(e)}\n\n")

            text_widget.update()  # Update the text widget

        messagebox.showinfo("Processing Completed", "Processing completed.")

        root.destroy()
        sys.exit()
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while processing the file: {str(e)}")
        sys.exit()

# Create Tkinter root window
root = Tk()
root.geometry("400x400")  # Set window size to 400x400 pixels
root.title("File Processing")
root.configure(bg="#f2f2f2")  # Set window background color

# Create button for file selection
select_button = Button(root, text="Select Excel File", command=select_file, bg="#008080", fg="white", font=("Arial", 14))
select_button.place(relx=0.5, rely=0.4, anchor="center")  # Place button in the middle

# Create button to start processing
start_button = Button(root, text="Start Processing", command=start_processing, bg="#FF4500", fg="white", font=("Arial", 14))
start_button.place(relx=0.5, rely=0.6, anchor="center")  # Place button in the middle

# Create the "Developed by" label
developed_by_label = Label(root, text="Developed by: SSROY (Shuvo Saha Roy)", font=("Arial", 12))
developed_by_label.place(relx=0.5, rely=0.85, anchor="center")

# Create the "Mail Me" label
mail_me_label = Label(root, text="Email: sshuvo548@gmail.com", font=("Arial", 12))
contact_label = Label(root, text="Contact no: 01963102700", font=("Arial", 12))
mail_me_label.place(relx=0.5, rely=0.90, anchor="center")
contact_label.place(relx=0.5, rely=0.95, anchor="center")

root.mainloop()
sys.exit()