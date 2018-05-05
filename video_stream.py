import cv2
import socket

PORT = 9999
HOST = socket.gethostbyname("DESKTOP-S87U62L")
# HOST = socket.gethostbyname("raspberrypi")

cap = cv2.VideoCapture(0)
sock = socket.create_connection((HOST, PORT), 10)

while True:
    try:
        ret, frame = cap.read()
        _, img_data = cv2.imencode(".jpg", frame)
        sock.sendall(str(len(img_data)).encode())
        response = sock.recv(1024)
        if response == "OK":
            sock.sendall(img_data)
            sock.recv(1024)
    except socket.error:
        break
cap.release()
