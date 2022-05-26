# ContentBasedImageRetrieval
Welcome to a small scale Content-Based Image Retrieval Using Barcode Proram
This program does the following:
1. There are a list of 100, 28 x 28 pixel Images. 10 each from Numbers 1-9
2. This program first goes through all Images and converts it into a pixelated array using Pillow, a python library
3. Then using the Barcode funtion the program goes through each pixelated array and creates five projections
A. The First projection is a horizontal sum of each row
B. The Second projection is the sum from each of the positive offset diagonals 
C. The Third projection is a vertical sum of each column
D. The Fourth projection is the sum from each of the negative offset diagonals 
D. The Fifth projection is the sum of each reverse horizontal 
4. The projection are then converted into barcodes by calculating the threshold values and stored into a Dictionary
5. The final part of this program implements a search function which you may use to test the accuracy of this program

## Files

The program is done in two ways of calculating accuracy. The first is a ten key method, which takes the 10 most similar hamming distance from each search and calculates the accuracy as such.
The second method is the one key method, which only finds the most similar hamming distance and then calculates the accuracy.

To view the Ten Key method visit the MainTenKeySearch[https://github.com/huzaifazia17/ContentBasedImageRetrieval/blob/main/MainTenKeySearch.py] file
To view the One Key method visit the MainOneKeySearch[https://github.com/huzaifazia17/ContentBasedImageRetrieval/blob/main/MainOneKeySearch.py] file

To view the overall accuracy of each program visit the respective Test Driver files. 

For more in-dpeth information please read the Project Report[https://github.com/huzaifazia17/ContentBasedImageRetrieval/blob/main/CBIR-Report.pdf]