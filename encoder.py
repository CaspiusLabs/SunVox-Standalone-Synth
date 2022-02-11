#!/usr/bin/env python
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
from time import sleep
import uinput

Enc_Pin_A = 20 # ENCODER CWR
Enc_Pin_B = 26 # ENCODER CCWR
Enc_Pin_C = 21 # ENTER

Touch_Pin_A = 17 # CTRL
Touch_Pin_B = 27 # SHIFT
Touch_Pin_C = 22 # DOT
Touch_Pin_D = 10 # F10
Touch_Pin_E = 9  # F9
Touch_Pin_F = 11 # F12

Device = uinput.Device([
    uinput.KEY_UP,
    uinput.KEY_DOWN,
    uinput.KEY_LEFT,
    uinput.KEY_RIGHT,
    uinput.KEY_ENTER,
    uinput.KEY_RIGHTCTRL,
    uinput.KEY_RIGHTSHIFT,
    uinput.KEY_DOT,
    uinput.KEY_F10,
    uinput.KEY_F9,
    uinput.KEY_F12
])

LastItem = (0,1,1)
Item = 0
CtrlCombo = ShiftCombo = False


def init():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)

    GPIO.setup(Enc_Pin_A, GPIO.IN)
    GPIO.setup(Enc_Pin_B, GPIO.IN)
    GPIO.setup(Enc_Pin_C, GPIO.IN)

    GPIO.setup(Touch_Pin_A, GPIO.IN)
    GPIO.setup(Touch_Pin_B, GPIO.IN)
    GPIO.setup(Touch_Pin_C, GPIO.IN)
    GPIO.setup(Touch_Pin_D, GPIO.IN)
    GPIO.setup(Touch_Pin_E, GPIO.IN)
    GPIO.setup(Touch_Pin_F, GPIO.IN)

    GPIO.add_event_detect(Enc_Pin_A, GPIO.RISING, callback=encoder_interrupt, bouncetime=1)
    GPIO.add_event_detect(Enc_Pin_B, GPIO.RISING, callback=encoder_interrupt, bouncetime=1)
    GPIO.add_event_detect(Enc_Pin_C, GPIO.RISING, callback=encoder_interrupt, bouncetime=1)

    GPIO.add_event_detect(Touch_Pin_A, GPIO.BOTH, callback=touchsensor_interrupt, bouncetime=1)
    GPIO.add_event_detect(Touch_Pin_B, GPIO.BOTH, callback=touchsensor_interrupt, bouncetime=1)
    GPIO.add_event_detect(Touch_Pin_C, GPIO.RISING, callback=touchsensor_interrupt, bouncetime=1)
    GPIO.add_event_detect(Touch_Pin_D, GPIO.RISING, callback=touchsensor_interrupt, bouncetime=1)
    GPIO.add_event_detect(Touch_Pin_E, GPIO.RISING, callback=touchsensor_interrupt, bouncetime=1)
    GPIO.add_event_detect(Touch_Pin_F, GPIO.RISING, callback=touchsensor_interrupt, bouncetime=1)


def encoder_interrupt(Pin):
    global Item, LastItem

    if Pin == Enc_Pin_A:
        Item = (Pin, 1, GPIO.input(Enc_Pin_B))
    if Pin == Enc_Pin_B:
        Item = (Pin, GPIO.input(Enc_Pin_A),1)
    if Pin == Enc_Pin_C:
        Device.emit_click(uinput.KEY_ENTER)
        #print("ENTER")

    if Item == (Enc_Pin_A,1,1) and LastItem[1] == 0:
        if CtrlCombo:
            Device.emit_click(uinput.KEY_LEFT)
            #print("LEFT")
        else:
            Device.emit_click(uinput.KEY_DOWN)
            #print("DOWN")

    elif Item == (Enc_Pin_B,1,1) and LastItem[2] == 0:
        if CtrlCombo:
            Device.emit_click(uinput.KEY_RIGHT)
            #print("RIGHT")
        else:
            Device.emit_click(uinput.KEY_UP)
            #print("UP")

    LastItem = Item


def touchsensor_interrupt(Pin):
    global CtrlCombo, ShiftCombo

    if Pin == Touch_Pin_A:
        if CtrlCombo:
            Device.emit_click(uinput.KEY_RIGHTCTRL)
            #print("CTRL")
            CtrlCombo = False
        else:
            CtrlCombo = True

    if Pin == Touch_Pin_B:
        if ShiftCombo:
            Device.emit_click(uinput.KEY_RIGHTSHIFT)
            #print("SHIFT")
            ShiftCombo = False
        else:
            ShiftCombo = True

    if Pin == Touch_Pin_C:
        if CtrlCombo:
            Device.emit_combo([uinput.KEY_RIGHTCTRL, uinput.KEY_DOT])
            #print(">")
        elif ShiftCombo:
            Device.emit_combo([uinput.KEY_RIGHTSHIFT, uinput.KEY_DOT])
            #print("<")
        else:
            Device.emit_click(uinput.KEY_DOT)
            #print("DOT")

    if Pin == Touch_Pin_D:
        if CtrlCombo:
            Device.emit_combo([uinput.KEY_RIGHTCTRL, uinput.KEY_F10])
            #print("CTRL+F10")
        elif ShiftCombo:
            Device.emit_combo([uinput.KEY_RIGHTSHIFT, uinput.KEY_F10])
            #print("SHIFT+F10")
        else:
            Device.emit_click(uinput.KEY_F10)
            #print("F10")

    if Pin == Touch_Pin_E:
        if CtrlCombo:
            Device.emit_combo([uinput.KEY_RIGHTCTRL, uinput.KEY_F9])
            #print("CTRL+F9")
        elif ShiftCombo:
            Device.emit_combo([uinput.KEY_RIGHTSHIFT, uinput.KEY_F9])
            #print("SHIFT+F9")
        else:
            Device.emit_click(uinput.KEY_F9)
            #print("F9")

    if Pin == Touch_Pin_F:
        if CtrlCombo:
            Device.emit_combo([uinput.KEY_RIGHTCTRL, uinput.KEY_F12])
            #print("CTRL+F12")
        elif ShiftCombo:
            Device.emit_combo([uinput.KEY_RIGHTSHIFT, uinput.KEY_F12])
            #print("SHIFT+F12")
        else:
            Device.emit_click(uinput.KEY_F12)
            #print("F12")


try:
    init()
    while True:
        sleep(0.01)
except KeyboardInterrupt:
    GPIO.cleanup()
