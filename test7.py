import pyautogui
import time
import os

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.4

POSTMAN_PATH = r"C:\Users\KITS\AppData\Local\Postman\Postman.exe"

os.makedirs("responses", exist_ok=True)


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
    For each reference image requests/request_1.png, request_2.png ...
      1. Scroll to top using UP arrow (like original code)
      2. Locate reference image on screen
      3. Click 10px below it
      4. Screenshot → responses/request_N.png
      5. Press DOWN arrow once to prepare for next request
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

        print(f"[{idx}/{len(ref_images)}] Processing: {ref_image}")

        # --- Step 1: Scroll to top using UP arrow (your original style) ---
        print("  Scrolling to top...")
        pyautogui.click()
        for _ in range(40):
            pyautogui.press("up")
        time.sleep(2)

        # --- Step 2: Locate reference image, press DOWN if not yet visible ---
        location = None
        down_attempts = 0
        MAX_DOWN_ATTEMPTS = 100  # safety limit

        while location is None and down_attempts < MAX_DOWN_ATTEMPTS:
            location = locate_request(ref_image)

            if location is None:
                print(f"  Not visible, pressing DOWN... (attempt {down_attempts + 1})")
                pyautogui.press("down")
                time.sleep(0.3)
                down_attempts += 1

        if location is None:
            print(f"  Could not find {ref_image} after scrolling. Skipping.")
            continue

        # --- Step 3: Click 10px below the located position ---
        rx, ry = location
        print(f"  Found at ({rx}, {ry}), clicking ({rx}, {ry + 10})")
        pyautogui.click(rx, ry + 10)
        time.sleep(2)

        # --- Step 4: Screenshot ---
        filename = f"responses/request_{idx}.png"
        pyautogui.screenshot(filename)
        print(f"  Saved {filename}")

        # --- Step 5: Press DOWN once to shift view for next request ---
        pyautogui.press("down")
        time.sleep(0.5)

    print(f"\nDone. Captured {len(ref_images)} request(s).")


open_postman()
start_collection()
scroll_to_top()
capture_each_request()
# ```

# **The flow per request:**
# ```
# scroll UP ×40        → reset to top
# press DOWN until     → request image found on screen
# click (x, y+10)      → select the request
# screenshot           → save to responses/
# press DOWN ×1        → nudge view for next iteration