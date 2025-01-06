import cv2 
import numpy as np
def detect_glass(image):
  edges = cv2.Canny(image, 130, 200)
  lines = cv2.HoughLinesP(edges, rho=1, theta=np.pi/180, threshold=50, minLineLength=10, maxLineGap=6)

  if lines is not None:
      for line in lines:
          x1, y1, x2, y2 = line[0]
          image_length = image.shape[1]
          # print(image_length,length)

          if abs(y2 - y1) < abs(x2 - x1):
              length = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
              # cv2.imshow('detect glass',image)
              # cv2.waitKey(0)
              # print(length)
                          # cv2.imshow('detect glass',gray_center_cropped_image)
            # cv2.waitKey(0)
              # return True
            #   print(f"Line detected: Image width={image_length}, Line length={length}")
              # Check if line length approximately matches the image width
              if 12 < length < image_length + 3:
                #   print(f"Horizontal line detected matching image width: {length}")
                  return True
  return False