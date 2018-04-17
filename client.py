# Echo client program
import socket
import cv2
import numpy as np

HOST = 'localhost'    # The remote host
PORT = 8080           # The same port as used by the server

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
data = s.recv(65536)
s.close()
img_data = np.fromstring(data, dtype=np.uint8)
img = cv2.imdecode(img_data, 1)
cv2.imshow("test", img)
while True:
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
