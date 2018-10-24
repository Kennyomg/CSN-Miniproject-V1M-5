from gpiozero import LED, Button, DigitalInputDevice
from threading import Thread
from time import sleep
from enum import Enum
from requests import get
from signal import pause

is_pincode_correct = False

ledRed = LED(2)
ledYellow = LED(3)
ledBlue = LED(4)
buttonRed = Button(14)
buttonBlack = Button(15)
buttonYellow = Button(18)
buttonBlue = Button(17)
buttonGreen = Button(27)
magnetSensor = DigitalInputDevice(22)


class Color(Enum):
    RED = 1
    BLACK = 2
    YELLOW = 3
    BLUE = 4
    GREEN = 5


def alarm_countdown():
    global is_pincode_correct
    global ledRed
    global ledYellow
    global ledBlue

    ledRed.off()
    ledYellow.blink()

    timer = 10
    while True:
        if is_pincode_correct:
            ledBlue.on()
            ledYellow.off()
            break
        elif timer == 0:
            ledRed.on()
            ledYellow.off()
            get("192.168.42.2:8000")
            break
        else:
            timer -= 1
            sleep(1)


def set_pincode(color, pincode_list):
    pincode_list.append(color)


def mainProgram():

    global ledRed
    global ledYellow
    global ledBlue
    global buttonRed
    global buttonBlack
    global buttonYellow
    global buttonBlue
    global buttonGreen
    global magnetSensor

    global is_pincode_correct

    pincode = []
    input_pincode = []

    is_pincode_set = False

    ledRed.off()
    ledYellow.off()
    ledBlue.off()

    isRedPressed = False
    isBlackPressed = False
    isYellowPressed = False
    isBluePressed = False
    isGreenPressed = False

    isMagnetSensorActive = False

    def changeRed():
        nonlocal isRedPressed
        isRedPressed = True

    def changeBlack():
        nonlocal isBlackPressed
        isBlackPressed = True

    def changeYellow():
        nonlocal isYellowPressed
        isYellowPressed = True

    def changeBlue():
        nonlocal isBluePressed
        isBluePressed = True

    def changeGreen():
        nonlocal isGreenPressed
        isGreenPressed = True

    def changeMagnet():
        nonlocal is_pincode_set
        nonlocal isMagnetSensorActive

        if is_pincode_set:
            isMagnetSensorActive = True
            myThread = Thread(target=alarm_countdown)
            myThread.start()

    buttonRed.when_activated = changeRed
    buttonBlack.when_activated = changeBlack
    buttonYellow.when_activated = changeYellow
    buttonBlue.when_activated = changeBlue
    buttonGreen.when_activated = changeGreen

    #buttonRed.when_activated = ledBlue.on
    #buttonRed.when_deactivated = ledBlue.off

    magnetSensor.when_activated = lambda: [changeMagnet()]
    #magnetSensor.when_deactivated = ledRed.off

    ledYellow.on()

    while True:
        if not is_pincode_set:
            if isRedPressed:
                pincode.append(Color.RED)
                print("RED")
                isRedPressed = False
            if isBlackPressed:
                pincode.append(Color.BLACK)
                print("BLACK")
                isBlackPressed = False
            if isYellowPressed:
                pincode.append(Color.YELLOW)
                print("YELLOW")
                isYellowPressed = False
            if isBluePressed:
                pincode.append(Color.BLUE)
                print("BLUE")
                isBluePressed = False
            if isGreenPressed:
                print("Pincode set\n", pincode)
                is_pincode_set = True
                isGreenPressed = False
                ledYellow.off()
                ledRed.blink()
        elif isMagnetSensorActive:
            if isRedPressed:
                input_pincode.append(Color.RED)
                isRedPressed = False
            if isBlackPressed:
                input_pincode.append(Color.BLACK)
                isBlackPressed = False
            if isYellowPressed:
                input_pincode.append(Color.YELLOW)
                isYellowPressed = False
            if isBluePressed:
                input_pincode.append(Color.BLUE)
                isBluePressed = False
            if isGreenPressed:
                if input_pincode == pincode:
                    input_pincode = []
                    is_pincode_correct = True
                else:
                    input_pincode = []
                isGreenPressed = False


mainProgram()
