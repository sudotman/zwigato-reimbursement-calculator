from PIL import Image  # install by > python3 -m pip install --upgrade Pillow  # ref. https://pillow.readthedocs.io/en/latest/installation.html#basic-installation

import os

path = os.getcwd()
files = os.listdir(path)
included_extensions = ['jpg','jpeg', 'bmp', 'png', 'gif']
files = [f for f in files if os.path.isfile(path+'/'+f)] #Filtering only the files.
files = [fn for fn in os.listdir(path) if any(fn.endswith(ext) for ext in included_extensions)] #filter out all non image files (i.e non screenshots)
print(*files, sep="\n")

images = []

for file in files:
    images.append(Image.open(file))

pdf_path = "test.pdf"
    
images[0].save(
    pdf_path, "PDF" ,resolution=100.0, save_all=True, append_images=images[1:]
)