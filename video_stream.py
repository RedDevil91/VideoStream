import cv2
import socket

PORT = 9999
# HOST = "127.0.0.1"
HOST = socket.gethostbyname("DESKTOP-S87U62L")

cap = cv2.VideoCapture(0)

while True:
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((HOST, PORT))
        ret, frame = cap.read()
        _, img_data = cv2.imencode(".jpg", frame)
        sock.sendall(str(len(img_data)).encode())
        response = sock.recv(1024)
        if response == "OK":
            sock.sendall(img_data)
            sock.recv(1024)
    except socket.error:
        sock.close()
        break
cap.release()
