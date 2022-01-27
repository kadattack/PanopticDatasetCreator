
def createConfig():
    config = {}

    # Images and masks, apart from file extensions, need to have the same filename to map them correctly.

    # If masks_channels == "grayscale" then the program will use the rgb_mask_output folder as location to generate RGB masks.
    config["cfg"] = {
        # Folder where there panoptic.json and instances.json will be generated
        "json_output_folder": "d:/Segmentacija/panoptic-deeplab-master/tools_d2/datasets/coco/annotations/",
        # Folder where your images are located
        "images_folder": "d:/Segmentacija/best/train_mastr1325/",
        "images_file_type": "jpg",
        # Folder where your RBG or grayscale panoptic segmentations masks are located
        "masks_folder": "d:/Segmentacija/panoptic-deeplab-master/tools_d2/datasets/coco/panoptic_train/",
        "masks_file_type": "png",
        # What type of masks are you using. "grayscale" or "rgb"
        # "masks_channels": "grayscale",
        "masks_channels": "rgb",
        # If you select "masks_channels": "grayscale" the program will generate RGB masks, along with the json files in this folder.
        "rgb_mask_output": "d:/Segmentacija/panoptic-deeplab-master/tools_d2/datasets/coco/panoptic_train/",
    }

    # Defined classes if masks are "grayscale". If other are selected, this will be ignored.
    config["classes"] = [
        {"color": [0], "isthing": 0, "iscrowd": 0, "id": 1, "name": "obstacles_and_environment"},
        {"color": [1], "isthing": 0, "iscrowd": 0, "id": 2, "name": "water"},
        {"color": [2], "isthing": 0, "iscrowd": 0, "id": 3, "name": "sky"},
        {"color": [4], "isthing": 0, "iscrowd": 0, "id": 4, "name": "ignore"},
        {"color": list(range(10, 30)), "isthing": 1, "iscrowd": 0, "id": 4, "name": "ship_part"},
        {"color": list(range(30, 50)), "isthing": 1, "iscrowd": 0, "id": 5, "name": "boat"},
        {"color": list(range(50, 70)), "isthing": 1, "iscrowd": 0, "id": 6, "name": "buoy"},
        {"color": list(range(70, 90)), "isthing": 1, "iscrowd": 0, "id": 7, "name": "ship"},
        {"color": list(range(90, 110)), "isthing": 1, "iscrowd": 0, "id": 8, "name": "floating_fence"},
        {"color": list(range(110, 130)), "isthing": 1, "iscrowd": 0, "id": 9, "name": "unknown_object"},
        {"color": list(range(130, 150)), "isthing": 1, "iscrowd": 0, "id": 10, "name": "yacht"},
        {"color": list(range(150, 170)), "isthing": 1, "iscrowd": 0, "id": 11, "name": "water_scooter"},
    ]

    # Defined classes if masks are "rgb". If other are selected, this will be ignored.
    config["classes_rgb"] = [
        {"color": [(229, 142, 137)], "isthing": 0, "iscrowd": 1, "id": 1, "name": "obstacles_and_environment"},
        {"color": [(232, 102, 52)], "isthing": 0, "iscrowd": 0, "id": 2, "name": "water"},
        {"color": [(172, 80, 53)], "isthing": 0, "iscrowd": 0, "id": 3, "name": "sky"},
        {"color": [(58, 111, 127)], "isthing": 0, "iscrowd": 0, "id": 4, "name": "ignore"},
        {"color": [(118, 56, 58)], "isthing": 1, "iscrowd": 0, "id": 4, "name": "ship_part"},
        {"color": [(170, 45, 144), (165, 251, 109), (223, 232, 194), (34, 95, 131), (152, 173, 10), (177, 21, 86)],
         "isthing": 1, "iscrowd": 0, "id": 5, "name": "boat"},
        {"color": [(74, 2, 33), (87, 141, 49), (130, 204, 215), (178, 0, 228)], "isthing": 1, "iscrowd": 0, "id": 6,
         "name": "buoy"},
        {"color": [(35, 129, 230), (146, 165, 117), (180, 214, 186), (53, 212, 57), (217, 53, 52), (229, 218, 113)],
         "isthing": 1, "iscrowd": 0, "id": 7, "name": "ship"},
        {"color": [(156, 212, 165)], "isthing": 1, "iscrowd": 0, "id": 8, "name": "floating_fence"},
        {"color": [(216, 196, 88), (68, 202, 21), (12, 240, 141), (45, 35, 200), (170, 99, 89), (212, 74, 124)],
         "isthing": 1, "iscrowd": 0, "id": 9, "name": "unknown_object"},
        {"color": [(61, 180, 128), (233, 237, 186), (157, 246, 221), (109, 7, 252), (201, 204, 179), (210, 89, 19),
                   (26, 240, 209), (137, 29, 92), (203, 53, 98), (86, 250, 74), (218, 65, 84), (6, 202, 29),
                   (52, 112, 87), (133, 128, 14)], "isthing": 1, "iscrowd": 0, "id": 10, "name": "yacht"},
    ]


    return config
