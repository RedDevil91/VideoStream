import cv2
import socket

PORT = 9999
HOST = socket.gethostbyname("DESKTOP-S87U62L")
# HOST = socket.gethostbyname("raspberrypi")

cap = cv2.VideoCapture(0)

while True:
    try:
        sock = socket.create_connection((HOST, PORT), 10)
        ret, frame = cap.read()
        _, img_data = cv2.imencode(".jpg", frame)
        byte_data = "%8d" % len(img_data) + img_data.tobytes()
        sock.sendall(byte_data)
        response = sock.recv(1024)
    except socket.error:
        break
cap.release()
