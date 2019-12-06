# exercise 2.11

import bpy
import numpy as np
import mathutils


# set size of output picture
picture_width = 513
picture_height = 513
# set filepth (file must be .png)
filepath = "//textures/perlin_noise_matze.png"
#set scale of noise
scale = 20


# save the perlin noise array as image to given path
def save_as_image(perlin_array, file_path):

	# store height and width
    height, width = len(perlin_array), len(perlin_array[0])

    # create new image
    image = bpy.data.images.new(file_path, width=width, height=height)

    # make rgb array
    image_pixel = [0 for y in range(height) for x in range(width)]
    for y in range(height):
        for x in range(width):
            r = perlin_array[y][x]
            g = r
            b = r
            a = 1.0

            image_pixel[int((y * width) + x)] = [r, g, b, a]

    # make it only 1d for blender
    image_pixel = [color_channel for x in image_pixel for color_channel in x]

    # assign pixels
    image.pixels = image_pixel

    # save image
    image.filepath_raw = file_path
    image.file_format = 'PNG'
    image.save()

# normalize the moisture array
def normalize_array(perlin_array):
    # finding the smallest value of the noise map
    smallest_value = np.amin(perlin_array)
    # finding the largest value of the noise map
    largest_value = np.amax(perlin_array)
    value_range = largest_value + abs(smallest_value)

    # Go through the 2d array and update the values
    # according to the smallest and highest values
    for y in range(len(perlin_array)):
        for x in range(len(perlin_array[y])):
            perlin_array[y][x] = (perlin_array[y][x] + abs(smallest_value)) / value_range
    
    return perlin_array

# generate perlin noise array with values between 0 and 1
def generate_perlin_noise(height, width, scale):
    height = int(height)
    width = int(width)
    
	# init the noisemap with zeros
    perlin_noise = [[0 for x in range(width)] for y in range(height)]
    
    # adding the noise to each pixel of the noise map
    for y in range(height):
        for x in range(width):
            nx = x/width * scale
            ny = y/height * scale
            perlin_noise[y][x] = mathutils.noise.noise(mathutils.Vector((nx, ny, 1)))
    
    return normalize_array(perlin_noise)


if __name__ == "__main__":
	# perform perlin noise algorithm
    moisture_map = generate_perlin_noise(picture_height, picture_width, scale)
	# save array as image
    save_as_image(moisture_map, filepath)
