from flask import request, Flask
import os
import slack

SLACK_OAUTH_TOKEN = 'xoxp-974374833842-975694945859-986809404900-6552916ad83acf3d3f217bc2b3b33882'
SLACK_BOT_USER_TOKEN = 'xoxb-974374833842-975733718883-cU3GDLRlhHorebv82p82lmL7'

Client = slack.WebClient(SLACK_BOT_USER_TOKEN)

app = Flask(__name__)

@app.route('/slack/getco', methods=['POST'])
def getco():
    return "",200

@app.route('/remindme', methods=['POST'])
def remindme():
    Client.chat_postMessage(channel='general', text='TEST')
    return "",200

    views = {
        [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "*Let waterbot remind you to drink water :smile:*"
            }
        },
        {
            "type": "divider"
        },
        {
            "type": "input",
            "element": {
                "type": "plain_text_input",
                "placeholder": {
                    "type": "plain_text",
                    "text": "eg. 10-19",
                    "emoji": True
                }
            },
            "label": {
                "type": "plain_text",
                "text": "Enter Working Hours (24 Hours)",
                "emoji": True
            }
        },
        {
            "type": "divider"
        },
        {
            "type": "input",
            "label": {
                "type": "plain_text",
                "text": "Select days to be reminded on",
                "emoji": True
            },
            "element": {
                "type": "multi_static_select",
                "placeholder": {
                    "type": "plain_text",
                    "text": "Select days",
                    "emoji": True
                },
                "options": [
                    {
                        "text": {
                            "type": "plain_text",
                            "text": "Saturday",
                            "emoji": True
                        },
                        "value": "value-0"
                    },
                    {
                        "text": {
                            "type": "plain_text",
                            "text": "Sunday",
                            "emoji": True
                        },
                        "value": "value-1"
                    },
                    {
                        "text": {
                            "type": "plain_text",
                            "text": "Monday",
                            "emoji": True
                        },
                        "value": "value-2"
                    },
                    {
                        "text": {
                            "type": "plain_text",
                            "text": "Tuesday",
                            "emoji": True
                        },
                        "value": "value-3"
                    },
                    {
                        "text": {
                            "type": "plain_text",
                            "text": "Wednesday",
                            "emoji": True
                        },
                        "value": "value-4"
                    },
                    {
                        "text": {
                            "type": "plain_text",
                            "text": "Thursday",
                            "emoji": True
                        },
                        "value": "value-5"
                    },
                    {
                        "text": {
                            "type": "plain_text",
                            "text": "Friday",
                            "emoji": True
                        },
                        "value": "value-2"
                    }
                ]
            }
        },
        {
            "type": "divider"
        },
        {
            "type": "input",
            "element": {
                "type": "static_select",
                "placeholder": {
                    "type": "plain_text",
                    "text": "Select duration",
                    "emoji": True
                },
                "options": [
                    {
                        "text": {
                            "type": "plain_text",
                            "text": "30 minutes",
                            "emoji": True
                        },
                        "value": "value-0"
                    },
                    {
                        "text": {
                            "type": "plain_text",
                            "text": "1 hour",
                            "emoji": True
                        },
                        "value": "value-1"
                    },
                    {
                        "text": {
                            "type": "plain_text",
                            "text": "4 hours",
                            "emoji": True
                        },
                        "value": "value-2"
                    }
                ]
            },
            "label": {
                "type": "plain_text",
                "text": "Every..",
                "emoji": True
            }
        }
        ] 
    }

