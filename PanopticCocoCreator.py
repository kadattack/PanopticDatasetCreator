import os
import random
import numpy as np
import cv2.cv2 as cv2
from pycocotools import _mask as pmask
from pycocotools import mask
from imantics import Mask
import json

FILE_COLOR_SCHEME={}



def convertGrayscaleToRgbArray(maskfile, dir):
    image = cv2.imread(dir + maskfile, cv2.IMREAD_GRAYSCALE)
    backtorgb = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
    return backtorgb

def addColorToRgbArray(rgbArray, rgb, color):
    rgbArray[np.all(rgbArray == (color, color, color), axis=2), :] = rgb
    return rgbArray


def generateColorForImage(color):
    looking_for_color = True
    r,g,b = 0,0,0
    if color in FILE_COLOR_SCHEME:
        return FILE_COLOR_SCHEME[color]
    else:
        while looking_for_color:
            looking_for_color = False
            r = random.randint(0, 255)
            g = random.randint(0, 255)
            b = random.randint(0, 255)
            for key in FILE_COLOR_SCHEME:
                if FILE_COLOR_SCHEME[key] == (r,g,b):
                    looking_for_color = True
        FILE_COLOR_SCHEME[color] = (r,g,b)
        return (r,g,b)




def calculateAreaFromSubmask(submask):
    return len(submask[submask == 255])


def createPolyFromSubmask(submask, iscrowd):
    if iscrowd == 1:
        rle = {'counts': [], 'size': list(submask.shape)}
        counts = rle.get('counts')
        last_elem = 0
        running_length = 0
        for i, elem in enumerate(submask.ravel(order='F')):
            if elem == last_elem:
                pass
            else:
                counts.append(running_length)
                running_length = 0
                last_elem = elem
            running_length += 1
        counts.append(running_length)
        return rle

    polygons = Mask(submask).polygons()
    list_of_shapes = []
    for shape in polygons.polygons:
        list_of_shapes.append(shape.tolist())
    return list_of_shapes


def createBBoxFromSubmask(submask):
    # Submask should contain only values 0 and 255, for a single segment. 255 is mask. 0 is nothingness.
    encoded = mask.encode(np.asfortranarray(submask))
    return pmask.toBbox(encoded)[0]


def createSubmaskByColor(maskarray, value, mask_type):
    submask = np.zeros((maskarray.shape[0],maskarray.shape[1],1), dtype=np.uint8)
    if mask_type.lower() == "grayscale":
        submask[maskarray == value] = 255
    elif mask_type.lower() == "rgb":
        submask[np.where(np.all(maskarray == value, axis=2))] = 255
    return submask


def addSignleImagesAnnotation(maskfile, maskarray, images, imageid, image_file_type):
    image = {
        "height": maskarray.shape[0],
        "width": maskarray.shape[1],
        "id": imageid,
        "file_name": maskfile.split(".")[0] + image_file_type
    }
    images.append(image)
    return images


def createAllCategoryAnnotations(category_list):
    categories = []
    for category_mask in category_list:
        categories.append(
            {
                "supercategory": category_mask["name"],
                "isthing": category_mask["isthing"],
                "id": category_mask["id"],
                "name": category_mask["name"]
            }
        )
    return categories


def createSegments_info(segments_info, poly_area, bbox_array, category_list, color):
    category_id = 0
    iscrowd = 0
    for item in category_list:
        for c in item["color"]:
            if c == color:
                category_id = item["id"]
                iscrowd = item["iscrowd"]
    if type(color) is int:
        color = generateColorForImage(color)
    ids = color[0] + (color[1] * 256) + (color[2] * (256 ** 2))
    segments_info.append(
        {
            "id": ids,
            "category_id": category_id,
            "iscrowd": iscrowd,
            "bbox": [
                int(bbox_array[0]),
                int(bbox_array[1]),
                int(bbox_array[2]),
                int(bbox_array[3])
            ],
            "area": poly_area
        }
    )
    return segments_info, color, category_id, iscrowd


def addSignleAnnotationToPanAnnotations(maskfile, annotations, segments_info, imageid):
    annotations.append(
        {
            "segments_info": segments_info,
            "file_name": maskfile,
            "image_id": imageid
        }
    )
    return annotations


def createPanopticVal(images, categories, pan_annotations, output_folder):
    panoptic = {
        "images": images,
        "annotations": pan_annotations,
        "categories": categories
    }
    panoptic_file = open(output_folder + "panoptic.json", "w+")
    json.dump(panoptic, panoptic_file)


def createPanopticInstances(images, categories, insta_annotations, output_folder):
    panoptic = {
        "images": images,
        "annotations": insta_annotations,
        "categories": categories
    }
    panoptic_file = open(output_folder + "instances.json", "w+")
    json.dump(panoptic, panoptic_file)


def addSignleAnnotationToInstaAnnotations(insta_id, category_id, insta_annotations, bbox_array,
                                          poly_array, poly_area, imageid, iscrowd):
    insta_annotations.append(
        {
            "segmentation": poly_array,
            "area": poly_area,
            "iscrowd": iscrowd,
            "image_id": imageid,
            "bbox": [
                int(bbox_array[0]),
                int(bbox_array[1]),
                int(bbox_array[2]),
                int(bbox_array[3])
            ],
            "category_id": category_id,
            "id": insta_id
        }
    )
    return insta_annotations
