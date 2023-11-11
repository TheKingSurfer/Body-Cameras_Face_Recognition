import cv2
import socket
import struct
import pickle
import threading
import logging
import os
import datetime


class VideoServer:
    def __init__(self, ip='0.0.0.0', port=8080):
        self.ip = ip
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.logger = self.setup_logger()

    def setup_logger(self):
        logger = logging.getLogger('server_logger')
        logger.setLevel(logging.DEBUG)
        
        current_date = datetime.datetime.now().strftime('%Y-%m-%d')
        log_file_path = os.path.join(os.getcwd(), f"server_log_{current_date}.txt")
        
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s')
        
        # File Handler
        fh = logging.FileHandler(log_file_path)
        fh.setFormatter(formatter)
        
        # Stream Handler (stdout)
        ch = logging.StreamHandler()
        ch.setFormatter(formatter)
        
        logger.addHandler(fh)
        logger.addHandler(ch)
        
        return logger

    def start(self):
        try:
            self.server_socket.bind((self.ip, self.port))
            self.server_socket.listen(1)
            self.logger.info(f"Server listening on {self.ip}:{self.port}")

            while True:
                client_socket, client_addr = self.server_socket.accept()
                self.logger.info("Client connected for video streaming")

                client_thread = threading.Thread(target=self.receive_video, args=(client_socket, client_addr,))
                client_thread.start()

        except Exception as e:
            self.logger.exception(f"Error in start: {str(e)}")
        finally:
            self.server_socket.close()

    def receive_video(self, client_socket, client_addr):
        try:
            data = b""
            payload_size = struct.calcsize("L")

            while True:
                print("asd")
                while len(data) < payload_size:
                    data += client_socket.recv(4096)
                    if not data:
                        break
                    
                packed_msg_size = data[:payload_size]
                data = data[payload_size:]

                msg_size = struct.unpack("L", packed_msg_size)[0]

                while len(data) < msg_size:
                    data += client_socket.recv(4096)
                    if not data:
                        break

                frame_data = data[:msg_size]
                data = data[msg_size:]

                frame = pickle.loads(frame_data)
                cv2.imshow(f'Video Stream {client_addr[0]}', frame)
                
                if cv2.waitKey(1) & 0xFF == ord('q') :
                    break

        except Exception as e:
            self.logger.exception(f"Error in receive_video: {str(e)}")
        finally:
            cv2.destroyAllWindows()
            client_socket.close()
            self.logger.info(f"Connection with {client_addr[0]} closed.")

def main():
    video_server = VideoServer()
    video_server.start()

if __name__ == '__main__':
    main()
