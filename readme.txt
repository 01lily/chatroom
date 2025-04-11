# Secure Chatroom Web App (Localhost)

## Description
A secure, anonymous web-based chatroom with basic sentiment moderation using spaCy. Messages flagged with harmful content are stopped before being broadcast.

## Features
- Real-time chat using Flask-SocketIO
- AI-based sentiment filtering before message broadcast
- Anonymous usernames (no login)
- Fully local deployment for low-resource systems

## Setup Instructions

1. Clone or extract this project folder.
2. Open a terminal inside the folder.

### Step 1: Create virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate

### Step 2: Install required libraries
pip install -r requirements.txt
python -m spacy download en_core_web_sm

### Step 3: Run the application
python app.py

### Step 4: Open in browser
Visit http://localhost:5000 in your browser.

## Notes
- This is a prototype with basic sentiment filtering and does not store messages.
- Only lightweight models are used for compatibility with low-resource machines.
