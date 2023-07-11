import tkinter as tk
from tkinter import filedialog
import easyocr
from PIL import Image
import datetime
import calendar
import threading
from tkinter.ttk import Progressbar

selected_files = []  # Global list to store the selected files
stop_program = False  # Global flag to indicate if the program should stop

def emptyFun():
    print('Empty')

threadMain = threading.Thread(target=emptyFun)


def select_files():
    global selected_files  # Use the global list to store the selected files
    files = filedialog.askopenfilenames()
    if files:
        print("Selected Files:")
        for file in files:
            selected_files.append(file)  # Add selected files to the list
            print(file)
        progress_label.config(text="Ready")  # Update label to "Ready"
        run_button.config(state=tk.NORMAL)  # Enable the "Run Program" button
    else:
        progress_label.config(text="Waiting for selection of files")  # Update label to "Waiting for selection of files"
        run_button.config(state=tk.DISABLED)  # Disable the "Run Program" button

def run_program():
    global stop_program  # Use the global flag to check if the program should stop
    global threadMain
    progress_label.config(text="Running...")
    progress_bar.config(mode="indeterminate")  # Set the progress bar mode to indeterminate
    progress_bar.start()  # Start the indeterminate progress bar
    run_button.config(state=tk.DISABLED) 

    def program_thread():
        import easyocr
        import os

        path = os.getcwd()
        files = os.listdir(path)
        included_extensions = ['jpg','jpeg', 'bmp', 'png', 'gif']
        files = [f for f in files if os.path.isfile(path+'/'+f)] #Filtering only the files.
        files = [fn for fn in os.listdir(path) if any(fn.endswith(ext) for ext in included_extensions)] #filter out all non image files (i.e non screenshots)
        print(*files, sep="\n")

        reader = easyocr.Reader(['en','hi'])
        # reader_without_hi = easyocr.Reader(['en'])

        results_normal = []
        results_without_hi = []

        target_char = 'र'

        for file in files:
            results_normal.append(reader.readtext(str(file)))


        totalAmounts = []
        def returnBackLastRupee(listOfFiles):
            matches = []

            for differentFile in listOfFiles:
                # print(individualMatches[1])

                for matchContents in differentFile:
                    # print(matchContents[1])

                    if target_char in matchContents[1]:
                        matches.append(matchContents[1])

                totalAmounts.append(matches[-1])
                print(totalAmounts)

                matches=[]
            
                

        returnBackLastRupee(results_normal)

        # Hindi to English dictionary mapping
        hindi_to_english = {
            '०': '0',
            '१': '1',
            '२': '2',
            '३': '3',
            '४': '4',
            '५': '5',
            '६': '6',
            '७': '7',
            '८': '8',
            '९': '9'
        }

        convertedToEnglishNumeralAmounts = []

        for numbers in totalAmounts:
            for hindi_num, english_num in hindi_to_english.items():
                numbers = numbers.replace(hindi_num, english_num)

            convertedToEnglishNumeralAmounts.append(numbers)

        totalAmounts = convertedToEnglishNumeralAmounts

        total = 0.0
        for amount in totalAmounts:
            num_without_rupee = amount[1:]  # Remove the first character (rupee symbol)
            total += float(num_without_rupee)

        with open('Reimbursement.txt', 'w',encoding="utf=8") as f:
            f.write('Total Reimbursement amount in chronological order: ')
            f.write('\n')
            f.write('\n')
            for line in totalAmounts:
                
                f.write(line)
                f.write('\n')

            f.write('\n')
            f.write('Total Amount: ')
            f.write(str(total))


        from PIL import Image  # install by > python3 -m pip install --upgrade Pillow  # ref. https://pillow.readthedocs.io/en/latest/installation.html#basic-installation

        import os

        import datetime
        import calendar

        current_date = datetime.date.today()
        previous_month = current_date.month - 1 if current_date.month > 1 else 12

        month_name = calendar.month_name[previous_month]


        images = []

        for file in files:
            images.append(Image.open(file))


        pdf_path = "Reimbursement_" + month_name + ".pdf"
            
        images[0].save(
            pdf_path, "PDF" ,resolution=100.0, save_all=True, append_images=images[1:]
        )

        progress_bar.stop()  # Stop the indeterminate progress bar
        progress_label.config(text="Completed!")
    

    threadMain = threading.Thread(target=program_thread)
    threadMain.start()

def stop_program():
    global stop_program  # Use the global flag to indicate if the program should stop
    stop_program = False
    resetToStartup()

import sys

def update_gui():
    window.update()
    window.update_idletasks()

def resetToStartup():
    progress_label.config(text="Waiting for selection of files")
    select_files = []
    run_button.config(state=tk.DISABLED)  # Disable the "Run Program" button
    sys.exit("exited main")
    progress_bar.stop()

# Create the main window
window = tk.Tk()
window.title("Reimbursement Tool")
window.geometry("300x250")

# File selection button
select_button = tk.Button(window, text="Select Files", command=select_files)
select_button.pack(pady=20)

# Progress bar and label
progress_label = tk.Label(window, text="Waiting for selection of files")
progress_label.pack()
progress_bar = Progressbar(window, mode="indeterminate")
progress_bar.pack(pady=10)

# Run program button
run_button = tk.Button(window, text="Run Program", command=run_program, state=tk.DISABLED)
run_button.pack(pady=10)

# # Stop program button
# stop_button = tk.Button(window, text="Stop Program", command=stop_program)
# stop_button.pack(pady=5)

# Progress bar and label
description_label = tk.Label(window, text="After pressing run, the seperate thread will\n get processed using your CPU on a seperate thread. \nDon't run multiple instances at once.")
description_label.pack()

# Start the GUI event loop
window.mainloop()
