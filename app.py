from flask import Flask, request, jsonify, redirect, render_template
from pymongo import MongoClient
import random
import string

app = Flask(__name__)
