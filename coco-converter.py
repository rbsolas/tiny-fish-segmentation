from config import *

from sahi.utils.coco import Coco, CocoCategory, CocoImage, CocoAnnotation
from sahi.utils.file import save_json
from PIL import Image
import glob, re
import json

coco = Coco()
for i in range(2):  # Category id = 0 should be supercategory (i.e. 'underwater-objects')
    coco.add_category(CocoCategory(id=i, name=CATEGORIES[i], supercategory=(CATEGORIES[0] if i > 0 else "none")))

# For each image, create a COCO image
# Add annotations to COCO image
# Add annotated COCO image object to COCO object
# After all images are added, export COCO object to JSON
i = 0
split=['train', 'test', 'val']
for annot_file in [TRAIN_LABELS_PATH, TEST_LABELS_PATH, VAL_LABELS_PATH]:
    with open(annot_file, 'r') as file:
        data = json.load(file)

    for img in data:
        coco_img = CocoImage(file_name=img['filename'], width=img['width'], height=img['height'])
        
        for annot in img['annotations']:
            # Has bbox and category id
            coco_img.add_annotation(
                CocoAnnotation(
                bbox=annot['bbox'],
                category_id=annot['category_id'] + 1, # Category 0 should be 'underwater-objects'
                category_name=CATEGORIES[annot['category_id'] + 1]
                )
            )
        
        coco.add_image(coco_img)

    save_path = COCO_JSON_OUTPUT_PATH + f'/{split[i]}/{split[i]}_labels.json'
    save_json(data=coco.json, save_path=save_path)
    file.close()

    with open(save_path, 'r+') as file:
        data = json.load(file)
        data['info'] = {"year":"2025",
                "version":"1",
                "description":"Made with SAHO COCO utilities",
                "contributor":"",
                "url":"https://public.roboflow.com/object-detection/undefined",
                "date_created":"2025-04-18T09:57:28+00:00"}
        data['licenses'] = [{"id":1,"url":"https://creativecommons.org/licenses/by/4.0/","name":"CC BY 4.0"}]
        # print("Number of keys: " + len(data))
        file.seek(0)

        json.dump(data, file)
    
    file.close()
    
    print("Output saved at: " + save_path)
    i += 1

# for file in sorted(glob.glob(DATASET_PATH + '/*/*/*.jpg')):
#     print(file)
#     width, height = Image.open(file).size
#     img = CocoImage(file_name= file.split('/')[-1], width=width, height=height)

#     print(f"{width}, {height}")