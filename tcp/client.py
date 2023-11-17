import cv2
import socket
import struct
import pickle

def video_sender(server_ip='127.0.0.1', server_port=9090):
    # Create a client socket and connect to the server
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, server_port))

    # Open a video file for reading frames
    video = cv2.VideoCapture(r"../Bill Hader channels Tom Cruise [DeepFake].mp4")
    print("Heyy")

    while True:
        try:
            # Read a frame from the video
            success, frame = video.read()

            # Serialize the frame using pickle
            data = pickle.dumps(frame)

            # Pack the size of the serialized frame as a message
            message_size = struct.pack("L", len(data))

            # Send the size of the message followed by the serialized frame data
            client_socket.sendall(message_size + data)

        except Exception as e:
            # Print an error message if an exception occurs and break out of the loop
            print(f"Error in video_sender: {str(e)}")
            break

    # Release the video capture and close the client socket
    video.release()
    client_socket.close()

if __name__ == "__main__":
    # Call the video_sender function when the script is executed
    video_sender()
