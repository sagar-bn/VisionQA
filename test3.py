import pyautogui
import time
import os

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.5

POSTMAN_PATH = r"C:\Users\KITS\AppData\Local\Postman\Postman.exe"

os.makedirs("responses", exist_ok=True)


def find_click(image):

    while True:

        try:
            location = pyautogui.locateCenterOnScreen(
                image,
                confidence=0.8,
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

    time.sleep(14)


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
    time.sleep(19)


def scroll_to_top():

    print("Scrolling to top")

    pyautogui.click()

    for _ in range(20):
        pyautogui.press("up")

    time.sleep(2)


def capture_each_request():

    print("Finding first result")

    first = None

    while first is None:
        first = pyautogui.locateOnScreen(
            "images/first_result.png",
            confidence=0.6,
            grayscale=True
        )
        time.sleep(1)

    processed = []
    count = 1

    current_top = first.top

    while True:

        results = list(pyautogui.locateAllOnScreen(
            "images/result_item.png",
            confidence=0.6,
            grayscale=True
        ))

        if not results:
            print("No results found")
            break

        # sort results top → bottom
        results = sorted(results, key=lambda r: r.top)

        found_new = False

        for r in results:

            # skip rows above the first result
            if r.top < current_top:
                continue

            if r in processed:
                continue

            pyautogui.click(pyautogui.center(r))

            time.sleep(2)

            filename = f"responses/request_{count}.png"
            pyautogui.screenshot(filename)

            print("Saved", filename)

            processed.append(r)

            current_top = r.top
            count += 1
            found_new = True

        if not found_new:

            print("Scrolling for more results")

            pyautogui.scroll(-500)
            time.sleep(2)

            new_rows = list(pyautogui.locateAllOnScreen(
                "images/result_item.png",
                confidence=0.6,
                grayscale=True
            ))

            if all(r in processed for r in new_rows):
                print("Reached end of results")
                break


open_postman()

start_collection()

scroll_to_top()

capture_each_request()