import pyautogui
import time
import os

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.3

POSTMAN_PATH = r"C:\Users\KITS\AppData\Local\Postman\Postman.exe"

os.makedirs("responses", exist_ok=True)

# ── Tune this value during testing ──────────────────────────
SCROLL_AMOUNT = 5   # how many scroll steps down after each screenshot
# ────────────────────────────────────────────────────────────


def find_click(image, confidence=0.7):
    while True:
        try:
            location = pyautogui.locateCenterOnScreen(
                image, confidence=confidence, grayscale=True
            )
            if location:
                pyautogui.click(location)
                return
        except Exception:
            pass
        time.sleep(1)


def open_postman():
    os.startfile(POSTMAN_PATH)
    print("Opening Postman...")
    time.sleep(8)


def start_collection():
    print("Clicking collection tab...")
    find_click("images/collection.png")
    time.sleep(3)

    print("Clicking Run button...")
    find_click("images/run_button.png")
    time.sleep(2)

    print("Starting collection run...")
    find_click("images/run_collection.png")

    print("Waiting for collection run to finish...")
    time.sleep(15)


def scroll_to_top():

    print("Scrolling results to top")

    pyautogui.click()

    for _ in range(40):
        pyautogui.press("up")

    time.sleep(2)


def locate_request(image_path):
    """Try to find the reference image on screen. Returns (x, y) or None."""
    try:
        location = pyautogui.locateCenterOnScreen(
            image_path,
            confidence=0.7,
            grayscale=True
        )
        return location
    except Exception:
        return None


def capture_each_request():
    """
    For each reference image in requests/request_1.png, request_2.png ...
      1. Locate it on screen (scroll down if not visible)
      2. Click 10px below it
      3. Screenshot → save to responses/request_N.png
      4. Scroll down SCROLL_AMOUNT to reveal next request
    """

    # Count how many reference images exist
    ref_images = []
    i = 1
    while True:
        path = f"requests/request_{i}.png"
        if os.path.exists(path):
            ref_images.append(path)
            i += 1
        else:
            break

    if not ref_images:
        print("No reference images found in requests/ folder. Exiting.")
        return

    print(f"Found {len(ref_images)} reference image(s). Starting capture...\n")

    for idx, ref_image in enumerate(ref_images, start=1):

        print(f"[{idx}/{len(ref_images)}] Looking for: {ref_image}")

        # --- Step 1: Locate reference image, scroll down if not yet visible ---
        location = None
        scroll_attempts = 0
        MAX_SCROLL_ATTEMPTS = 30  # safety: won't scroll forever

        while location is None and scroll_attempts < MAX_SCROLL_ATTEMPTS:
            location = locate_request(ref_image)

            if location is None:
                print(f"  Not visible yet, scrolling down... (attempt {scroll_attempts + 1})")
                pyautogui.click(700, 400)   # keep focus on results panel
                pyautogui.scroll(-30)        # scroll down a little
                time.sleep(0.8)
                scroll_attempts += 1

        if location is None:
            print(f"  Could not find {ref_image} after scrolling. Skipping.")
            continue

        # --- Step 2: Click 10px below the located position ---
        rx, ry = location
        print(f"  Found at ({rx}, {ry}), clicking at ({rx}, {ry + 100})")
        pyautogui.locateCenterOnScreen
        time.sleep(2)   # wait for detail panel to load

        # --- Step 3: Screenshot ---
        filename = f"responses/request_{idx}.png"
        pyautogui.screenshot(filename)
        print(f"  Saved {filename}")

        # --- Step 4: Scroll down to reveal next request ---
        print(f"  Scrolling down {SCROLL_AMOUNT} steps...")
        pyautogui.click(700, 400)
        for _ in range(SCROLL_AMOUNT):
            pyautogui.scroll(-30)
            time.sleep(0.2)

open_postman()
start_collection()
scroll_to_top()
capture_each_request()
# ```c

# **Folder structure needed:**
# ```
# project/
# ├── images/
# │   ├ccc── collection.png
# │   ├── run_button.png
# │   └c── run_collection.png
# ├── requests/
# │   ├── request_1.png   ← your cropped reference images
# │   ├── request_2.png
# │   ├── request_3.png
# │   └── ...
# ├── responses/          ← screenshots saved here automatically
# └── script.py