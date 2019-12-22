import time
import threading

import pyautogui


class Player:
    def __init__(self, id, up, left, right, reset, speed):
        self.id = id
        self.Up = up
        self.Left = left
        self.Right = right
        self.Reset = reset
        self.speed = speed
        self.currentButton = ""
        self.initial_frames = []
        self.states = {'right': False, 'center': False, 'left': False}
        self.timer = {'right': 0, 'center': 0, 'left': 0}

    def always_forward(self):
        def press_gas(rate):
            time.sleep(5)
            while True:
                pyautogui.keyDown(self.Up)
                time.sleep(rate)
                pyautogui.keyUp(self.Up)
        thread = threading.Thread(target=press_gas, args=(0.5,))
        thread.start()

    def turn_right(self):
        def press_right(rate):
            if self.timer['right'] < 2:
                self.timer['right'] += rate
            else:
                self.timer['right'] = 0
            self.timer['left'] = 0
            pyautogui.keyDown(self.Right)
            time.sleep(self.timer['right'])
            pyautogui.keyUp(self.Right)
            self.states['right'] = False

        thread = threading.Thread(target=press_right, args=(0.15,))
        thread.start()

    def turn_left(self):
        def press_left(rate):
            if self.timer['left'] < 2:
                self.timer['left'] += rate
            else:
                self.timer['left'] = 0
            self.timer['right'] = 0
            pyautogui.keyDown(self.Left)
            time.sleep(self.timer['left'])
            pyautogui.keyUp(self.Left)
            self.states['left'] = False
        thread = threading.Thread(target=press_left, args=(0.15,))
        thread.start()

    def handle_movement(self):
        right = self.states['right']
        left = self.states['left']
        if right and not left:
            self.turn_right()
        if left and not right:
            self.turn_left()


