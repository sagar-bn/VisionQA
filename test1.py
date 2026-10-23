import pyautogui
import time
import os

POSTMAN_PATH = r"C:\Users\KITS\AppData\Local\Postman\Postman.exe"

os.makedirs("responses", exist_ok=True)

def find_click(image):

    while True:

        location = pyautogui.locateCenterOnScreen(image, confidence=0.85)

        if location:
            pyautogui.click(location)
            return

        time.sleep(1)


def open_postman():

    os.startfile(POSTMAN_PATH)

    print("Opening Postman")

    time.sleep(15)


def start_collection():

    print("Clicking collection")

    find_click("images/collection.png")

    time.sleep(2)

    print("Click Run")

    find_click("images/run_button.png")

    time.sleep(3)

    print("Start run")

    find_click("images/run_collection.png")


def capture_each_request():

    count = 1

    time.sleep(10)

    while True:

        location = pyautogui.locateCenterOnScreen("images/result_item.png", confidence=0.8)

        if location:

            pyautogui.click(location)

            time.sleep(2)

            filename = f"responses/request_{count}.png"

            pyautogui.screenshot(filename)

            print("Saved", filename)

            pyautogui.press("down")

            count += 1

            time.sleep(2)

        else:

            break


open_postman()

start_collection()

capture_each_request()