import cv2
import numpy as np
import SocketServer
import threading
import Queue

MAX_RCV_LENGTH = 2048

HOST = 'localhost'
PORT = 9999

incoming_images = Queue.Queue()


class ThreadedRequestHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        length = int(self.request.recv(1024))
        self.request.sendall("OK")
        image = self.get_image_from_stream(length)
        incoming_images.put(image)
        self.request.sendall("OK")

    def get_image_from_stream(self, image_length):
        chunks = []
        bytes_rcvd = 0
        while bytes_rcvd < image_length:
            chunk = self.request.recv(min(image_length - bytes_rcvd, MAX_RCV_LENGTH))
            bytes_rcvd += len(chunk)
            chunks.append(chunk)
        data = "".join(chunks)
        img_data = np.fromstring(data, dtype=np.uint8)
        img = cv2.imdecode(img_data, 1)
        return img


class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass


if __name__ == '__main__':
    server = ThreadedTCPServer((HOST, PORT), ThreadedRequestHandler)

    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.setDaemon(True)
    server_thread.start()

    while True:
        if not incoming_images.empty():
            received_img = incoming_images.get()
            cv2.imshow("test", received_img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    server.shutdown()
    server.server_close()
