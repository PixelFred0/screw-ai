from PIL import Image 
import random
import cv2 as cv

# load image

objects = []
targets = []


def imageCapture(device = 0, fileName = "frame"):
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
            print("Spacebar was pressed, Image captured ...")
            break
    cam.release()
    cv.destroyAllWindows()
    return f"{fileName}.png"


def object_collection():
    for i in range(20):
        print("Press Space to capture the Image!")
        image = Image.open(imageCapture(device=1))
        objects.append(recognisation(image=image))
        target = input("Enter 1 for long or 0 for short: " )
        targets.append(int(target))
    return objects, targets


def recognisation (image):
    threshold = 90
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
    # size of bounding box
    x = xmax-xmin
    y = ymax-ymin
    if x < y:
        x,y = y,x
    print ("Bounding Box: ",x,y)
    i = [x,y]
    return i


def create(size):
    neuron = []
    for i in range(size+1):
        neuron.append(random.random())
    return neuron


def output(neuron, input):
    s = 0 
    for i in range(len(input)):
        s = s + neuron[i] * input[i]
    s = s+neuron[len(input)]
    if s > 0:
        return 1
    else:
        return 0
    

def train(neuron, input, target):
    error = output(neuron, input) - target
    for i in range(len(input)):
        neuron[i] = neuron[i] - input[i] * error
    neuron[len(input)] = neuron[len(input)] - error


def learning(neuron, objects, targets):
    for i in range(10000000):
        index = int(random.randint(0,19))
        train(neuron, objects[index], targets[index])

print("### Traings-Process starts ###")
objects, targets = object_collection()
print (objects)
print(targets)
neuron = create(2)
print(neuron)
learning(neuron, objects, targets)
print(neuron)
print("### Start Detection ###")
for x in range(10):
    print("Put a screw under cam, to be measured!")
    screwType = output(neuron, recognisation(Image.open(imageCapture(device=1))))
    if screwType == 0:
        print("Screw is short!")
    else:
        print("Screw is long!")



    
