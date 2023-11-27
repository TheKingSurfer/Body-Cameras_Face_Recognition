from deepface import DeepFace
import cv2
import json
import face_

def save_to_file(data, filename='output.txt'):
    with open(filename, 'a') as file:
        file.write(json.dumps(data) + '\n')

def main():
    # Set your image directory
    image_directory = "Images"

    # Set the model name
    model_name = "MediaPipe"

    # Start the stream
    for frame in DeepFace.stream(image_directory):
        try:
            # Process the frame using deepface
            results = DeepFace.analyze(frame, actions=['emotion'])

            # Print or use the results as needed
            print(results)

            # Save the results to a file
            save_to_file(results)

            # Display the frame
            cv2.imshow("Facial Recognition Stream", frame)

            # Check for the 'q' key press to exit the stream
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        except Exception as e:
            print(f"Error processing frame: {e}")

    # Release the video capture object and close the OpenCV windows
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
