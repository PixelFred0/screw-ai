import cv2 as cv

def imageCapture(device = 0, fileName = "frame"):
    import cv2 as cv
    cam = cv.VideoCapture(device)
    cv.namedWindow("Schrauben Auswahl")
    while True:
        ret, frame = cam.read()
        if not ret:
            print("failed to grab frame")
            break
        cv.imshow("Schrauben Auswahl", frame)
        k = cv.waitKey(1)
        if k%256 == 27:
            # ESC pressed
            print("Escape gedrückt, schließt...")
            break
        elif k%256 == 32:
            # SPACE pressed
            img_name = f"{fileName}.png"
            cv.imwrite(img_name, frame)
            print("{} written!".format(img_name))
            print("Leertaste gedrückt, schließt...")
            break
    cam.release()
    cv.destroyAllWindows()
    return f"{fileName}.png"



