from PIL import Image
import os
import cv2
import time



def createTrainData():
  trainData = []
  for file in os.listdir(path="./schrauben/"):
    # load image
    image = Image.open(f"./schrauben/{file}")
    # extract label
    fileLabel = file.split("_")[1].removesuffix(".jpg")
    if fileLabel.lower() == "l":
       fileLabel = 1
    else:
       fileLabel = 0 
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
    trainData.append([x,y,fileLabel])
    print (f"Bounding Box for file: {file} : ",x,y)
  return trainData

def create(size):
    from random import random
    neuron = []
    for i in range(size+1):
        neuron.append(random())
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
    error = (output(neuron, input) - (target))
    for i in range(len(input)):
        neuron[i] = (neuron[i] - (input[i] * error))
    neuron[len(input)] = neuron[len(input)] - error
    print(neuron)


dataSet = [
    [363, 198, 1],
    [343, 255, 1],
    [303, 213, 0],
    [306, 165, 0]
]

test_dataSet = [
    [363, 198],
    [306, 165]
]

# dataSet = createTrainData()

# model = create(2)

# for data in dataSet:
#     train(model, data[0:1], data[len(data)-1])

# for data in test_dataSet:
#      print(output(model, data))



