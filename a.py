import requests

TELEGRAM_TOKEN = "6504179423:AAErvZ5KBgsJwIGa6uIZxU0eDG5QXy5NReQ"
GITHUB_TOKEN = "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"
REPO_OWNER = "new-user-18"
REPO_NAME = "new-repo"

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
    
    if response.status_code == 201:
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

def main():
    print("Telegram Bot for GitHub Collaboration Management")
    while True:
        command = input("Enter a command (/add or /remove): ")
        if command == "/add":
            username = input("Enter GitHub username to add as a collaborator: ")
            result = add_collaborator(username)
            print(result)
        elif command == "/remove":
            username = input("Enter GitHub username to remove as a collaborator: ")
            result = remove_collaborator(username)
            print(result)
        else:
            print("Unknown command. Use /add or /remove followed by a GitHub username.")

if __name__ == "__main__":
    main()
