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


def find_results_panel():

    print("Locating results panel")

    panel = None

    while panel is None:

        try:
            panel = pyautogui.locateOnScreen(
                "images/results_panel_header.png",
                confidence=0.6,
                grayscale=True
            )
        except:
            pass

        time.sleep(1)

    print("Results panel found:", panel)

    return panel


# def capture_each_request():

#     panel = find_results_panel()

#     screen_w, screen_h = pyautogui.size()

#     # dynamic scanning region
#     scan_region = (
#     panel.left,
#     panel.top + 80,   # start slightly below header
#     panel.width,
#     panel.height - 120
#     )

#     print("Scan region:", scan_region)

#     print("Searching first request number...")

#     current = None

#     while current is None:

#         try:
#             current = pyautogui.locateOnScreen(
#                 "images/request_anchor.png",
#                 region=scan_region,
#                 confidence=0.5,
#                 grayscale=True
#             )
#         except:
#             pass

#         if current is None:
#             print("Still searching for first request...")

#         time.sleep(1)

#     print("First request found:", current)

#     count = 1

#     while True:

#         x, y = pyautogui.center(current)

#         # click slightly below the number
#         pyautogui.click(x, y + 10)

#         time.sleep(2)

#         filename = f"responses/request_{count}.png"

#         pyautogui.screenshot(filename)

#         print("Saved", filename)

#         search_region = (
#             current.left,
#             current.top + current.height,
#             scan_region[2],
#             scan_region[3]
#         )

#         next_item = None

#         try:
#             next_item = pyautogui.locateOnScreen(
#                 "images/request_anchor.png",
#                 region=search_region,
#                 confidence=0.5,
#                 grayscale=True
#             )
#         except:
#             pass

#         if next_item is None:

#             print("Scrolling for more requests")

#             pyautogui.scroll(-500)
#             time.sleep(2)

#             try:
#                 next_item = pyautogui.locateOnScreen(
#                     "images/request_anchor.png",
#                     region=scan_region,
#                     confidence=0.5,
#                     grayscale=True
#                 )
#             except:
#                 pass

#             if next_item is None:
#                 print("Reached end of results")
#                 break

#         current = next_item
#         count += 1
def capture_each_request():

    panel = find_results_panel()

    scan_region = (
        panel.left,
        panel.top + 80,
        panel.width,
        panel.height - 120
    )

    print("Searching first request")

    current = None

    while current is None:
        try:
            current = pyautogui.locateOnScreen(
                "images/request_anchor.png",  # image of "[" or "[1]"
                region=scan_region,
                confidence=0.5,
                grayscale=True
            )
        except:
            pass

        time.sleep(1)

    count = 1

    while True:

        x, y = pyautogui.center(current)

        pyautogui.click(x, y + 10)

        time.sleep(2)

        filename = f"responses/request_{count}.png"
        pyautogui.screenshot(filename)

        print("Saved", filename)

        search_region = (
            current.left,
            current.top + current.height,
            panel.width,
            panel.height
        )

        next_item = None

        while next_item is None:

            try:
                next_item = pyautogui.locateOnScreen(
                    "images/request_anchor.png",
                    region=search_region,
                    confidence=0.5,
                    grayscale=True
                )
            except:
                pass

            if next_item is None:
                pyautogui.scroll(-50)
                time.sleep(1)

                try:
                    next_item = pyautogui.locateOnScreen(
                        "images/request_anchor.png",
                        region=scan_region,
                        confidence=0.5,
                        grayscale=True
                    )
                except:
                    pass

                if next_item is None:
                    print("Reached end of requests")
                    return

        current = next_item
        count += 1

open_postman()

start_collection()

scroll_to_top()

capture_each_request()