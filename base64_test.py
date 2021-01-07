import base64
import io
import cv2
import matplotlib.pyplot as plt
import numpy as np

filename = "image_on.png"
with open(filename, "rb") as fid:
    data = fid.read()

b64_bytes = base64.b64encode(data)
b64_string = b64_bytes.decode()

print(b64_bytes)
print(b64_string)

image = b64_string  # raw data with base64 encoding
decoded_data = base64.b64decode(image)
np_data = np.fromstring(decoded_data,np.uint8)
img = cv2.imdecode(np_data,cv2.IMREAD_UNCHANGED)
cv2.imshow("test", img)
cv2.waitKey(0)
