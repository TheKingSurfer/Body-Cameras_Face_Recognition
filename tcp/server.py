import cv2
import socket
import struct
import pickle
import threading
import logging
import os
import datetime


class VideoServer:

    def __init__(self, ip='0.0.0.0', port=9090):
        # Initialize VideoServer with default IP '0.0.0.0' and port 9090
        self.ip = ip
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.logger = self.setup_logger()

    def setup_logger(self):
        # Set up logging configuration for the server
        logger = logging.getLogger('server_logger')
        logger.setLevel(logging.DEBUG)

        # Create log file with a name containing the current date
        current_date = datetime.datetime.now().strftime('%Y-%m-%d')
        log_file_path = os.path.join(os.getcwd(), f"server_log_{current_date}.txt")

        # Define log message format
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s')

        # File Handler for writing logs to a file
        fh = logging.FileHandler(log_file_path)
        fh.setFormatter(formatter)

        # Stream Handler for printing logs to the console
        ch = logging.StreamHandler()
        ch.setFormatter(formatter)

        # Add both handlers to the logger
        logger.addHandler(fh)
        logger.addHandler(ch)

        return logger

    def start(self):
        try:
            # Bind and listen for incoming connections
            self.server_socket.bind((self.ip, self.port))
            self.server_socket.listen(1)
            self.logger.info(f"Server listening on {self.ip}:{self.port}")

            while True:
                # Accept incoming connections and start a new thread for each client
                client_socket, client_addr = self.server_socket.accept()
                self.logger.info("Client connected for video streaming")

                # Start a new thread to handle video reception for the connected client
                client_thread = threading.Thread(target=self.receive_video, args=(client_socket, client_addr,))
                client_thread.start()

        except Exception as e:
            self.logger.exception(f"Error in start: {str(e)}")
        finally:
            # Close the server socket when done
            self.server_socket.close()

    def receive_video(self, client_socket, client_addr):
        try:
            data = b""
            payload_size = struct.calcsize("L")

            while True:
                # Receive the size of the video frame
                while len(data) < payload_size:
                    data += client_socket.recv(4096)
                    if not data:
                        break

                packed_msg_size = data[:payload_size]
                data = data[payload_size:]

                msg_size = struct.unpack("L", packed_msg_size)[0]

                # Receive the video frame data
                while len(data) < msg_size:
                    data += client_socket.recv(4096)
                    if not data:
                        break

                frame_data = data[:msg_size]
                data = data[msg_size:]

                # Unpickle the frame data and display it using OpenCV
                frame = pickle.loads(frame_data)
                cv2.imshow(f'Video Stream {str(client_addr)}', frame)

                # Break the loop if the 'q' key is pressed
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

        except Exception as e:
            self.logger.exception(f"Error in receive_video: {str(e)}")
        finally:
            # Close OpenCV window, client socket, and log connection closure
            cv2.destroyAllWindows()
            client_socket.close()
            self.logger.info(f"Connection with {client_addr[0]} closed.")


def main():
    # Create a VideoServer instance and start the server
    video_server = VideoServer()
    video_server.start()


if __name__ == '__main__':
    # Run the server when the script is executed
    main()
