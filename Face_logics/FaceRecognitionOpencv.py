import cv2
from simple_facerec import SimpleFacerec


#Encode faces from folders
sfr = SimpleFacerec()
sfr.load_encoding_images("Images/BillGates/")

#load camera
cap = cv2.VideoCapture(0)


while True:
    ret, frame = cap.read()
    cv2.imshow("Frame", frame)

    #detect faces
    face_locations, face_names =sfr.detect_known_faces(frame)
    for face_loc, name in zip(face_locations, face_names):
        #print the quardinates of the face shown in the camera
        print(face_loc)



    key = cv2.waitKey(1)
    if key == 27:
        break
cap.release()
cv2.destroyAllWindows()



