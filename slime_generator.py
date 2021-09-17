import glob
from itertools import product
from util import overlay_image_alpha
import cv2
import numpy as np
import json

COMPONENTS_DIR = 'data/components'
COLORS_DIR = 'data/colors'
OUTPUT_DIR = 'output'

data = dict()
uncolored_components_dict = dict()
for i, components_folder in enumerate(glob.iglob(f'{COMPONENTS_DIR}/*', recursive=False)):
    key = components_folder.split('/')[-1]
    uncolored_components_dict[key] = []
    for j, component in enumerate(glob.iglob(f'{components_folder}/*')):
        image = cv2.imread(component, flags=cv2.IMREAD_UNCHANGED)
        key = component.split('/')[-2]
        metadata = [component.split('/')[-1].split('.')[0].split('_')[-1]]
        image_with_metadata = image, metadata
        uncolored_components_dict[key].append(image_with_metadata)
        # if np.sum(image[:, :, 3]) == 0:
        #     image_with_metadata = image, metadata
        #     colored_components_dict[key].append(image_with_metadata)
        #     continue

        # for c, color in enumerate(glob.glob(f'{COLORS_DIR}/*')):
        # color_image = cv2.imread(color, flags=cv2.IMREAD_UNCHANGED)
        # color_image = cv2.cvtColor(color_image, cv2.COLOR_BGR2BGRA)
        
        # color = list(np.random.choice(range(256), size=3))
        # color_image = np.zeros_like(image)
        # color_image[:, :, :3] = color
        # color_image[:, :, 3] = 255
        # new_image = cv2.addWeighted(image, 0.5, color_image, 0.5, 0)
        # new_image[image <= 10] = image[image <= 10]
        # key = component.split('/')[-2]
        # image_with_metadata = new_image, metadata
        # colored_components_dict[key].append(image_with_metadata)

for key in uncolored_components_dict.keys():
    print(key, len(uncolored_components_dict[key][0]))

for i, uncolored_components_with_meta in enumerate(product(*(iter(uncolored_components_dict[key]) for key in uncolored_components_dict.keys()))):
    final_metadata = []
    color = list(np.random.choice(range(256), size=3))
    color_image = np.zeros_like(image)
    color_image[:, :, :3] = color
    color_image[:, :, 3] = 255
    final_image = color_image
    for j, uncolored_component_with_meta in enumerate(uncolored_components_with_meta):
        uncolored_component, metadata = uncolored_component_with_meta
        final_metadata.append(metadata)
        # color component
        color = list(np.random.choice(range(256), size=3))
        color_image = np.zeros_like(image)
        color_image[:, :, :3] = color
        color_image[:, :, 3] = 255
        colored_component = cv2.addWeighted(uncolored_component, 0.5, color_image, 0.5, 0)
        colored_component[uncolored_component <= 10] = uncolored_component[uncolored_component <= 10]

        alpha_mask = colored_component[:, :, 3] / 255.0
        final_image = overlay_image_alpha(final_image, colored_component, 0, 0, alpha_mask)
    cv2.imwrite(f'{OUTPUT_DIR}/{i}.png', final_image)
    data[i] = final_metadata

generation = 1
with open(f'generation_{generation}.json', 'w') as f:
    json.dump(data, f)