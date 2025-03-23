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
@app.route('/<short_code>', methods=['GET'])
def redirect_to_url(short_code):
    url_data = find_url_by_short_code(short_code)
    if not url_data:
        return jsonify({"error": "Short URL not found"}), 404
    
    urls_collection.update_one({"shortCode": short_code}, {"$inc": {"accessCount": 1}})
    return redirect(url_data["url"])
@app.route('/shorten/<short_code>', methods=['DELETE'])
def delete_short_url(short_code):
    result = urls_collection.delete_one({"shortCode": short_code})
    if result.deleted_count == 0:
        return jsonify({"error": "Short URL not found"}), 404
    
    return jsonify({"message": "Short URL deleted successfully"}), 204
@app.route('/shorten/<short_code>', methods=['PUT'])
def update_short_url(short_code):
    data = request.json
    new_url = data.get("url")
    if not new_url:
        return jsonify({"error": "New URL is required"}), 400
    
    result = urls_collection.update_one(
        {"shortCode": short_code},
        {"$set": {"url": new_url}}
    )
    
    if result.matched_count == 0:
        return jsonify({"error": "Short URL not found"}), 404
    
    return jsonify({"message": "URL updated successfully"}), 200
@app.route('/shorten/<short_code>/stats', methods=['GET'])
def get_url_statistics(short_code):
    url_data = find_url_by_short_code(short_code)
    if not url_data:
        return jsonify({"error": "Short URL not found"}), 404
    
    return jsonify({
        "shortCode": url_data["shortCode"],
        "url": url_data["url"],
        "accessCount": url_data["accessCount"]
    }), 200
@app.route('/')
def home():
    return render_template('index.html')
