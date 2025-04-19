from config import *

import sys, argparse, json
from datetime import datetime
from sahi.utils.coco import Coco, CocoCategory, CocoImage, CocoAnnotation
from sahi.utils.file import save_json
from PIL import Image

'''
Converts Detectron2 .json annotations (generated c/o of hoalarious on Github) to COCO .json format. Make sure that the dataset is structured as follows:
    dataset_root/
        train/
            ...images...
        test/
            ...images...
        valid/
            ...images...    
'''

options = "yvdcut"
long_options = ["year", "version", "description", "contributor",
                "url", "time_created"]
assert len(options) == len(long_options)
defaults = {'year': datetime.today().strftime('%Y'),
            'version': 1,
            'description': "Made with SAHI COCO utilities",
            'contributor': "",
            'url': "https://public.roboflow.com/",
            'time_created': datetime.today().strftime('%Y-%m-%d %H:%M:%S')}

parser = argparse.ArgumentParser()
for i in range(len(options)):
    parser.add_argument(f"-{options[i]}", f"--{long_options[i]}", default=defaults[long_options[i]])

args = parser.parse_args()

coco = Coco()
for i in range(2):  # Category id = 0 should be supercategory (i.e. 'underwater-objects')
    coco.add_category(CocoCategory(id=i, name=CATEGORIES[i], supercategory=(CATEGORIES[0] if i > 0 else "none")))

# For each image, create a COCO image
# Add annotations to COCO image
# Add annotated COCO image object to COCO object
# After all images are added, export COCO object to JSON
i = 0
split=['train', 'test', 'valid']
for annot_file in [DETECTRON_2_TRAIN_LABELS_PATH, DETECTRON_2_TEST_LABELS_PATH, DETECTRON_2_VAL_LABELS_PATH]:
    with open(annot_file, 'r') as file:
        data = json.load(file)

    for img in data:
        coco_img = CocoImage(file_name=img['filename'], width=img['width'], height=img['height'])
        
        for annot in img['annotations']:
            # Has bbox and category id
            coco_img.add_annotation(
                CocoAnnotation(
                # From [x1, y1, x2, y2] to [x, y, width height] 
                bbox=[annot['bbox'][0], annot['bbox'][1], 
                      annot['bbox'][2] - annot['bbox'][0], 
                      annot['bbox'][3] - annot['bbox'][1]],
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
        data['info'] = {"year":args.year,
                "version":args.version,
                "description":args.description,
                "contributor":args.contributor,
                "url":args.url,
                "date_created":args.time_created}
        data['licenses'] = [{"id":1,"url":"https://creativecommons.org/licenses/by/4.0/","name":"CC BY 4.0"}]
        file.seek(0)

        json.dump(data, file)
    
    file.close()
    
    print("Output saved at: " + save_path)
    i += 1