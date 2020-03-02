import cv2
import numpy as np
import matplotlib.pyplot as plt
from math import pi, inf

# Read the image 'coins'
img = cv2.imread('coins.png', cv2.IMREAD_COLOR)
# Copy the original image so we can show the detected circles later
img_orig = img.copy()
# Converting the image to RGB pattern
# OpenCV default is BGR (Blue, Green, Red)
img_orig = cv2.cvtColor(img_orig, cv2.COLOR_BGR2RGB)
# Convert the image to grayscale
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# Setting the size of the plot image to 16x9 proportion
plt.rcParams['figure.figsize'] = (16, 9)
# plt.imshow(img_orig)
# plt.show()
# plt.imshow(img, cmap='gray')
# plt.show()

# Using a Gaussian Blur to reduze the details
# so it's easier to identify circles
img = cv2.GaussianBlur(img, (21, 21), cv2.BORDER_DEFAULT)
# plt.imshow(img, cmap='gray')
# plt.show()

# To find the circles, we used HoughCircles in conjunction with Hough Gradient
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

"""
# Printing the full array of detected circles,
# where the first number is the 'x' coordinate,
# the second is the 'y' coordinate and
# the third is the radius
print(all_circles_rounded)

# Printing the dimensions of the circles array
# The number of circles detected is the second value
print(all_circles_rounded.shape)
"""
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

    # This labels which circle is which
    cv2.putText(img_orig, f'Coin {count}', (i[0] - 70, i[1] + 30), cv2.FONT_HERSHEY_SIMPLEX, 1.1, (255, 0, 0), 2)

    # Saving the detected circles informations for display
    area = pi * ((i[2] * 0.26) ** 2)
    perimeter = 2 * pi * (i[2] * 0.26)
    coins_info.append((count, area, perimeter, i[2]))
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
print(f'{"COIN":^6}|{"AREA (px²)":^14}|{"PERIMETER (px)":^16}')
print('-' * 6 + '+' + '-' * 14 + '+' + '-' * 16)
for index, coin in enumerate(coins_info):
    if coin[1] <= min:
        min = coin[1]
        min_coin = coin[0]

    if coin[1] >= max:
        max = coin[1]
        max_coin = coin[0]

    print(f'{coin[0]:^6}|{coin[1]:^14.2f}|{coin[2]:^16.2f}')
    print('-' * 6 + '+' + '-' * 14 + '+' + '-' * 16) if index != (len(coins_info) - 1) else print()

coins_5 = list()
coins_10 = list()
coins_25 = list()

for coin in coins_info:
    if coin[3] <= coins_info[min_coin - 1][3] + 7:
        coins_10.append(coin)
    elif coin[3] >= coins_info[max_coin - 1][3] - 6:
        coins_25.append(coin)
    else:
        coins_5.append(coin)

print(f'Smallest coin:\n\tCoin {min_coin}\n\tArea: {min:.2f} px²')
print(f'Largest coin:\n\tCoin {max_coin}\n\tArea: {max:.2f} px²')

print(f'\nQuantity of 5\'s: {len(coins_5)}')
for coin in coins_5:
    print(f'\tCoin {coin[0]}')
print(f'Quantity of 10\'s: {len(coins_10)}')
for coin in coins_10:
    print(f'\tCoin {coin[0]}')
print(f'Quantity of 25\'s: {len(coins_25)}')
for coin in coins_25:
    print(f'\tCoin {coin[0]}')

value = (len(coins_5) * 5) + (len(coins_10) * 10) + (len(coins_25) * 25)
value /= 100
print(f'\nValue on the table: R${value:.2f}')
