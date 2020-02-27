# -*- coding: utf-8 -*-
"""
In this file, we'll create a python Bot Class.
"""
import os
import json
import slack


class Bot(object):
    """ Instantiates a Bot object to handle Slack interactions."""

    def __init__(self):
        super(Bot, self).__init__()
        # When we instantiate a new bot object, we can access the app
        # credentials we set earlier in our local development environment.
        self.oauth = {"client_id": os.environ.get("CLIENT_ID"),
                      "client_secret": os.environ.get("CLIENT_SECRET"),
                      # Scopes provide and limit permissions to what our app
                      # can access. It's important to use the most restricted
                      # scope that your app will need.
                      "scope": "app_mentions:read,calls:read,calls:write,channels:history,channels:join,"
                               "channels:manage,channels:read,chat:write,commands,dnd:read,emoji:read,files:read,"
                               "files:write,groups:history,groups:read,groups:write,im:history,im:read,im:write,"
                               "incoming-webhook,links:read,links:write,mpim:history,mpim:read,mpim:write,pins:read,"
                               "pins:write,reactions:read,reactions:write,reminders:read,reminders:write,"
                               "remote_files:read,remote_files:share,remote_files:write,team:read,usergroups:read,"
                               "usergroups:write,usergroups:read,users:read,users:read.email,users:write",
                      "signing_secret": os.environ.get("SIGNING_SECRET")}
        self.verification = os.environ.get("VERIFICATION_TOKEN")
        self.client = slack.WebClient(token="")
        self.bot_user_id = ""

    def auth(self, code):
        if code:
            auth_response = self.client.oauth_v2_access(client_id=self.oauth.get('client_id'),
                                                        client_secret=self.oauth.get('client_secret'),
                                                        code=code)

            # We'll save the bot_user_id to check incoming messages mentioning our bot
            self.bot_user_id = auth_response["bot_user_id"]
            self.client = slack.WebClient(auth_response["access_token"])
            return ""
        else:
            return "Authentication failed: did not go through with install."

    def say_hello(self, message):
        hello_message = "I want to live! Please build me."
        message_attachments = [
            {
                "pretext": "I'll tell you how to set up your system. :robot_face:",
                "text": "What operating system are you using?",
                "callback_id": "os",
                "color": "#3AA3E3",
                "attachment_type": "default",
                "actions": [
                    {
                        "name": "mac",
                        "text": ":apple: Mac",
                        "type": "button",
                        "value": "mac"
                    },
                    {
                        "name": "windows",
                        "text": ":fax: Windows",
                        "type": "button",
                        "value": "win"
                    }
                ]
            }
        ]
        channel = message["channel"]
        self.client.chat_postMessage(channel=channel,
                                     text=hello_message,
                                     attachments=message_attachments)

    def show_win(self):
        message = {
            "as_user": False,
            "replace_original": False,
            "response_type": "ephemeral",
            "text": ":fax: *Windows OS*:\n Here's some helpful tips for "
                    "setting up the requirements you'll need for this workshop:",
            "attachments": [{
                "mrkdwn_in": ["text", "pretext"],
                "text": "*Python 2.7 and Pip*:\n_Check to see if you have "
                        "Python on your system:_\n```python --version```\n_Download "
                        "link:_\nhttps://www.python.org/ftp/python/2.7.12/python-2.7.1"
                        "2.msi\n_Make sure to tick  `Add Python.exe to PATH` when "
                        "installing Python for Windows._\n_If that doesn't add it to "
                        "the path after installation, run this command:_\n```c:\pyth"
                        "on27\\tools\scripts\win_add2path.py```\n_After downloading "
                        "Python, you must upgrade your version of Pip:_\n```python "
                        "-m pip install -U pip```\n*Virtualenv*:\n_Check to see if "
                        "you have virtualenv on your system and install it if you "
                        "don't have it:_\n```virtualenv --version\npip install "
                        "virtualenv```\n*Ngrok:*\n_Check to see if you have ngrok on "
                        "your system:_\n```ngrok --version```\n_Download "
                        "Link:_\nhttps://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable"
                        "-darwin-amd64.zip\nTo unzip on Windows, just double click "
                        "ngrok.zip",
                "footer": "Slack API: Build this Bot Workshop",
                "footer_icon": "https://platform.slack-edge.com/img/default"
                               "_application_icon.png"
            }]}
        return json.dumps(message)

    def show_mac(self):
        """
        A method to respond to a user's action taken from a message button.
        Returns a message with system setup instructions for building this bot
        on a Mac operating system.
        """
        message = {
            "as_user": False,
            "replace_original": False,
            "response_type": "ephemeral",
            "text": ":apple: *Mac OS*:\n Here's some helpful tips for "
                    "setting up the requirements you'll need for this workshop:",
            "attachments": [{
                "mrkdwn_in": ["text", "pretext"],
                "text": "*Python 2.7 and Pip*:\n_Check to see if you have "
                        "Python on your system:_\n```which python && python "
                        "--version```\n_If you have homebrew, you can use it to "
                        "install python and pip:_\n```brew install python && pip```"
                        "\n_If not, you can download python here:_Download link:_\n"
                        "https://www.python.org/ftp/python/2.7.12/python-2.7.12-"
                        "macosx10.6.pkg\n_After downloading Python, you must upgrade "
                        "your version of Pip:_\n```pip install -U pip```\n"
                        "*Virtualenv*:\n_Check to see if you have virtualenv on your "
                        "system and install it if you don't have it:_\n```which "
                        "virtualenv\npip install virtualenv```\n*Ngrok:*\n_Check "
                        "to see if you have ngrok on your system:_\n```which ngrok"
                        "```\n_Download Link:_\nhttps://bin.equinox.io/c/4VmDzA7iaHb"
                        "/ngrok-stable-darwin-amd64.zip\n```unzip /path/to/ngrok.zip"
                        "\ncd /usr/local/bin\nln -s /path/to/ngrok ngrok```",
                "footer": "Slack API: Build this Bot Workshop",
                "footer_icon": "https://platform.slack-edge.com/img/default"
                               "_application_icon.png"
            }]
        }
        return json.dumps(message)

