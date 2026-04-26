import cv2
import os
import time
from datetime import datetime

# ── Settings ──────────────────────────────────────────
SAVE_FOLDER = "events/images"
CAPTURE_DELAY = 1.5
# ──────────────────────────────────────────────────────

def capture_image():
    os.makedirs(SAVE_FOLDER, exist_ok=True)

    print("[CAMERA] Activating camera...")
    cam = cv2.VideoCapture(0)

    if not cam.isOpened():
        print("[CAMERA] ERROR: Cannot open camera.")
        return None, None

    # Warm up
    for i in range(10):
        cam.read()

    time.sleep(CAPTURE_DELAY)

    ret, frame = cam.read()
    cam.release()

    if not ret or frame is None:
        print("[CAMERA] ERROR: Failed to capture frame.")
        return None, None

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"img_{timestamp}.jpg"
    filepath = os.path.join(SAVE_FOLDER, filename)

    cv2.imwrite(filepath, frame)

    if os.path.exists(filepath):
        size_kb = os.path.getsize(filepath) // 1024
        print(f"[CAMERA] Image saved: {filepath} ({size_kb} KB)")
        return filepath, timestamp
    else:
        print("[CAMERA] ERROR: Image failed to save.")
        return None, None


# ── Quick test ──
if __name__ == "__main__":
    print("Testing camera capture...\n")
    path, ts = capture_image()

    if path:
        print(f"\n[TEST] Success!")
        print(f"[TEST] File path : {path}")
        print(f"[TEST] Timestamp : {ts}")
        print(f"\n[TEST] Check your VigilCore/events/images/ folder.")
    else:
        print("\n[TEST] Capture failed. Check error above.")