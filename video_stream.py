import cv2
import socket

PORT = 8080

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("localhost", PORT))
s.listen(1)

client_socket, address = s.accept()

cap = cv2.VideoCapture(0)

ret, frame = cap.read()
grayscale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
_, img_data = cv2.imencode(".jpg", grayscale)
client_socket.sendall(img_data)

client_socket.close()
cap.release()
