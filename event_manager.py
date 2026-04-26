import json
import os
import random
from datetime import datetime

# ── Settings ──────────────────────────────────────────
EVENTS_LOG = "events/events_log.json"

# Simulated UAV patrol coordinates around JSS Noida
# These simulate the UAV flying around — each trigger picks a slightly different spot
BASE_LAT = 28.5355
BASE_LON = 77.3910
# ──────────────────────────────────────────────────────

os.makedirs("events", exist_ok=True)


def get_simulated_gps():
    """
    Simulates UAV GPS position.
    Adds small random offset to base coordinates — mimics UAV moving around.
    """
    lat = BASE_LAT + random.uniform(-0.003, 0.003)
    lon = BASE_LON + random.uniform(-0.003, 0.003)
    return round(lat, 6), round(lon, 6)


def create_event(image_path, annotated_path, timestamp, confidence):
    """
    Packages all detection data into a structured event and saves to log.
    Returns the event dictionary.
    """

    lat, lon = get_simulated_gps()

    event = {
        "id": timestamp,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "latitude": lat,
        "longitude": lon,
        "confidence": confidence,
        "confidence_pct": f"{int(confidence * 100)}%",
        "image_path": image_path,
        "annotated_path": annotated_path,
        "sensor": "mmWave-SIM + RGB",
        "platform": "UAV-SIM",
        "status": "HUMAN DETECTED"
    }

    # Append event to log file
    with open(EVENTS_LOG, "a") as f:
        f.write(json.dumps(event) + "\n")

    print(f"[EVENT] Event created successfully!")
    print(f"[EVENT] ID         : {event['id']}")
    print(f"[EVENT] Time       : {event['timestamp']}")
    print(f"[EVENT] Location   : {lat}, {lon}")
    print(f"[EVENT] Confidence : {event['confidence_pct']}")
    print(f"[EVENT] Saved to   : {EVENTS_LOG}")

    return event


def get_all_events():
    """
    Reads all events from log and returns as a list.
    """
    events = []
    if not os.path.exists(EVENTS_LOG):
        return events

    with open(EVENTS_LOG, "r") as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    events.append(json.loads(line))
                except json.JSONDecodeError:
                    continue

    return events


def clear_events():
    """
    Clears all events — useful for fresh demo.
    """
    if os.path.exists(EVENTS_LOG):
        os.remove(EVENTS_LOG)
        print("[EVENT] All events cleared.")
    else:
        print("[EVENT] No events to clear.")


# ── Quick test ──
if __name__ == "__main__":
    print("Testing event creation...\n")

    # Use latest captured image for test
    folder = "events/images"
    annotated_folder = "events/annotated"

    img_files = sorted(os.listdir(folder)) if os.path.exists(folder) else []
    ann_files = sorted(os.listdir(annotated_folder)) if os.path.exists(annotated_folder) else []

    if not img_files:
        print("[TEST] No images found. Run camera_capture.py first.")
        exit(1)

    image_path = os.path.join(folder, img_files[-1])
    annotated_path = os.path.join(annotated_folder, ann_files[-1]) if ann_files else image_path
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Create a test event
    event = create_event(
        image_path=image_path,
        annotated_path=annotated_path,
        timestamp=timestamp,
        confidence=0.87
    )

    print("\n── All events in log ─────────────────")
    all_events = get_all_events()
    print(f"  Total events: {len(all_events)}")
    for e in all_events:
        print(f"  → {e['timestamp']} | {e['confidence_pct']} | {e['latitude']}, {e['longitude']}")
    print("──────────────────────────────────────")