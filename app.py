from flask import Flask, request, jsonify, redirect, render_template
from pymongo import MongoClient
import random
import string

app = Flask(__name__)
client = MongoClient("mongodb://localhost:27017/")
db = client["url_shortener"]
urls_collection = db["urls"]
def generate_short_code(length=6):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choices(characters, k=length))
def find_url_by_short_code(short_code):
    return urls_collection.find_one({"shortCode": short_code})

def find_url_by_original_url(original_url):
    return urls_collection.find_one({"url": original_url})
@app.route('/shorten', methods=['POST'])
def create_short_url():
    data = request.json
    original_url = data.get("url")
    
    if not original_url:
        return jsonify({"error": "URL is required"}), 400
    
    existing_url = find_url_by_original_url(original_url)
    if existing_url:
        return jsonify({
            "id": str(existing_url["_id"]),
            "url": existing_url["url"],
            "shortCode": existing_url["shortCode"]
        }), 200
    
    short_code = generate_short_code()
    while find_url_by_short_code(short_code):
        short_code = generate_short_code()
    
    url_data = {"url": original_url, "shortCode": short_code, "accessCount": 0}
    result = urls_collection.insert_one(url_data)
    
    return jsonify({
        "id": str(result.inserted_id),
        "url": original_url,
        "shortCode": short_code
    }), 201
