from PIL import Image 
import random
import cv2 as cv
import json
import os

def saveTrainData(trainData = [], file = "data.json"):
    if not os.path.isfile(file):
        print("data.json does not exsits")
        with open('data.json', 'x') as f:
            data = {}
            json.dump(data, f, indent=4)
    with open(file, 'r+') as f:
        data = json.load(f)
        data['trainData'] = trainData 
        f.seek(0)        
        json.dump(data, f, indent=4)
        f.truncate()

def loadTrainData(file = "data.json"):
    with open(file) as f:
        data = json.load(f)
        fileTrainData = data["trainData"]
    return fileTrainData

def imageCapture(device = 0, file_name = "frame"):
    cam = cv.VideoCapture(device)
    cv.namedWindow("Bild Aufnahme")
    capture_process = True
    while capture_process:
        ret, frame = cam.read()
        if not ret:
            print("failed to grab frame")
            capture_process = False
        cv.imshow("Bild Aufnahme", frame)
        k = cv.waitKey(1)
        if k%256 == 27:
            # ESC pressed
            print("Escape gedrückt, schließt...")
            capture_process = False
        elif k%256 == 32:
            # SPACE pressed
            img_name = f"{file_name}.png"
            cv.imwrite(img_name, frame)
            print("{} written!".format(img_name))
            print("Spacebar was pressed, Image captured ...")
            capture_process = False
    cam.release()
    cv.destroyAllWindows()
    return f"{file_name}.png"

def calibrateCamera(sizeEichObjectMM):
    image = Image.open(imageCapture(device=1))
    x = recognisation(image, 1)[1]
    print(x/sizeEichObjectMM)
    eichWert = sizeEichObjectMM/x
    return eichWert

def eichen(boundingBox, eichWert):
    for i in range(len(boundingBox)):
      boundingBox[i] = boundingBox[i] * eichWert 
    return boundingBox

def object_collection(eichWert, amount_to_train):
    for i in range(amount_to_train):
        print("Press Space to capture the Image!")
        image = Image.open(imageCapture(device=1))
        objects.append(recognisation(image, eichWert)[0])
        target = input("Enter 1 for long or 0 for short: " )
        targets.append(int(target))
    return objects, targets


def recognisation (image, eichWert):
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
    boundingBox = eichen([x,y], eichWert)
    return boundingBox, x

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

def learning(neuron, objects, targets, learning_rate):
    for i in range(learning_rate):
        index = int(random.randint(0,19))
        train(neuron, objects[index], targets[index])

def trainingProcess(eichWert, learning_rate, amount_to_train):
    objects, targets = object_collection(eichWert, amount_to_train)
    neuron = create(2)
    learning(neuron, objects, targets, learning_rate)
    saveTrainData(trainData=neuron)

def recognisationProcess(neuron= [], amount_to_measure=1, eichWert=1):
    for x in range(amount_to_measure):
        print("Put a screw under cam, to be measured!")
        screwType = output(neuron, recognisation(Image.open(imageCapture(device=1)), eichWert)[0])
        if screwType == 0:
            print("Die Schraube ist kurz")
        else:
            print("Die Schraube ist lang")

def main():
    eichWert = calibrateCamera(sizeEichObjectMM=21)

    #trainingProcess(eichWert, 10000000, 20)

    neuron = loadTrainData()
    recognisationProcess(neuron, 5, eichWert)

if __name__ == "__main__":
    objects = []
    targets = []
    main()