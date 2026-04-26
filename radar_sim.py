import cv2
import numpy as np
import time

# ── Settings ──────────────────────────────────────────
MOTION_THRESHOLD = 2500
COOLDOWN_SECONDS = 5
# ──────────────────────────────────────────────────────

def start_radar(on_detection_callback):
    cam = cv2.VideoCapture(0)

    if not cam.isOpened():
        print("[RADAR] ERROR: Cannot open camera.")
        return

    print("[RADAR] Radar started. Monitoring for motion...")
    print("[RADAR] Press CTRL+C to quit.\n")

    ret, frame1 = cam.read()
    ret, frame2 = cam.read()

    last_trigger_time = 0

    try:
        while True:
            diff = cv2.absdiff(frame1, frame2)
            gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
            blur = cv2.GaussianBlur(gray, (5, 5), 0)
            _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
            dilated = cv2.dilate(thresh, None, iterations=3)
            motion_score = np.sum(dilated)

            current_time = time.time()
            cooldown_active = (current_time - last_trigger_time) < COOLDOWN_SECONDS

            if cooldown_active:
                remaining = int(COOLDOWN_SECONDS - (current_time - last_trigger_time))
                print(f"\r[RADAR] Cooldown: {remaining}s remaining...   ", end="")
            else:
                print(f"\r[RADAR] Scanning... motion score: {int(motion_score)}   ", end="")

            if motion_score > MOTION_THRESHOLD and not cooldown_active:
                print(f"\n[RADAR] *** MOTION DETECTED *** Score: {int(motion_score)}")
                last_trigger_time = current_time
                cam.release()
                on_detection_callback()
                time.sleep(COOLDOWN_SECONDS)
                cam = cv2.VideoCapture(0)
                ret, frame1 = cam.read()
                ret, frame2 = cam.read()
                continue

            frame1 = frame2
            ret, frame2 = cam.read()
            if not ret:
                print("\n[RADAR] Camera read failed.")
                break

            time.sleep(0.05)

    except KeyboardInterrupt:
        print("\n[RADAR] Stopped by user.")

    finally:
        cam.release()


# ── Quick test ──
if __name__ == "__main__":
    def test_callback():
        print("[TEST] Pipeline would fire here!")
        print("[TEST] Returning to radar monitoring...\n")

    start_radar(test_callback)