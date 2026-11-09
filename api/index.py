import os
import sys
import traceback

# Tambahkan root directory ke sys.path agar Vercel runtime selalu bisa mengimpor package 'app'
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

try:
    from app import create_app
    app = create_app()
except Exception as e:
    print(f"CRITICAL ERROR STARTING APP: {e}", flush=True)
    traceback.print_exc()
    from flask import Flask, jsonify
    from flask_cors import CORS

    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": "*"}})

    @app.route("/", defaults={"path": ""})
    @app.route("/<path:path>", methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"])
    def error_fallback(path):
        return jsonify({
            "success": False,
            "message": "Backend initialization failed",
            "error": str(e),
            "traceback": traceback.format_exc()
        }), 500
