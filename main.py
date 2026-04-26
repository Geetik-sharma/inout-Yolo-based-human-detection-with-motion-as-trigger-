import os
import time as t
os.chdir(os.path.dirname(os.path.abspath(__file__)))

from radar_sim import start_radar
from camera_capture import capture_image
from ai_detect import detect_human, save_annotated_image
from event_manager import create_event

print("""
╔══════════════════════════════════════╗
║       VIGILCORE SYSTEM STARTING      ║
║  Radar → Camera → AI → Dashboard     ║
╚══════════════════════════════════════╝
""")

def on_detection():
    print("\n[PIPELINE] ═══ PIPELINE TRIGGERED ═══")
    pipeline_start = t.time()

    # Step 1 — Capture
    step1_start = t.time()
    print("[PIPELINE] Step 1 → Capturing image...")
    image_path, timestamp = capture_image()
    step1_time = round((t.time() - step1_start) * 1000)
    print(f"[PIPELINE] Step 1 done in {step1_time}ms")

    if not image_path:
        print("[PIPELINE] Camera failed. Returning to radar.\n")
        return

    # Step 2 — AI detection
    step2_start = t.time()
    print("[PIPELINE] Step 2 → Running AI detection...")
    human_found, confidence = detect_human(image_path)
    step2_time = round((t.time() - step2_start) * 1000)
    print(f"[PIPELINE] Step 2 done in {step2_time}ms")

    if not human_found:
        print("[PIPELINE] No human confirmed. Discarding.\n")
        return

    # Step 3 — Annotate
    step3_start = t.time()
    print("[PIPELINE] Step 3 → Saving annotated image...")
    annotated_path = save_annotated_image(image_path, timestamp)
    step3_time = round((t.time() - step3_start) * 1000)
    print(f"[PIPELINE] Step 3 done in {step3_time}ms")

    # Step 4 — Event
    step4_start = t.time()
    print("[PIPELINE] Step 4 → Creating event...")
    event = create_event(image_path, annotated_path, timestamp, confidence)
    step4_time = round((t.time() - step4_start) * 1000)
    print(f"[PIPELINE] Step 4 done in {step4_time}ms")

    total_time = round((t.time() - pipeline_start) * 1000)

    print(f"""
[PIPELINE] ═══ PIPELINE COMPLETE ═══
  Step 1  Camera capture    : {step1_time}ms
  Step 2  AI inference      : {step2_time}ms
  Step 3  Image annotation  : {step3_time}ms
  Step 4  Event creation    : {step4_time}ms
  ─────────────────────────────────
  Total pipeline latency    : {total_time}ms
  Confidence                : {int(confidence*100)}%
  Status                    : HUMAN DETECTED
═══════════════════════════════════\n""")

# ── Start radar (blocks here, fires on_detection on motion) ──
print("[VIGILCORE] Dashboard should be running at http://localhost:5000")
print("[VIGILCORE] Starting radar monitoring...\n")
start_radar(on_detection)