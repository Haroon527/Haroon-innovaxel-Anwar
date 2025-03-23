from flask import Flask, request, jsonify, redirect, render_template
from pymongo import MongoClient
import random
import string

app = Flask(__name__)
client = MongoClient("mongodb://localhost:27017/")
db = client["url_shortener"]
urls_collection = db["urls"]
