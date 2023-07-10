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