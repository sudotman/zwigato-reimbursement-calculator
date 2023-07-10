import tkinter as tk
from tkinter import filedialog
import easyocr
from PIL import Image
import datetime
import calendar
import threading
from tkinter.ttk import Progressbar

selected_files = []  # Global list to store the selected files

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
    progress_label.config(text="Running...")
    progress_bar.start(10)

    # progress_bar["maximum"] = 50  # Set the maximum value for the progress bar
    # progress_bar["value"] = 0  # Reset the progress bar value
    # progress_bar.step(5)
    update_gui()  # Update the GUI

    def program_thread():
        print(*selected_files, sep="\n")

        reader = easyocr.Reader(['en', 'hi'])

        results_normal = []

        for file in selected_files:
            results_normal.append(reader.readtext(str(file)))

        # progress_bar.step(5)  # Increment progress by 5
        update_gui()  # Update the GUI

        totalAmounts = []

        def return_back_last_rupee(list_of_files):
            matches = []

            for index, different_file in enumerate(list_of_files):
                for match_contents in different_file:
                    if 'र' in match_contents[1]:
                        matches.append(match_contents[1])

                if matches:
                    totalAmounts.append(matches[-1])
                    print(totalAmounts)

                matches = []

                if index % 10 == 0:  # Update progress bar at every 10th iteration
                    # progress_bar.step(10 / len(list_of_files))  # Increment progress
                    update_gui()  # Update the GUI

            update_gui()  # Update the GUI

        return_back_last_rupee(results_normal)

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

        converted_to_english_numeral_amounts = []

        for numbers in totalAmounts:
            for hindi_num, english_num in hindi_to_english.items():
                numbers = numbers.replace(hindi_num, english_num)

            converted_to_english_numeral_amounts.append(numbers)

        totalAmounts = converted_to_english_numeral_amounts

        total = 0.0
        for amount in totalAmounts:
            num_without_rupee = amount[1:]  # Remove the first character (rupee symbol)
            total += float(num_without_rupee)

        with open('Reimbursement.txt', 'w', encoding="utf-8") as f:
            f.write('Total Reimbursement amount in chronological order: ')
            f.write('\n')
            f.write('\n')
            for line in totalAmounts:
                f.write(line)
                f.write('\n')

            f.write('\n')
            f.write('Total Amount: ')
            f.write(str(total))

        # progress_bar.step(2.5)  # Increment progress by 2.5
        update_gui()  # Update the GUI

        current_date = datetime.date.today()
        previous_month = current_date.month - 1 if current_date.month > 1 else 12

        month_name = calendar.month_name[previous_month]

        images = []
        for file in selected_files:
            images.append(Image.open(file))

        pdf_path = "Reimbursement_" + month_name + ".pdf"

        images[0].save(
            pdf_path, "PDF", resolution=100.0, save_all=True, append_images=images[1:]
        )

        # progress_bar.step(2.5)  # Increment progress by 2.5
        update_gui()  # Update the GUI

        progress_bar.stop()  # Stop the progress bar
        progress_label.config(text="Completed!")

    thread = threading.Thread(target=program_thread)
    thread.start()

def update_gui():
    window.update()
    window.update_idletasks()

# Create the main window
window = tk.Tk()
window.title("File Selection")
window.geometry("300x200")

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

# Start the GUI event loop
window.mainloop()
