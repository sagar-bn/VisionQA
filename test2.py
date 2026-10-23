import pyautogui
import time
import os

POSTMAN_PATH = r"C:\Users\KITS\AppData\Local\Postman\Postman.exe"

os.makedirs("responses", exist_ok=True)

def find_click(image):

    while True:

        # location = pyautogui.locateCenterOnScreen(image, confidence=0.8)
        location = pyautogui.locateCenterOnScreen(image, confidence=0.55, grayscale=True)
        if location:
            pyautogui.click(location)
            return

        time.sleep(1)


def open_postman():

    os.startfile(POSTMAN_PATH)

    print("Opening Postman")

    time.sleep(6)


def start_collection():

    print("Clicking collection")
    find_click("images/collection.png")

    time.sleep(2)

    print("Click Run")
    find_click("images/run_button.png")

    time.sleep(2)

    print("Start run")
    find_click("images/run_collection.png")

    print("Waiting for collection run to finish...")
    time.sleep(10)


def scroll_to_top():

    print("Scrolling to top")

    pyautogui.click()  

    for _ in range(40):
        pyautogui.press("up")

    time.sleep(2)

# def capture_each_request():

#     print("Capturing responses")

#     count = 1

#     methods = [
#         "images/method_get.png",
#         "images/method_post.png"
#     ]

#     processed = []

#     while True:

#         found = []

#         for m in methods:

#             found += list(pyautogui.locateAllOnScreen(
#                 m,
#                 confidence=0.6,
#                 grayscale=True
#             ))

#         if not found:
#             break

#         for item in found:

#             if item in processed:
#                 continue

#             x = item.left + 200
#             y = item.top + 10

#             pyautogui.click(x, y)

#             time.sleep(2)

#             filename = f"responses/request_{count}.png"

#             pyautogui.screenshot(filename)

#             print("Saved", filename)

#             processed.append(item)

#             count += 1

#         pyautogui.scroll(-500)

#         time.sleep(2)
def capture_each_request():

    print("Finding first result")

    first = None

    while first is None:
        first = pyautogui.locateCenterOnScreen(
            "images/first_result.png",
            confidence=0.6,
            grayscale=True
        )
        time.sleep(1)

    current = first
    count = 1

    while True:

        pyautogui.click(current)

        time.sleep(2)

        filename = f"responses/request_{count}.png"
        pyautogui.screenshot(filename)

        print("Saved", filename)

        # search area below current result
        region = (
            current.left,
            current.top + 40,
            600,
            400
        )

        next_item = pyautogui.locateOnScreen(
            "images/result_item.png",
            region=region,
            confidence=0.6,
            grayscale=True
        )

        if next_item is None:
            print("No more results")
            break

        current = next_item
        count += 1
###


open_postman()

start_collection()

scroll_to_top()

capture_each_request()