import cv2
import numpy as np
import matplotlib.pyplot as plt
from math import pi, inf

# Read the image "moedas"
img = cv2.imread('moedas.png', cv2.IMREAD_COLOR)
# Copy the original image so we can show the detected circles later
img_orig = img.copy()
# Convert the image to grayscale
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# Set the size of the plot image to 16x9 proportion
plt.rcParams['figure.figsize'] = (16, 9)
plt.imshow(img, cmap='gray')
plt.show()

# Using a Gaussian Blur to reduze the details
# so it's easier to identify circles
img = cv2.GaussianBlur(img, (21, 21), cv2.BORDER_DEFAULT)
plt.imshow(img, cmap='gray')
plt.show()

# To find the circles, we use HoughCircles in conjunction with Hough Gradient
# The arguments taken by the function are:
# The image that will be analized
# The method of analisis, in this case, Hough Gradient, which uses the gradient information of edges
# The inverse ratio of the accumulator resolution to the image resolution.
#       (dp = 1, the accumulator has the same resolution as the input image,
#       dp = 2, the accumulator has half the resolution and so on)
# The minimum distance between detected circles centers
#       (If too small, multiple circles may be falsely detected.
#       If too large, some circles may be missed)
# First method-specific parameter. In case of HOUGH_GRADIENT,
#       it is the higher threshold of the two passed to the Canny edge detector
#       (the lower one is twice smaller)
# second method-specific parameter. In case of HOUGH_GRADIENT,
#       it is the accumulator threshold for the circle centers at the detection stage.
#       The smaller it is, the more false circles may be detected.
#       Circles, corresponding to the larger accumulator values, will be returned first.
# Minimum circle radius
# Maximum circle radius
all_circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 1, 120, param1=50, param2=30, minRadius=60, maxRadius=150)
# Evenly round the numbers received from HoughCircles and converts them to 16 bits unsigned integer type
all_circles_rounded = np.uint16(np.around(all_circles))

# Printing the full array of detected circles,
# where the first number is the 'x' coordinate,
# the second is the 'y' coordinate and
# the third is the radius
print(all_circles_rounded)

# Printing the dimensions of the circles array
# The number of circles detected is the second value
print(all_circles_rounded.shape)
print(f'I have found {all_circles_rounded.shape[1]} coins!')

coins_info = list()
count = 1
# Iterating through all the coins and drawing a circle on top
# of the original image showing the detected circles
for i in all_circles_rounded[0, :]:
    # The parameters for the 'circle' function are:
    # The image in which the circle will be drawn
    # A tuple with the circles' center coordinates
    # The circle radius
    # A tuple with the RGB color of the circle
    # The width of the circle line

    # This first circle is the border of the detected circle
    cv2.circle(img_orig, (i[0], i[1]), i[2], (0, 255, 0), 5)
    # This is the center of the detected circle
    cv2.circle(img_orig, (i[0], i[1]), 2, (255, 0, 0), 3)

    # This just labels which circle is which
    cv2.putText(img_orig, f'Coin {count}', (i[0] - 70, i[1] + 30), cv2.FONT_HERSHEY_SIMPLEX, 1.1, (255, 0, 0), 2)

    # Saving the detected circles informations for display
    area = pi * (i[2] ** 2)
    perimeter = 2 * pi * i[2]
    coins_info.append((count, area, perimeter))
    count += 1

# Showing the original image with the drawn circles on it
plt.imshow(img_orig)
plt.show()

print()
max = -inf
max_coin = -1
min = inf
min_coin = -1

# Printing each circles' information, as well as
# comparing them to find the smallest and the largest ones
for index, coin in enumerate(coins_info):
    if coin[1] <= min:
        min = coin[1]
        min_coin = coin[0]

    if coin[1] >= max:
        max = coin[1]
        max_coin = coin[0]

    print(f'Coin {coin[0]}')
    print(f'\tArea: {coin[1]:.2f} pixels')
    print(f'\tPerimeter: {coin[2]:.2f} pixels')
    print()

print(f'Smallest coin:\n\tCoin {min_coin}\n\tArea: {min:.2f} pixels')
print(f'Largest coin:\n\tCoin {max_coin}\n\tArea: {max:.2f} pixels')