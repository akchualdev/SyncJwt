from flask import Flask, jsonify, request
from flask_caching import Cache
from app.utils.response import process_token
from colorama import init
import warnings
from urllib3.exceptions import InsecureRequestWarning
import time

# Ignore SSL warnings
warnings.filterwarnings("ignore", category=InsecureRequestWarning)

# Initialize colorama
init(autoreset=True)

# Initialize Flask app
app = Flask(__name__)

cache = Cache(app, config={"CACHE_TYPE": "simple"})  # In-memory cache

@app.route("/")
def home():
    return "JWT Token Generator API is running!"

@app.route("/token", methods=["GET"])
def get_responses():
    uid = request.args.get("uid")
    password = request.args.get("password")

    if uid and password:
        # Generate a unique cache key per request using a timestamp
        cache_key = f"token_{uid}_{password}_{int(time.time())}"

        response = process_token(uid, password)
        cache.set(
            cache_key, response, timeout=25200
        )  # Cache response with 7-hour expiry
        return jsonify(response)

    # Bulk retrieval logic removed as per request
    return jsonify({"message": "Bulk retrieval logic has been removed."})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5030)
