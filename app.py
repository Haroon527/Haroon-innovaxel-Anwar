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
