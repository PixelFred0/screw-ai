from PIL import Image 
import random
import cv2 as cv
import json
import os

def cls(): #clear the console
    os.system('cls' if os.name=='nt' else 'clear')

def saveTrainData(trainData = [], file = "data.json"):
    if not os.path.isfile(file):
        print("data.json was created!")
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
    try:
        with open(file) as f:
            data = json.load(f)
            fileTrainData = data["trainData"]
        return fileTrainData
    except FileNotFoundError:
        print("There is no data.json file  with your Training Data in the directory!")
        return False

def imageCapture(device = 0, file_name = "frame"):
    cam = cv.VideoCapture(device)
    cv.namedWindow("Capture Picture")
    capture_process = True
    while capture_process:
        ret, frame = cam.read()
        if not ret:
            print("failed to grab frame")
            capture_process = False
        cv.imshow("Capture Picture", frame)
        k = cv.waitKey(1)
        if k%256 == 27:
            # ESC pressed
            print("Escape pressed, closing...")
            capture_process = False
        elif k%256 == 13:
            # Enter pressed
            img_name = f"{file_name}.png"
            cv.imwrite(img_name, frame)
            print("Enter was pressed, Image captured ...")
            capture_process = False
    cam.release()
    cv.destroyAllWindows()
    return f"{file_name}.png"

def calibrateCamera(sizeEichObjectMM):
    print("""### Cam Calibration ###\n
          1. Create a white Background (for instance a peace of paper)\n
          2. Put a 5 cent coin underneath the Camera\n
          3. Press Enter to capture the Image!""")
    image = Image.open(imageCapture(device=1))
    x = recognisation(image, 1)[1]
    print(x/sizeEichObjectMM)
    eichWert = sizeEichObjectMM/x
    print("Don't move the camera!")
    return eichWert

def eichen(boundingBox, eichWert):
    for i in range(len(boundingBox)):
      boundingBox[i] = boundingBox[i] * eichWert 
    return boundingBox

def object_collection(eichWert, amount_to_train):
    for i in range(amount_to_train):
        print(f"Capture {i+1}. image")
        print("Press Enter to capture the Image!")
        image = Image.open(imageCapture(device=1))
        objects.append(recognisation(image, eichWert)[0])
        target = input("Enter 1 for long or 0 for short: " )
        targets.append(int(target))
        cls()
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
    print(f"Try to use {amount_to_train//2} Picture's for the long Object and\n {amount_to_train-(amount_to_train//2)} Picture's for the short Object")
    objects, targets = object_collection(eichWert, amount_to_train)
    neuron = create(2)
    print("Training Process is running, please wait ...")
    learning(neuron, objects, targets, learning_rate)
    saveTrainData(trainData=neuron)

def recognisationProcess(neuron= [], amount_to_measure=1, eichWert=1):
    for x in range(amount_to_measure):
        print(f"{x+1}. Recognition")
        print("Put a Object under the cam, to be measured!")
        screwType = output(neuron, recognisation(Image.open(imageCapture(device=1)), eichWert)[0])
        if screwType == 0:
            print("The Object is short")
        else:
            print("The Object is long")
        unused = input("Do you want to continue? ")
        cls()

def main():
    cls()
    user_continue = True
    unused = input(menu["Introduction"])
    cls()
    eichWert = calibrateCamera(sizeEichObjectMM=23)
    while user_continue:
        cls()
        user_process_selection = input(menu["Main-Menu"]).strip()
        cls()
        if user_process_selection == "1": #Training
            user_amount_to_train = int(input("How many Object's do you want to use for training (Recommended 20 or more):"))
            trainingProcess(eichWert, 10000000, user_amount_to_train)
        elif user_process_selection == "2": #Recognison
            neuron = loadTrainData()
            if neuron:
                user_amount_objects = int(input("How many Objects do you want to recognise?: "))
                recognisationProcess(neuron, user_amount_objects, eichWert)
        elif user_process_selection == "3": #Calibrate
            eichWert = calibrateCamera(sizeEichObjectMM=23)
        else:
            print("Your Choice was not in the Menu range from 1 to 3!")
        user_continue = input("Do you want to close the Programm?(Y/N)")
        if user_continue.lower() in ["y","yes"]:
            user_continue = False
        else:
            user_continue = True

if __name__ == "__main__":
    objects = []
    targets = []
    menu = {"Introduction": 
            '''#### Welcome to the Size detector ###\n
            1. Connect a Cam to your Computer  \n
            2. Point the Cam towards a white Backround\n
            3. You need to run the Cam calibration\n
            Press Enter to continue: ''',
            "Main-Menu": """###### Main Menu ######\n
              1. Train the detection-model\n
              2. Recognise Objectsize\n
              3. Calibrate Cam (Recommende if the cam was moved!)\n
              What do you want to do (answer with the Menu number): 
              """,}
    main()