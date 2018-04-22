# Echo client program
import socket
import cv2
import numpy as np

MAX_RCV_LENGTH = 2048

HOST = 'localhost'    # The remote host
PORT = 8080           # The same port as used by the server

stream = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
stream.connect((HOST, PORT))


def get_image_from_stream(stream_socket, msg_length):
    chunks = []
    bytes_rcvd = 0
    while bytes_rcvd < msg_length:
        chunk = stream_socket.recv(min(msg_length - bytes_rcvd, MAX_RCV_LENGTH))
        bytes_rcvd += len(chunk)
        chunks.append(chunk)
    data = "".join(chunks)
    img_data = np.fromstring(data, dtype=np.uint8)
    img = cv2.imdecode(img_data, 1)
    return img


while True:
    msg_length = int(stream.recv(8))
    received_img = get_image_from_stream(stream, msg_length)
    cv2.imshow("test", received_img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
stream.close()
