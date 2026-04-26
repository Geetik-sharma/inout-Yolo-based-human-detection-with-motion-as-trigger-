from ultralytics import YOLO
import cv2
import os

# ── Settings ──────────────────────────────────────────
CONFIDENCE_THRESHOLD = 0.50  # minimum confidence to count as detection
# ──────────────────────────────────────────────────────

# Load model once when file is imported (not every detection)
print("[AI] Loading YOLOv8 model...")
model = YOLO("yolov8n.pt")  # downloads automatically on first run (~6MB)
print("[AI] Model ready.")


def detect_human(image_path):
    """
    Runs YOLOv8 on the given image.
    Returns (True, confidence) if human found, (False, 0.0) if not.
    """

    if not os.path.exists(image_path):
        print(f"[AI] ERROR: Image not found at {image_path}")
        return False, 0.0

    print(f"[AI] Analyzing image: {image_path}")

    results = model(image_path, verbose=False)

    best_confidence = 0.0
    human_found = False

    for result in results:
        for i, cls in enumerate(result.boxes.cls):
            if int(cls) == 0:  # class 0 = person in COCO dataset
                confidence = float(result.boxes.conf[i])
                print(f"[AI] Human detected! Confidence: {confidence:.2f}")
                if confidence > best_confidence:
                    best_confidence = confidence
                if confidence >= CONFIDENCE_THRESHOLD:
                    human_found = True

    if not human_found:
        print(f"[AI] No human detected above threshold ({CONFIDENCE_THRESHOLD})")

    return human_found, round(best_confidence, 2)


def save_annotated_image(image_path, timestamp):
    """
    Saves a copy of the image with detection boxes drawn on it.
    Returns path to annotated image.
    """
    results = model(image_path, verbose=False)

    annotated_folder = "events/annotated"
    os.makedirs(annotated_folder, exist_ok=True)

    annotated_path = os.path.join(annotated_folder, f"annotated_{timestamp}.jpg")

    for result in results:
        annotated_frame = result.plot()  # draws boxes on image
        cv2.imwrite(annotated_path, annotated_frame)
        print(f"[AI] Annotated image saved: {annotated_path}")
        break

    return annotated_path


# ── Quick test ──
if __name__ == "__main__":
    import sys

    # If image path passed as argument use it, otherwise use latest captured image
    if len(sys.argv) > 1:
        test_image = sys.argv[1]
    else:
        # Auto-find the latest image in events/images/
        folder = "events/images"
        if not os.path.exists(folder):
            print("[TEST] No events/images folder found.")
            print("[TEST] Run camera_capture.py first to capture an image.")
            sys.exit(1)

        files = sorted(os.listdir(folder))
        if not files:
            print("[TEST] No images found in events/images/")
            print("[TEST] Run camera_capture.py first.")
            sys.exit(1)

        test_image = os.path.join(folder, files[-1])
        print(f"[TEST] Using latest image: {test_image}\n")

    # Run detection
    found, confidence = detect_human(test_image)

    # Save annotated version
    timestamp = test_image.split("_")[-1].replace(".jpg", "")
    annotated = save_annotated_image(test_image, timestamp)

    # Result summary
    print("\n── Detection Result ──────────────────")
    print(f"  Human found    : {found}")
    print(f"  Confidence     : {confidence * 100:.0f}%")
    print(f"  Annotated image: {annotated}")
    print("──────────────────────────────────────")

    if found:
        print("\n[TEST] PIPELINE WOULD PROCEED → creating event")
    else:
        print("\n[TEST] PIPELINE WOULD STOP → no human confirmed")