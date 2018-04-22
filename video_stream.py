import cv2
import socket

PORT = 8080

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("localhost", PORT))
s.listen(1)

client_socket, address = s.accept()

cap = cv2.VideoCapture(0)

while True:
    try:
        ret, frame = cap.read()
        _, img_data = cv2.imencode(".jpg", frame)
        client_socket.sendall(str(len(img_data)).encode())
        client_socket.sendall(img_data)
    except socket.error:
        break

client_socket.close()
cap.release()
