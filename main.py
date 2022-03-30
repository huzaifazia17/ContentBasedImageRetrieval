from operator import itemgetter
from PIL import Image
import PIL
from matplotlib.pyplot import axis
import numpy as np
import os
import time
# Assuming all images are of the same size in the directory

# Declaration of all variables
imagesRGB = []
pixelImages = []
imagesDic = {}
counter = 0
imageCounter = 0
p1 = []
p2 = []
p3 = []
p4 = []
p1C = []
p2C = []
p3C = []
p4C = []
diagonal = []
sumPosOffset = []
sumNegOffset = []
sumDiagonal = []
sumPosOffsetP4 = []
sumNegOffsetP4 = []
sumDiagonalP4 = []
sumP1 = []
sumP3 = []
barcodes = []
barcodesDic = {}


cwd = os.getcwd()
MNIST_path = os.path.join(cwd, 'MNIST_DS')
classes = os.listdir(MNIST_path)


# loop through num (1-10) and save all image names into image files
for c in classes:
    images_dir = os.path.join(MNIST_path, c)
    image_files = os.listdir(images_dir)
    for f in image_files:  # Go through each class of image and convert it into a pixelated array
        fullImagePath = images_dir + '\\' + f
        ImagesAsArray = np.asarray(PIL.Image.open(fullImagePath))
        listImages = np.array(ImagesAsArray).tolist()
        pixelImages.append(listImages)

# Store all images into a dictionary with a key
# Key : {Image Class(0-9): Image Number (0-9)}

for k in pixelImages:
    if (counter % 10 == 0):
        imageCounter += 1
        counter = 0
    mainCounter = "{}:{}".format(imageCounter-1, counter)
    imagesDic[mainCounter] = k
    counter += 1

imageCounter = 0
counter = 0
mainCounter = 0

# Function to find average


def average(l):
    return sum(l) / len(l)

# Function to genearate barcode
# Tnis is a function


def generate_c(p):
    c = []
    for item in p:
        if item > average(p):
            c.append(1)
        else:
            c.append(0)
    return c

# # hamming distance
# # The Hamming distance between two equal-length strings of symbols is the number of positions at which the corresponding symbols are different.


def hamming_distance(str1, str2):
    d = 0
    for c1, c2 in zip(str1, str2):  # zip() Iterate over several iterables in parallel
        if c1 != c2:
            d = d + 1
    return d


# Print Image as Array
# for key, value in imagesDic.items():
    #print(key, ": ", value, "\n")


# Convert Dictionary of pixelated values to barcode. Find Projections
# For more information on the projections visit the CIBR.txt file
def barcodeGenerate(imagesDic):

    imageCounter = 0
    counter = 0
    mainCounter = 0

    # For every value in dictionary of images pixel values
    for v in imagesDic.values():
        # For length of V
        for i in range(len(v)):
            # Skip last diagonals as well as middle
            if i + 1 < len(v) and i >= 1:
                # Projection 2 diagonal sums
                sumPosOffset.append(sum(np.diagonal(v, i, 0, 1)))
                sumNegOffset.append(sum(np.diagonal(v, -i, 0, 1)))
                # Projection 4 diagonal sums
                sumPosOffsetP4.append(sum(np.diagonal(np.fliplr(v), i, 0, 1)))
                sumNegOffsetP4.append(sum(np.diagonal(np.fliplr(v), -i, 0, 1)))

                # Projection 1 horizontal sum
                sumP1 = list(map(sum, v))
                # Projection 3 vertical sum
                sumP3 = np.sum(v, axis=0)
                sumP3 = sumP3[::-1]

        # Get diagonal Sum for P2 and P4
        sumDiagonal.append(sum(np.diagonal(v, 0, 0, 1)))
        sumDiagonalP4.append(sum(np.diagonal(np.fliplr(v), 0, 0, 1)))
        # Reverse the sum to get values in proper order
        sumPosOffset.reverse()
        sumNegOffsetP4.reverse()

        # Set projections
        p1 = sumP1
        p2 = sumPosOffset+sumDiagonal+sumNegOffset
        p3 = sumP3
        p4 = sumNegOffsetP4+sumDiagonalP4+sumPosOffsetP4

        # Generate Barcodes
        p1C = generate_c(p1)
        p2C = generate_c(p2)
        p3C = generate_c(p3)
        p4C = generate_c(p4)
        barcodes = p1C+p2C+p3C + p4C

        # Store all barcodes into a dictionary with key
        if (counter % 10 == 0):
            imageCounter += 1
            counter = 0
        mainCounter = "{}:{}".format(imageCounter-1, counter)
        barcodesDic[mainCounter] = barcodes
        counter += 1

        # Clear All lists
        sumPosOffset.clear()
        sumDiagonal.clear()
        sumNegOffset.clear()
        sumPosOffsetP4.clear()
        sumDiagonalP4.clear()
        sumNegOffsetP4.clear()
        sumP1.clear()
    return barcodesDic


print("\nWelcome to a small scale Content-Based Image Retrieval Using Barcode Proram")
print("This program does the following:")
print("1. There are a list of 100, 28 x 28 pixel Images. 10 each from Numbers 1-9")
print("2. This program first goes through all Images and converts it into a pixelated array using Pillow, a python library")
print("3. Then using the Barcode funtion the program goes through each pixelated array and creates four projections")
print("\t A. The First projection is a horizontal sum of each row")
print("\t B. The Second projection is the sum from each of the positive offset diagonals ")
print("\t C. The Third projection is a vertical sum of each column")
print("\t D. The Fourth projection is the sum from each of the negative offset diagonals ")
print("4. The projection are then converted into barcodes by calculating the threshold values and stored into a Dictionary")
print("5. The final part of this program implements a search function which you may use to test the accuracy of this program")
print("\nBARCODES ARE BEING GENERATED\n")


# runtime test of Barcode generator function
start = time.time()
# Store barcodes into a dictionary
barcodesDic = barcodeGenerate(imagesDic)
end = time.time()

# Store barcodes into a file
with open('Barcodes.txt', 'w') as f:
    f.truncate(0)
    for key, value in barcodesDic.items():
        # f.write(key, ": ", value, "\n")
        f.write(str(key))
        f.write(":")
        f.write(str(value))
        f.write("\n\n")

# Close file
f.close()

imageClass = 0
imageNum = 0

# Outputs, Ask user to enter Image Class and Number

print("BARCODES HAVE BEEN GENERATED:\n")
print("Barcodes with keys have been stored into Barcodes.txt\n")
print("Which Image would you like to use a query image to test accuracy of this program:\n")

imageClass = input("Choose Image Number from 0-9: ")
while int(imageClass) < 0 or int(imageClass) > 9:
    imageClass = input("Choose Image Number from 0-9: ")

imageNum = input("Choose a random image of number from 0-9: ")
while int(imageNum) < 0 or int(imageNum) > 9:
    imageNum = input("Choose Image Number from 0-9: ")

key = "{}:{}".format(imageClass, imageNum)

# Function to Search for Similar Images


def imageSearch(key, barcodesDic):

    hammingDistances = {}
    K = 10
    # Copy Dictionary and remove image to be searched
    searchDic = barcodesDic.copy()
    queryImage = barcodesDic[key]
    # Get key and class of Image to be searched
    queryImageClass = key
    queryImageClass = queryImageClass[0]
    hit = 0
    retrvAccuracy = 0

    # Delete query image from dictionary
    del searchDic[key]

    # Convert query image barcode values into sunsequent seperate strings to compare
    string_c1 = [str(n) for n in queryImage]

    # Comapre with each value in dictionary
    for k, v in searchDic.items():
        # Convert test image barcode values into sunsequent seperate strings to compare
        string_c2 = [str(n) for n in v]
        # Use hamming distance to find distance between subsequent 0 and 1 bits
        hammingDistances[k] = hamming_distance(
            ''.join(string_c1), ''.join(string_c2))

    # Return and store keys and values of 10 images with the least hamming distance
    similarImages = dict(
        sorted(hammingDistances.items(), key=itemgetter(1))[:K])

    # print(str(similarImages))

    # Calculate how many hits there were by comparing keys of similarImages and query image class
    for k, v in similarImages.items():
        imageClass = k[0]
        if queryImageClass == imageClass:
            hit += 1

    # Calculate retrieval accuracy
    retrvAccuracy = hit/K * 100

    # for key, value in hammingDistances.items():
    #print(key, ": ", value, "\n")

    return retrvAccuracy


# Find accuracy of image search
accuracy = imageSearch(key, barcodesDic)

print("\nThe retrieval accuracy of ", imageClass,
      ":", imageNum, " is: ", accuracy, "%")

total = end - start
# print(total)
