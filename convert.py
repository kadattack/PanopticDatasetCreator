import cv2
import os

from PanopticCocoCreator import createPanopticVal, createPanopticInstances, addSignleAnnotationToPanAnnotations, \
    addSignleImagesAnnotation, addSignleAnnotationToInstaAnnotations, addColorToRgbArray, createPolyFromSubmask, \
    createSegments_info, calculateAreaFromSubmask, createBBoxFromSubmask, createAllCategoryAnnotations, \
    convertGrayscaleToRgbArray, createSubmaskByColor
from config_creator import createConfig

FILE_COLOR_SCHEME = {}


def test_config(config_data):
    output_folder = config_data["cfg"]["json_output_folder"]
    images_folder = config_data["cfg"]["images_folder"]
    mask_folder = config_data["cfg"]["masks_folder"]
    class_list = config_data["classes"]
    mask_type = config_data["cfg"]["masks_channels"].lower()
    assert os.path.exists(output_folder)
    assert os.path.exists(mask_folder)
    assert os.path.exists(images_folder)
    assert (mask_type == "grayscale" or mask_type == "rgb")
    assert type(class_list) == list
    for clas in class_list:
        assert "color" in clas
        assert "isthing" in clas
        assert "iscrowd" in clas
        assert "id" in clas
        assert "name" in clas


def printPercDone(per_index, counter, filelist):
    percent_set = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1, 1.1]
    if percent_set[per_index] < counter / len(filelist) < percent_set[per_index + 1]:
        print("Done " + str(int(percent_set[per_index] * 100)) + "%")
        per_index += 1
    return per_index


def annotateFromMasks(config_data):
    test_config(config_data)
    output_folder = config_data["cfg"]["json_output_folder"]
    binary_mask_folder = config_data["cfg"]["masks_folder"]
    masks_file_type = config_data["cfg"]["masks_file_type"]
    images_file_type = config_data["cfg"]["images_file_type"]
    mask_type = config_data["cfg"]["masks_channels"].lower()
    if mask_type == "grayscale":
        classes_dict = config_data["classes"]
    else:
        classes_dict = config_data["classes_rgb"]

    filelist = os.listdir(binary_mask_folder)

    per_index = 0
    images = []
    categories = createAllCategoryAnnotations(classes_dict)
    pan_annotations = []
    insta_annotations = []
    insta_id = 0
    counter = 0

    for maskfile in filelist:
        filetype = maskfile.split(".")[1]
        if masks_file_type == filetype:

            # Print % done
            per_index = printPercDone(per_index, counter, filelist)

            counter += 1
            segments_info = []
            maskarray = None
            rgbArray = None

            if mask_type == "grayscale":
                maskarray = cv2.imread(binary_mask_folder + maskfile, cv2.IMREAD_GRAYSCALE)
                rgbArray = convertGrayscaleToRgbArray(maskfile, binary_mask_folder)

            if mask_type == "rgb":
                maskarray = cv2.imread(binary_mask_folder + maskfile, cv2.IMREAD_COLOR)
                maskarray = cv2.cvtColor(maskarray, cv2.COLOR_BGR2RGB)

            colors = []
            for classes in classes_dict:
                [colors.append(c) for c in classes["color"]]

            for color in colors:
                if mask_type == "grayscale":
                    colorfound = len(maskarray[maskarray == color]) != 0
                else:
                    colorfound = color[0] in maskarray[:, :, 0] and color[1] in maskarray[:, :, 1] and color[
                        2] in maskarray[:, :, 2]

                if colorfound:
                    submask = createSubmaskByColor(maskarray, color, mask_type)
                    bbox_array = createBBoxFromSubmask(submask)

                    poly_area = calculateAreaFromSubmask(submask)
                    segments_info, rgb, category_id, iscrowd = createSegments_info(segments_info,
                                                                                   poly_area,
                                                                                   bbox_array,
                                                                                   classes_dict,
                                                                                   color
                                                                                   )
                    poly_array = createPolyFromSubmask(submask, iscrowd)
                    insta_annotations = addSignleAnnotationToInstaAnnotations(insta_id, category_id,
                                                                              insta_annotations, bbox_array,
                                                                              poly_array, poly_area, counter, iscrowd
                                                                              )
                    insta_id += 1

                    if mask_type == "grayscale":
                        rgbArray = addColorToRgbArray(rgbArray, rgb, color)

            if mask_type == "grayscale":
                rgbArray = cv2.cvtColor(rgbArray, cv2.COLOR_BGR2RGB)
                rgb_mask_output = config_data["cfg"]["rgb_mask_output"]
                assert os.path.exists(rgb_mask_output)
                cv2.imwrite(os.path.join(rgb_mask_output, maskfile), rgbArray)

            pan_annotations = addSignleAnnotationToPanAnnotations(maskfile, pan_annotations, segments_info, counter)
            images = addSignleImagesAnnotation(maskfile, maskarray, images, counter, images_file_type)

    createPanopticVal(images, categories, pan_annotations, output_folder)
    createPanopticInstances(images, categories, insta_annotations, output_folder)


def main():
    config_data = createConfig()
    annotateFromMasks(config_data)


if __name__ == '__main__':
    main()
