import cv2 as cv
from PIL import Image

def calibrateCamera(sizeEichObjectMM):
    image = Image.open(imageCapture(device=1))
    # initialize
    threshold = 80
    xmin = image.width
    xmax = 0
    ymin = image.height
    ymax = 0
    # convert to b/w image
    for x in range(0,image.width):
      for y in range(0,image.height):
        red = image.getpixel((x, y))[0]
        green = image.getpixel((x, y))[1]
        blue = image.getpixel((x, y))[2]
        if (red+green+blue) / 3 > threshold:
          image.putpixel((x, y), (255,255,255))
        else:
          image.putpixel((x, y), (0,0,0))
          if x < xmin:
            xmin = x
          elif x > xmax:
            xmax = x
          if y < ymin:
            ymin = y
          elif y > ymax:
            ymax = y
    # draw bounding box:
    for x in range(xmin, xmax):
      image.putpixel((x, ymin), (255,0,0))
      image.putpixel((x, ymax), (255,0,0))
    for y in range(ymin, ymax):
      image.putpixel((xmin, y), (255,0,0))
      image.putpixel((xmax, y), (255,0,0))
    # save image:
    image.save('output.png')
    # size of bounding box:
    x = xmax-xmin
    y = ymax-ymin
    if x < y:
      x,y = y,x
    print(x/sizeEichObjectMM)
    eichWert = x/sizeEichObjectMM
    return eichWert

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


calibrateCamera(eichWert=2.1)
