import pyautogui
import time
import os

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.4

POSTMAN_PATH = r"C:\Users\KITS\AppData\Local\Postman\Postman.exe"

os.makedirs("responses", exist_ok=True)


def find_click(image):

    while True:
        try:
            location = pyautogui.locateCenterOnScreen(
                image,
                confidence=0.7,
                grayscale=True
            )

            if location:
                pyautogui.click(location)
                return

        except:
            pass

        time.sleep(1)


def open_postman():

    os.startfile(POSTMAN_PATH)

    print("Opening Postman")
    time.sleep(8)


def start_collection():

    print("Clicking collection")
    find_click("images/collection.png")

    time.sleep(3)

    print("Click Run")
    find_click("images/run_button.png")

    time.sleep(2)

    print("Start run")
    find_click("images/run_collection.png")

    print("Waiting for collection run to finish...")
    time.sleep(15)


def scroll_to_top():

    print("Scrolling results to top")

    pyautogui.click()

    for _ in range(40):
        pyautogui.press("up")

    time.sleep(2)


def find_focus():

    focus = None

    while focus is None:

        try:
            focus = pyautogui.locateCenterOnScreen(
                "images/tab_focus.png",
                confidence=0.8,
                
            )
        except:
            pass

        time.sleep(2)

    return focus


def capture_each_request():

    print("Processing requests using stored images")

    count = 1

    while True:

        img_path = f"requests/request_{count}.png"

        if not os.path.exists(img_path):
            print("No more request images found.")
            break

        print(f"Searching for request {count}")

        location = None
        attempts = 0

        while location is None and attempts < 10:

            try:
                location = pyautogui.locateCenterOnScreen(
                    img_path,
                    confidence=0.7,
                    grayscale=True
                )
            except:
                pass

            if location is None:
                attempts += 1
                pyautogui.scroll(-40)
                time.sleep(1)

        if location is None:
            print(f"Request {count} not found, skipping")
            count += 1
            continue

        x, y = location

        pyautogui.click(x, y + 10)

        time.sleep(2)

        filename = f"responses/response_{count}.png"

        pyautogui.screenshot(filename)

        print("Saved", filename)

        count += 1
open_postman()
start_collection()
scroll_to_top()
capture_each_request()