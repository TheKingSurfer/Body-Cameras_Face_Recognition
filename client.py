import cv2
import socket
import struct
import pickle

def video_sender(server_ip='127.0.0.1', server_port=8080):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, server_port))

    video = cv2.VideoCapture(0)

    while True:
        try:
            success, frame = video.read()
            data = pickle.dumps(frame)
            message_size = struct.pack("L", len(data))

            # Send message size first
            client_socket.sendall(message_size + data)

        except Exception as e:
            print(f"Error in video_sender: {str(e)}")
            break

    video.release()
    client_socket.close()

if __name__ == "__main__":
    video_sender()
