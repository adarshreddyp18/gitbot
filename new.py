import os
import requests
from flask import Flask, request

app = Flask(__name__)
#using flask
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
GITHUB_TOKEN = os.environ.get("GITHUB_API_TOKEN")
REPO_OWNER = "your_username"
REPO_NAME = "your_repository"

if not TELEGRAM_TOKEN or not GITHUB_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN and GITHUB_API_TOKEN must be set as environment variables")

def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": chat_id, "text": text}
    response = requests.post(url, json=data)
    
    if response.status_code != 200:
        print(f"Failed to send message to Telegram. Response: {response.text}")

def add_collaborator(username):
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/collaborators/{username}"
    headers = {"Authorization": f"Bearer {GITHUB_TOKEN}"}
    response = requests.put(url, headers=headers)
    
    if response.status_code == 204:
        return "Collaborator added successfully."
    elif response.status_code == 404:
        return "User not found."
    elif response.status_code == 422:
        return "User is already a collaborator."
    else:
        return "Error adding collaborator."

def remove_collaborator(username):
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/collaborators/{username}"
    headers = {"Authorization": f"Bearer {GITHUB_TOKEN}"}
    response = requests.delete(url, headers=headers)
    
    if response.status_code == 204:
        return "Collaborator removed successfully."
    elif response.status_code == 404:
        return "User not found."
    elif response.status_code == 403:
        return "Permission denied."
    else:
        return "Error removing collaborator."

@app.route(f"/{TELEGRAM_TOKEN}", methods=["POST"])
def webhook():
    data = request.json
    chat_id = data["message"]["chat"]["id"]
    message_text = data["message"]["text"]
    
    if message_text.startswith("/add"):
        username = message_text.split("/add")[1].strip()
        result = add_collaborator(username)
        send_message(chat_id, result)
    elif message_text.startswith("/remove"):
        username = message_text.split("/remove")[1].strip()
        result = remove_collaborator(username)
        send_message(chat_id, result)
    else:
        send_message(chat_id, "Unknown command. Use /add or /remove followed by a GitHub username.")

    return {"status": "ok"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
