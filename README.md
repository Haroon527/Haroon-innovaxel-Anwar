# Haroon-innovaxel-Anwar
# URL Shortening Service

## Overview
This is a simple URL Shortening Service built with Flask and MongoDB. The service provides a RESTful API to shorten long URLs, retrieve original URLs, update or delete shortened URLs, and track usage statistics.

## Features
- Create a short URL for a given long URL
- Retrieve the original URL from a short URL
- Update an existing short URL
- Delete a short URL
- Track the number of times a short URL has been accessed
- Minimal frontend for interacting with the API

## Tech Stack
- **Backend**: Flask (Python)
- **Database**: MongoDB
- **Frontend**: HTML, JavaScript (Optional for testing)

## API Endpoints

### 1. Create Short URL
**Endpoint:** `POST /shorten`
#### Request Body:
```json
{
  "url": "https://www.example.com/some/long/url"
}
```
#### Response:
```json
{
  "id": "1",
  "url": "https://www.example.com/some/long/url",
  "shortCode": "abc123"
}
```

### 2. Retrieve Original URL
**Endpoint:** `GET /shorten/{shortCode}`
#### Response:
```json
{
  "id": "1",
  "url": "https://www.example.com/some/long/url",
  "shortCode": "abc123"
}
```

### 3. Update Short URL
**Endpoint:** `PUT /shorten/{shortCode}`
#### Request Body:
```json
{
  "url": "https://www.example.com/some/updated/url"
}
```
#### Response:
```json
{
  "message": "URL updated successfully"
}
```

### 4. Delete Short URL
**Endpoint:** `DELETE /shorten/{shortCode}`
#### Response:
```json
{
  "message": "Short URL deleted successfully"
}
```

### 5. Get URL Statistics
**Endpoint:** `GET /shorten/{shortCode}/stats`
#### Response:
```json
{
  "shortCode": "abc123",
  "url": "https://www.example.com/some/long/url",
  "accessCount": 10
}
```

## Setup Instructions

### 1. Clone the Repository
```sh
git clone https://github.com/your-repo/url-shortener.git
cd url-shortener
```

### 2. Install Dependencies
Make sure you have Python installed, then install required packages:
```sh
pip install -r requirements.txt
```

### 3. Run MongoDB Locally
Make sure MongoDB is installed and running on your machine.
```sh
mongod --dbpath /your/mongo/db/path
```

### 4. Run the Application
```sh
python app.py
```
The server will start at `http://127.0.0.1:5000`

## Future Enhancements
- Implement authentication and authorization
- Add custom short URL aliases
- Implement analytics dashboard

## License
This project is open-source and available under the MIT License.

