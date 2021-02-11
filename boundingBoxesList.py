"""
Project: List all bounding boxes of the annotated images.
Author: Rubens de Castro Pereira
Advisor: Dibio Leandro Borges
Date: 10/02/2021
Version: 1.0.0
"""

# Importing needed libraries

import os
import pathlib
import shutil

from random import randrange
from datetime import datetime
from Entity.BoundingBox import BoundingBox
from Entity.ObjectClassEnum import ObjectClassEnum

# ###########################################
# Constants
# ###########################################
LINE_FEED = '\n'


# ###########################################
# Application Methods
# ###########################################


# ###########################################
# Methods of Level 1
# ###########################################


# evaluate detection results
def listBoundingBoxes(inputImagesAnnotationsPath, resultsPathAndFilename, width, height):
    # removing and creating the evaluation file
    if os.path.exists(resultsPathAndFilename):
        os.remove(resultsPathAndFilename)

    # creating the evaluatin results file
    resultsListFile = open(resultsPathAndFilename, 'a+')

    # configuring header
    line = 'image name' \
           + ';class name' \
           + ';width' \
           + ';height' \
           + LINE_FEED

    # write line
    resultsListFile.write(line)

    # close file
    resultsListFile.close()

    for fileName in os.listdir(inputImagesAnnotationsPath):

        # check if file is an image or not
        if fileName.lower().find('jpg') == -1 and fileName.lower().find('jpeg') == -1:
            continue

        # get jpeg position
        jpegPosition = -1
        jpegPosition = fileName.find('jpg')
        if jpegPosition == -1: jpegPosition = fileName.find('jpeg')
        if jpegPosition == -1: jpegPosition = fileName.find('JPG')
        if jpegPosition == -1: jpegPosition = fileName.find('JPEG')

        # get only image name
        imageName = fileName[:jpegPosition - 1]

        # print filename
        print(fileName)

        # saving the annotated data
        processAnnotatedObjectsList(inputImagesAnnotationsPath, imageName, width, height, resultsPathAndFilename)


# ###########################################
# Methods of Level 2
# ###########################################


# getting the list of annotated objects
def processAnnotatedObjectsList(inputImagesAnnotationsPath, imageName, width, height, resultsPathAndFilename):
    # defining the annotated objects list
    annotatedObjectsList = []

    # open annotation file
    imageAnnotationFileName = imageName + ".txt"
    imageAnnotationPathAndFileName = inputImagesAnnotationsPath + imageAnnotationFileName

    # open log detection file
    imageAnnotationFile = open(imageAnnotationPathAndFileName, "r")

    # reading next line
    line = imageAnnotationFile.readline()

    # processing the file
    while line != '':
        # getting the array of values
        values = line.split(' ')

        # get fields of bounding box
        idClass = int(values[0])
        className = ObjectClassEnum.getValueName(idClass)
        colOfCentrePoint = float(values[1])
        linOfCentrePoint = float(values[2])
        heightOfCentrePoint = float(values[3])
        widthOfCentrePoint = float(values[4])

        # calculating the new points of bounding box
        linP1 = colOfCentrePoint
        colP1 = linOfCentrePoint
        linP2 = heightOfCentrePoint
        colP2 = widthOfCentrePoint
        confidence = 0

        # creating a new bounding box instance
        annotatedBoundingBox = BoundingBox(0, 0, 0, 0, '')
        annotatedBoundingBox.setYoloAnnotation(width, height,
                                               colOfCentrePoint, linOfCentrePoint,
                                               widthOfCentrePoint, heightOfCentrePoint,
                                               0,
                                               idClass)

        # saving bounding box
        saveProcessingResult(resultsPathAndFilename, imageName, annotatedBoundingBox)

        # reading next line
        line = imageAnnotationFile.readline()

    # close file
    imageAnnotationFile.close()


# save results of processing
def saveProcessingResult(outputPath, imageName, annotatedBoundingBox):
    # creating the processing results file
    processingResultsFile = open(outputPath, 'a+')

    # setting line to write
    line = imageName + ';' \
           + annotatedBoundingBox.className + ';' \
           + str(annotatedBoundingBox.colPoint2 - annotatedBoundingBox.colPoint1) + ';' \
           + str(annotatedBoundingBox.linPoint2 - annotatedBoundingBox.linPoint1) + ';' \
           + LINE_FEED

    # write line
    processingResultsFile.write(line)

    # closing file
    processingResultsFile.close()


# ###########################################
# Main method
# ###########################################
if __name__ == '__main__':
    # ANNOTATED_IMAGES = 'Detection-22'
    width = 128
    height = 128

    INPUT_IMAGES_ANNOTATIONS_PATH = 'E:/desenvolvimento/projetos/DoctoralProjects/BoundingBoxesListProjectImages/input/'
    OUTPUT_PATH = 'E:/desenvolvimento/projetos/DoctoralProjects/BoundingBoxesListProjectImages/output/'

    # INPUT_IMAGES_DETECTIONS_FULL_PATH = INPUT_ANNOTATED_IMAGES_PATH + ANNOTATED_IMAGES + '/'

    resultsFilename = 'ListOfBoundingBoxes.txt'
    resultsPathAndFilename = OUTPUT_PATH + resultsFilename

    print('List all bounding boxes')
    print('-----------------------')
    print('')
    # print('Input log detection path                 : ', INPUT_ANNOTATED_IMAGES_PATH)
    print('Input images annotations path : ', INPUT_IMAGES_ANNOTATIONS_PATH)
    print('Output results path           : ', OUTPUT_PATH)
    print('')

    # processing the annotated images
    listBoundingBoxes(INPUT_IMAGES_ANNOTATIONS_PATH, resultsPathAndFilename, width, height)

    # end of processing
    print('End of processing')
