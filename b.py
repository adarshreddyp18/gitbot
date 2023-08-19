import os
import requests
from telegram import Bot, Update
from telegram.ext import CommandHandler, MessageHandler, filters, Updater, CallbackContext

TELEGRAM_TOKEN = "6504179423:AAErvZ5KBgsJwIGa6uIZxU0eDG5QXy5NReQ"
GITHUB_TOKEN = "new-user-18"
GITHUB_USERNAME = "new-user-18"

def create_repository(repo_name):
    url = "https://api.github.com/user/repos"
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    data = {
        "name": repo_name,
        "private": False  # Change to True if you want a private repository
    }
    
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 201:
        return "Repository created successfully."
    else:
        return "Error creating repository."

def delete_repository(repo_name):
    url = f"https://api.github.com/repos/{GITHUB_USERNAME}/{repo_name}"
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    response = requests.delete(url, headers=headers)
    
    if response.status_code == 204:
        return "Repository deleted successfully."
    elif response.status_code == 404:
        return "Repository not found."
    else:
        return "Error deleting repository."

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Use /create <repo_name> to create a new GitHub repository.")
    update.message.reply_text("Use /delete <repo_name> to delete a GitHub repository.")

def create(update: Update, context: CallbackContext) -> None:
    if len(context.args) != 1:
        update.message.reply_text("Usage: /create <repo_name>")
        return
    
    repo_name = context.args[0]
    result = create_repository(repo_name)
    update.message.reply_text(result)

def delete(update: Update, context: CallbackContext) -> None:
    if len(context.args) != 1:
        update.message.reply_text("Usage: /delete <repo_name>")
        return
    
    repo_name = context.args[0]
    result = delete_repository(repo_name)
    update.message.reply_text(result)

def main():
    updater = Updater(token=TELEGRAM_TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    
    start_handler = CommandHandler("start", start)
    create_handler = CommandHandler("create", create)
    delete_handler = CommandHandler("delete", delete)
    
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(create_handler)
    dispatcher.add_handler(delete_handler)
    
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()





