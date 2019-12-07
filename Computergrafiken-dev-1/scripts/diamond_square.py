import numpy as np
import random
import bpy

# set size of output picture
picture_width = 513
picture_height = 513
# set filepth (file must be .png)
filepath = "C:/Users/Yannik/Dropbox/studium/computergrafik/abschlussarbeit/blender_diamond_square/diamond_square.png"

# looks for max picture length and searches for next bigger value which fullfills the condition: side_length == (2^n)+1
max_side_length = max(picture_height, picture_width)
n = int(np.ceil(np.log(max_side_length - 1)/np.log(2)))
global_side_length = (2**n)+1
# algorithm works with this value, in the end the calculated picture will be cropped to the picture lengths

# initialize array
pixels = np.zeros((global_side_length, global_side_length))
pixels_was_changed = np.zeros((global_side_length, global_side_length))
# initialize corner values ([y, x]) with random values between 0 and 1
# top left
pixels[0, 0] = random.uniform(0, 1)
pixels_was_changed[0, 0] += 1
# top right
pixels[0, global_side_length-1] = random.uniform(0, 1)
pixels_was_changed[0, global_side_length-1] += 1
# bottom left
pixels[global_side_length-1, 0] = random.uniform(0, 1)
pixels_was_changed[global_side_length-1, 0] += 1
# bottom right
pixels[global_side_length-1, global_side_length-1] = random.uniform(0, 1)
pixels_was_changed[global_side_length-1, global_side_length-1] += 1

# corner positions (top left, top right, bottom left, bottom right)
global_corners = np.array([[0, 0], [0, global_side_length-1],
                           [global_side_length-1, 0], [global_side_length-1, global_side_length-1]])
all_global_corners = np.reshape(global_corners, (4, 2, 1))


# adds a random value to average value, average value of random is zero
def calculate_new_height_value(average):
    # the smaller the size of the square, the smaller the magnitude of the random value
    # if dimension_difference match to the maximim (side_length), value range for random method is the largest
    # if dimension_difference match to the minimum (1), value rage is zero --> new height value is average without a random value
    square_edge_length = int(
        (all_global_corners[1, 1, 0] - all_global_corners[0, 1, 0]))
    if square_edge_length == 1:
        return average
    else:
        rand_max = ((1-average)/(global_side_length-2)) * (square_edge_length - 1)
        random_value = random.uniform(-rand_max, rand_max)
        return average + random_value


# perform diamond step
def diamond_step(corner):
    half_edge_length = int((corner[1, 1] - corner[0, 1]) / 2)
    average = 0
    for i in range(4):
        average += pixels[corner[i, 0], corner[i, 1]]
    average = average / 4
    # point in the middle of the corners
    x_pos = corner[0, 1] + half_edge_length
    y_pos = corner[0, 0] + half_edge_length
    pixels[y_pos, x_pos] = calculate_new_height_value(average)
    pixels_was_changed[y_pos, x_pos] += 1


# perform square step
def square_step(corner):
    # TOP (value in the middle of top edge of square)
    half_edge_length = int((corner[1, 1] - corner[0, 1]) / 2)
    value_middle = pixels[corner[0, 0] +
                          half_edge_length, corner[0, 1] + half_edge_length]
    x_pos = corner[0, 1] + half_edge_length
    y_pos = corner[0, 0]
    # check if value assignment was already done
    if pixels_was_changed[y_pos, x_pos] == 0:
        # check for global edge, if theres an edge --> half diamond
        if corner[0, 0] != 0:
            average = pixels[corner[0, 0], corner[0, 1]] + pixels[corner[1, 0], corner[1, 1]] + \
                value_middle + pixels[corner[0, 0] -
                                      half_edge_length, corner[0, 1] + half_edge_length]
            average = average / 4
        else:
            average = pixels[corner[0, 0], corner[0, 1]] + \
                pixels[corner[1, 0], corner[1, 1]] + value_middle
            average = average / 3
        # value for new point should be < 1
        pixels[y_pos, x_pos] = calculate_new_height_value(
            average)
        pixels_was_changed[y_pos, x_pos] = 1

    # BOTTOM (value in the middle of bottom edge of square)
    x_pos = corner[0, 1] + half_edge_length
    y_pos = corner[2, 0]
    if pixels_was_changed[y_pos, x_pos] == 0:
        # check for global edge, if theres an edge --> half diamond
        if corner[2, 0] != global_side_length-1:
            average = pixels[corner[2, 0], corner[2, 1]] + pixels[corner[3, 0], corner[3, 1]] + \
                value_middle + pixels[corner[2, 0] +
                                      half_edge_length, corner[2, 1] + half_edge_length]
            average = average / 4
        else:
            average = pixels[corner[2, 0], corner[2, 1]] + \
                pixels[corner[3, 0], corner[3, 1]] + value_middle
            average = average / 3
        # value for new point should be < 1
        pixels[y_pos, x_pos] = calculate_new_height_value(
            average)
        pixels_was_changed[y_pos, x_pos] += 1

    # LEFT (value in the middle of left edge of square)
    x_pos = corner[0, 1]
    y_pos = corner[0, 0] + half_edge_length
    # check if value assignment was already done
    if pixels_was_changed[y_pos, x_pos] == 0:
        # check for global edge, if theres an edge --> half diamond
        if corner[0, 1] != 0:
            average = pixels[corner[0, 0], corner[0, 1]] + pixels[corner[2, 0], corner[2, 1]] + \
                value_middle + pixels[corner[0, 0] +
                                      half_edge_length, corner[0, 1] - half_edge_length]
            average = average / 4
        else:
            average = pixels[corner[0, 0], corner[0, 1]] + \
                pixels[corner[2, 0], corner[2, 1]] + value_middle
            average = average / 3
        # value for new point should be < 1
        pixels[y_pos, x_pos] = calculate_new_height_value(
            average)
        pixels_was_changed[y_pos, x_pos] += 1

    # RIGHT (value in the middle of right edge of square)
    x_pos = corner[1, 1]
    y_pos = corner[0, 0] + half_edge_length
    # check if value assignment was already done
    if pixels_was_changed[y_pos, x_pos] == 0:
        # check for global edge, if theres an edge --> half diamond
        if corner[1, 1] != global_side_length - 1:
            average = pixels[corner[1, 0], corner[1, 1]] + pixels[corner[3, 0], corner[3, 1]] + \
                value_middle + pixels[corner[0, 0] +
                                      half_edge_length, corner[1, 1] + half_edge_length]
            average = average / 4
        else:
            average = pixels[corner[1, 0], corner[1, 1]] + \
                pixels[corner[3, 0], corner[3, 1]] + value_middle
            average = average / 3
        # value for new point should be < 1
        pixels[y_pos, x_pos] = calculate_new_height_value(
            average)
        pixels_was_changed[y_pos, x_pos] += 1

# subdivide square into 4 subsquares and return corner points
def get_new_corners(corner):
    half_edge_length = int((corner[1, 1] - corner[0, 1]) / 2)
    sub_corners_1 = np.array([[corner[0, 0], corner[0, 1]], [corner[0, 0], corner[0, 1] + half_edge_length], [
        corner[0, 0] + half_edge_length, corner[0, 1]], [corner[0, 0] + half_edge_length, corner[0, 1] + half_edge_length]])
    sub_corners_2 = np.array([[corner[0, 0], corner[0, 1] + half_edge_length], [corner[1, 0], corner[1, 1]], [
        corner[0, 0] + half_edge_length, corner[0, 1] + half_edge_length], [corner[1, 0] + half_edge_length, corner[1, 1]]])
    sub_corners_3 = np.array([[corner[0, 0] + half_edge_length, corner[0, 1]], [corner[0, 0] + half_edge_length,
                                                                              corner[0, 1] + half_edge_length], [corner[2, 0], corner[2, 1]], [corner[2, 0], corner[2, 1] + half_edge_length]])
    sub_corners_4 = np.array([[corner[3, 0] - half_edge_length, corner[3, 1] - half_edge_length], [corner[3, 0] -
                                                                                               half_edge_length, corner[3, 1]], [corner[3, 0], corner[3, 1] - half_edge_length], [corner[3, 0], corner[3, 1]]])
    new_sub_corners = np.zeros((4, 2, 4))
    new_sub_corners[:, :, 0] = sub_corners_1
    new_sub_corners[:, :, 1] = sub_corners_2
    new_sub_corners[:, :, 2] = sub_corners_3
    new_sub_corners[:, :, 3] = sub_corners_4
    return new_sub_corners

# perform diamond square algorithm
def perform_diamond_square():
    while True:
        global all_global_corners
        number_squares = all_global_corners.shape[2]

        # for all squares do diamond step
        for i in range(number_squares):
            actual_corner = all_global_corners[:, :, i]
            diamond_step(actual_corner)

        # for all squares do square step
        for i in range(number_squares):
            actual_corner = all_global_corners[:, :, i]
            square_step(actual_corner)

        # abort criterion: length of square edge is 2
        square_edge_length = int(
            (all_global_corners[1, 1, 0] - all_global_corners[0, 1, 0]))
        if square_edge_length == 2:
            break

        # for each square determine sub squares, override global array with corners
        # corners of first sub square will be written to first place in arrays, next will be concatenated
        new_corners = np.zeros((4, 2, 4))
        for i in range(number_squares):
            actual_corner = all_global_corners[:, :, i]
            actual_new_corner = get_new_corners(actual_corner)
            if i == 0:
                new_corners[:, :, 0:] = actual_new_corner
            else:
                new_corners = np.concatenate((new_corners, get_new_corners(
                    actual_corner)), axis=2)
        all_global_corners = new_corners.astype(int)


if __name__ == "__main__":
    # perform diamond square algorithm
    perform_diamond_square()

    # crop picture to the desired picture size
    picture = pixels[0:picture_height, 0:picture_width]
    
    # save array to image
    image = bpy.data.images.new("diamond_square_height_map", width=picture_width, height=picture_height)

    # create array for RGBA values
    pixels_image = [None] * picture_width * picture_height
    for x in range(picture_width):
        for y in range(picture_height):
            # assign RGBA values to same value to get greyscale
            color_value = picture[y, x]
            r = color_value
            g = color_value
            b = color_value
            a = 1.0

            pixels_image[(y * picture_width) + x] = [r, g, b, a]

    # flatten list
    pixels_image = [chan for px in pixels_image for chan in px]

    # hand over array with RGBA values
    image.pixels = pixels_image

    # save image
    image.filepath_raw = filepath
    image.file_format = 'PNG'

    try:
        image.save()
        print("image saved")
    except:
        print("ERROR: image not saved")