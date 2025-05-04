import cv2

def convert_to_sketch(image_path):
    img = cv2.imread(image_path)
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    inv_img = 255 - gray_img
    blur_img = cv2.GaussianBlur(inv_img, (21, 21), 0)
    sketch = cv2.divide(gray_img, 255 - blur_img, scale=256.0)
    return sketch
