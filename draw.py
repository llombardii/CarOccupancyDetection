import cv2

# Initialize variables
drawing = False
ix, iy = -1, -1
cell_size = 20  # Adjust the size of each grid cell as needed
coordinates = []

# Mouse callback function
def draw_grid(event, x, y, flags, param):
    global ix, iy, drawing, coordinates

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        width, height = x - ix, y - iy
        cv2.rectangle(car_park_img, (ix, iy), (x, y), (0, 255, 0, 128), 2)  # Semi-transparent rectangle
        coordinates.append((ix, iy, width, height))

# Load the existing image
car_park_img = cv2.imread('carParkImg.png', cv2.IMREAD_UNCHANGED)


# Set up the window and set the callback function
cv2.namedWindow('Bounding boxes')
cv2.setMouseCallback('Bounding boxes', draw_grid)

while True:
    cv2.imshow('Bounding boxes', car_park_img)
    key = cv2.waitKey(1) & 0xFF

    # Exit when 'Esc' is pressed
    if key == 27:
        break

cv2.destroyAllWindows()

# Print the coordinates of the grid boxes
for i, coord in enumerate(coordinates):
    print(f'Slot {i + 1}: {coord[0]}, {coord[1]}, {coord[2]}, {coord[3]}')
