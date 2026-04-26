from flask import Flask, jsonify, send_file, render_template
from event_manager import get_all_events
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('dashboard.html')

@app.route('/events')
def events():
    return jsonify(get_all_events())

@app.route('/image/<path:image_path>')
def get_image(image_path):
    # Try annotated first, fall back to original
    if os.path.exists(image_path):
        return send_file(image_path, mimetype='image/jpeg')
    return "Image not found", 404

@app.route('/clear')
def clear():
    from event_manager import clear_events
    clear_events()
    return jsonify({"status": "cleared"})

if __name__ == '__main__':
    print("[DASHBOARD] Starting VigilCore dashboard...")
    print("[DASHBOARD] Open your browser at: http://localhost:5000")
    app.run(debug=False, port=5000)