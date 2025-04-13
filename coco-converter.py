from config import *

from sahi.utils.coco import Coco, CocoCategory, CocoImage, CocoAnnotation
from sahi.utils.file import save_json
from PIL import Image
import glob, re

coco = Coco()
coco.add_category(CocoCategory(id=0, name='fish'))

# For each image, create a COCO image
# Add annotations to COCO image
# Add annotated COCO image object to COCO object
# After all images are added, export COCO object to JSON

for file in sorted(glob.glob(DATASET_PATH + '/*/*/*.jpg')):
    print(file)
    width, height = Image.open(file).size
    img = CocoImage(file_name= file.split('/')[-1], width=width, height=height)

    print(f"{width}, {height}")


if __name__ == "__main__":
    pass