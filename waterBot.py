from flask import request, Flask
import os
import slack
import boto3

SLACK_OAUTH_TOKEN = 'xoxp-974374833842-975694945859-977110332049-6bdaffad547d073d5ce15bc317c6b8c8'
SLACK_BOT_USER_TOKEN = 'xoxb-974374833842-975733718883-vws19XWIo8MnLmczqPMQejym'

Client = slack.WebClient(SLACK_BOT_USER_TOKEN)

app = Flask(__name__)

@app.route('/remindme', methods=['POST'])
def remindme():
    Client.chat_postMessage(channel='general', text='TEST')
    return "",200