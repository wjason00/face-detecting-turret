import cv2


video = cv2.VideoCapture(0)


while True:
    return_value, frame = video.read()
    
    # Drawing a line to show the middle of the screen by indexxing a tuple from frame.shape
    cv2.line(frame, (round(frame.shape[1] / 2), 0), (round(frame.shape[1] / 2), frame.shape[0]), (0,255,0), thickness=10)
    cv2.imshow("raspberry image", frame)
    print(frame.shape)

    if cv2.waitKey(30) & 0xFF == "27":
        video.release()
        cv2.destroyAllWindows()
       
