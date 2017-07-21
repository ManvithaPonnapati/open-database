#!/usr/bin/env python123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# -*- coding: utf-8 -*-123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport math123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport random123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFfrom random import randint123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport numpy as np123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport sys123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFfrom PIL import Image, ImageDraw, ImageOps123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport matchgenflags123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFDIM = matchgenflags.DIM123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFMARGINS = matchgenflags.MARGINS123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef generate_image_pairs(n):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    print_progress_bar(0, n, prefix="Generating images: ", suffix="Done!", decimals=2, length=50)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    for i in range(1, n + 1):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        print_progress_bar(i, n, prefix="Generating images: ", suffix="Done!", decimals=2, length=50)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        save_image_pair(i)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef save_image_pair(id):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    (lock, key) = get_image_pair()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    lock.save(matchgenflags.DIR + "/" + str(id) + "_L.png")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    key.save(matchgenflags.DIR + "/" + str(id) + "_K.png")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef get_image_pair():123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # First, generate a random polygon123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    shape = generate_polygon(center_x=DIM / 2, center_y=DIM/2, average_radius=DIM/4, irregularity=1, spikeyness=0.8, num_vertices=randint(10, 20))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    rotated_shape_for_lock = rotate(shape, random_angle())123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    rotated_shape_for_key = rotate(shape, random_angle())123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    lock_image = Image.new("1", (DIM - 1, DIM - 1), 0)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    key_image = Image.new("1", (DIM - 1, DIM - 1), 1)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    draw = ImageDraw.Draw(lock_image)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    draw.polygon(rotated_shape_for_lock, fill=1, outline=1)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    draw = ImageDraw.Draw(key_image)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    draw.polygon(rotated_shape_for_key, fill=0, outline=0)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    lock_image = full_size(lock_image, color=0)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    key_image = full_size(key_image, color=1)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    return lock_image, key_image123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# Based on https://stackoverflow.com/a/11143078123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef full_size(image, dimensions=(DIM, DIM), color=1, margins=(MARGINS, MARGINS)):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    new_size = (DIM + MARGINS * 2, DIM + MARGINS * 2)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    new_im = Image.new("1", new_size, color)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    new_im.paste(image, (randint(0, new_size[0] - DIM), randint(0, new_size[0] - DIM)))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    return new_im123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef generate_polygon(center_x, center_y, average_radius, irregularity, spikeyness, num_vertices):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    """123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    Based on https://stackoverflow.com/a/25276331123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    Start with the centre of the polygon at ctrX, ctrY,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    then creates the polygon by sampling points on a circle around the centre.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    Random noise is added by varying the angular spacing between sequential points,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    and by varying the radial distance of each point from the centre.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    Params:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    center_x, center_y - coordinates of the "centre" of the polygon123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    average_radius - in px, the average radius of this polygon, this roughly controls how large the polygon is, really only useful for order of magnitude.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    irregularity - [0,1] indicating how much variance there is in the angular spacing of vertices. [0,1] will map to [0, 2pi/numberOfVerts]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    spikeyness - [0,1] indicating how much variance there is in each vertex from the circle of radius aveRadius. [0,1] will map to [0, aveRadius]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    num_vertices - self-explanatory123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    Returns a list of vertices, in CCW order.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    """123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    irregularity = clip(irregularity, 0, 1) * 2 * math.pi / num_vertices123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    spikeyness = clip(spikeyness, 0, 1) * average_radius123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # generate n angle steps123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    angle_steps = []123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    lower = (2 * math.pi / num_vertices) - irregularity123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    upper = (2 * math.pi / num_vertices) + irregularity123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    current_sum = 0123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    for i in range(num_vertices):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        tmp = random.uniform(lower, upper)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        angle_steps.append(tmp)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        current_sum = current_sum + tmp123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # normalize the steps so that point 0 and point n+1 are the same123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    k = current_sum / (2 * math.pi)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    for i in range(num_vertices):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        angle_steps[i] = angle_steps[i] / k123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # now generate the points123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    points = []123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    angle = random.uniform(0, 2 * math.pi)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    for i in range(num_vertices):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        r_i = clip(random.gauss(average_radius, spikeyness), 0, 2 * average_radius)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        x = center_x + r_i * math.cos(angle)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        y = center_y + r_i * math.sin(angle)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        points.append((int(x), int(y)))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        angle = angle + angle_steps[i]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    return points123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef clip(x, minimum, maximum):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    if minimum > maximum:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        return x123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    elif x < minimum:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        return minimum123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    elif x > maximum:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        return maximum123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    else:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        return x123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef random_angle_degrees(min=0, max=359):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    return randint(min, max - 1)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef rotate(points, angle):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    result = list()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # Generate rotation matrix based on angle123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    rotation_matrix = np.matrix([[math.cos(angle), 0 - math.sin(angle)], [math.sin(angle), math.cos(angle)]])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # Loop through every point in the list of vertices123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    for point in points:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # Create a vector out of the point: (while setting center to origin)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        #   [[x]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        #    [y]]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        point_vector = np.transpose(np.matrix([point[0] - DIM / 2, point[1] - DIM / 2]))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # Multiply the rotation matrix by the point vector123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        rotated = np.matmul(rotation_matrix, point_vector)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # Reshape matrix into coordinate pair (and move origin back to origin from center)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        rotated_vertices = (math.floor(rotated.item((0, 0))) + DIM / 2, math.floor(rotated.item((1, 0))) + DIM / 2)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # Add rotated vertex to list123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        result.append(rotated_vertices)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    return result123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef random_angle():123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    return randint(0, 359) * math.pi / 180  # randint is inclusive, so 0 to 359123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef print_progress_bar(iteration, total, prefix='', suffix='', decimals=1, length=100, fill="█"):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    """123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    Call in a loop to create terminal progress bar. Based on https://stackoverflow.com/a/34325723123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    @params:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        iteration   - Required  : current iteration (Int)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        total       - Required  : total iterations (Int)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        prefix      - Optional  : prefix string (Str)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        suffix      - Optional  : suffix string (Str)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        decimals    - Optional  : positive number of decimals in percent complete (Int)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        length      - Optional  : character length of bar (Int)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        fill        - Optional  : bar fill character (Str)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    """123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    filled_length = int(length * iteration // total)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    bar = fill * filled_length + '-' * (length - filled_length)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    sys.stdout.write('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix) + '\r')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    sys.stdout.flush()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # Print New Line on Complete123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    if iteration == total:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        print()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        print()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        sys.stdout.write("")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF