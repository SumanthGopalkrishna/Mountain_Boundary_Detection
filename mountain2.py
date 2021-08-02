# !/usr/local/bin/python3
#
# Authors: [PLEASE PUT YOUR NAMES AND USER IDS HERE]
#
# Mountain ridge finder
# Based on skeleton code by D. Crandall, April 2021
#

from PIL import Image
from numpy import *
from scipy.ndimage import filters
import sys
import imageio
import math

# calculate "Edge strength map" of an image
#
def edge_strength(input_image):
    grayscale = array(input_image.convert('L'))
    filtered_y = zeros(grayscale.shape)
    filters.sobel(grayscale, 0, filtered_y)
    return sqrt(filtered_y ** 2)


# draw a "line" on an image (actually just plot the given y-coordinates
#  for each x-coordinate)
# - image is the image to draw on
# - y_coordinates is a list, containing the y-coordinates and length equal to the x dimension size
#   of the image
# - color is a (red, green, blue) color triple (e.g. (255, 0, 0) would be pure red
# - thickness is thickness of line in pixels
#
def draw_edge(image, y_coordinates, color, thickness):
    for (x, y) in enumerate(y_coordinates):
        for t in range(int(max(y - int(thickness / 2), 0)), int(min(y + int(thickness / 2), image.size[1] - 1))):
            image.putpixel((x, t), color)
    return image


# main program

gt_row = -1
gt_col = -1

if len(sys.argv) == 2:
    input_filename = sys.argv[1]
elif len(sys.argv) == 4:
    (input_filename, gt_row, gt_col) = sys.argv[1:]
else:
    raise Exception("Program requires either 1 or 3 parameters")

gt_row = int(gt_row)
gt_col = int(gt_col)

# load in image
input_image = Image.open(input_filename)

# compute edge strength mask
edge_strength = edge_strength(input_image)
imageio.imwrite('edges.jpg', uint8(255 * edge_strength / (amax(edge_strength))))

# simple bayes net
ridge = [argmax(edge_strength[:, i]) for i in range(edge_strength.shape[1])]
imageio.imwrite("static/Pics/output_simple.jpg", draw_edge(input_image, ridge, (255, 0, 0), 5))


## Viterbi
# pixel to consider for the previous columns
input_image = Image.open(input_filename)
def neighours_pixel(i, j):
    pixel_consider = [(i, j - 1), (i - 1, j - 1), (i - 2, j - 1), (i + 1, j - 1), (i + 2, j - 1)]
    boundary = []
    for n in pixel_consider:
        if 0 <= n[0] < edge_strength.shape[0] and 0 <= n[1] < edge_strength.shape[1]:
            boundary.append(n)
    return boundary


# emission probablity
def normalise(X):
    return (X - min(X)) / (max(X) - min(X))


emission_prob = [normalise(edge_strength[:, i]) for i in range(edge_strength.shape[1])]
emission_prob = array(emission_prob).T

# transition probablity
# same row probablity = 1
# +-1 row probablity = 0.5
# +- 0.01 row probablity = 0.01
transition_prob = [1, 0.5, 0.01]

# State probablity
state_prob = ones((edge_strength.shape[0], edge_strength.shape[1]))

# Inital probablity
state_prob[:, 0] = copy(emission_prob[:, 0])

# matrix contaning index value of maximum state of previous column
backtrack_matrix = ones((edge_strength.shape[0], edge_strength.shape[1]))

# viterbi
for col in range(1, edge_strength.shape[1]):
    for row in range(edge_strength.shape[0]):
        transition_pixel = neighours_pixel(row, col)
        max_a = -math.inf
        ## calculating the value of a
        for j in range(len(transition_pixel)):
            if abs(transition_pixel[j][0] - row) == 2:
                a = transition_prob[2] * state_prob[transition_pixel[j][0]][col - 1]
            elif abs(transition_pixel[j][0] - row) == 1:
                a = transition_prob[1] * state_prob[transition_pixel[j][0]][col - 1]
            else:
                a = transition_prob[0] * state_prob[transition_pixel[j][0]][col - 1]

            if a > max_a:
                max_a = a
                backtrack_matrix[row][col] = transition_pixel[j][0]

        state_prob[row][col] = emission_prob[row][col] * max_a

# maximum index for the last column. Based on this node backtracking would be done
max_state = argmax(state_prob[:, edge_strength.shape[1] - 1])
ridge_viterbi = ones(edge_strength.shape[1])

# backtracking the ridge
for col in range(edge_strength.shape[1] - 1, -1, -1):
    ridge_viterbi[col] = int(max_state)
    max_state = backtrack_matrix[int(max_state)][col]

imageio.imwrite("static/Pics/output_viterbi.jpg", draw_edge(input_image, ridge_viterbi, (0, 255, 0), 5))

# human input
# gt_row = 54
# gt_col = 100

if gt_row != -1 and gt_col != -1:

    ## changing the state probablity of the human input to one
    for row in range(edge_strength.shape[0]):
        state_prob[row][gt_col] = 0
    state_prob[gt_row][gt_col] = 1

    # gt_col becomes the initial state
    # feed forward from gt_col to the end
    for col in range(gt_col + 1, edge_strength.shape[1]):
        for row in range(edge_strength.shape[0]):

            transition_pixel = neighours_pixel(row, col)

            max_a = -math.inf
            ## calculating the value of a

            for j in range(len(transition_pixel)):
                if abs(transition_pixel[j][0] - row) == 2:
                    a = transition_prob[2] * state_prob[transition_pixel[j][0]][col - 1]
                elif abs(transition_pixel[j][0] - row) == 1:
                    a = transition_prob[1] * state_prob[transition_pixel[j][0]][col - 1]
                else:
                    a = transition_prob[0] * state_prob[transition_pixel[j][0]][col - 1]

                if a > max_a:
                    max_a = a
                    backtrack_matrix[row][col] = transition_pixel[j][0]

            state_prob[row][col] = emission_prob[row][col] * max_a

    max_state = argmax(state_prob[:, edge_strength.shape[1] - 1])
    ridge_human = ones(edge_strength.shape[1])

    for col in range(edge_strength.shape[1] - 1, -1, -1):
        ridge_human[col] = int(max_state)
        max_state = backtrack_matrix[int(max_state)][col]

    input_image = Image.open(input_filename)
    imageio.imwrite("static/Pics/output.jpg", draw_edge(input_image, ridge_human, (0, 0, 255), 5))

