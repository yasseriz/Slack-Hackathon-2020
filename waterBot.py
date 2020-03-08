from flask import request, Flask
import os
import slack
from threading import Thread
import json



Client = slack.WebClient(SLACK_BOT_USER_TOKEN)

app = Flask(__name__)

def backgroundworker(payload, userID,checkApp, userName):
	print(payload)

	workingDuration = payload['view']['state']['values']['workinghours']['workinghours']
	selectedDays = payload['view']['state']['values']['days']['days']['selected_option']
	duration = payload['view']['state']['values']['duration']['duration']['selected_option']['text']['text']

	message = " I've got your request, I shall remind you to drink water on" + "\n " + selectedDays + "\n every" +  duration + "\n during " + workingDuration
	Client.chat_postMessage(channel='general', text=message)

@app.route('/slack/getco', methods=['POST'])
def getco():

	print("Received something")
	print(request.form)
	payload = json.loads(request.form.get('payload'))
	checkApp = payload['view']['title']['text']
	userID = payload['user']['id']
	userName = payload['user']['username']
	
	thr = Thread(target=backgroundworker, args=[payload, userID, checkApp, userName])
	thr.start()
	return "",200

@app.route('/remindme', methods=['POST'])
def remindme():
	trigger_id = request.form.get('trigger_id')
	print(trigger_id)
	Client.views_open(
	trigger_id=trigger_id,
	view =
	 {
		"type": "modal",
		"title": {
			"type": "plain_text",
			"text": "Remind me to drink water",
			"emoji": True
		},
		"submit": {
			"type": "plain_text",
			"text": "Submit",
			"emoji": True
		},
		"close": {
			"type": "plain_text",
			"text": "Cancel",
			"emoji": True
		},
		"blocks": [
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
					},
					"action_id":"workinghours"
				},
				"label": {
					"type": "plain_text",
					"text": "Enter Working Hours (24 Hours)",
					"emoji": True
				},
				"block_id":"workinghours"
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
				"block_id":"days",
				"element": {
					"type": "multi_static_select",
					"placeholder": {
						"type": "plain_text",
						"text": "Select days",
						"emoji": True
					},
					"action_id":"days",
					"options": [
						{
							"text": {
								"type": "plain_text",
								"text": "Saturday",
								"emoji": True
							},
							"value": "saturday"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "Sunday",
								"emoji": True
							},
							"value": "sunday"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "Monday",
								"emoji": True
							},
							"value": "monday"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "Tuesday",
								"emoji": True
							},
							"value": "tuesday"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "Wednesday",
								"emoji": True
							},
							"value": "wednesday"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "Thursday",
								"emoji": True
							},
							"value": "thursday"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "Friday",
								"emoji": True
							},
							"value": "friday"
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
					"action_id":"duration",
					"options": [
						{
							"text": {
								"type": "plain_text",
								"text": "30 minutes",
								"emoji": True
							},
							"value": "minute30"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "1 hour",
								"emoji": True
							},
							"value": "hour1"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "4 hours",
								"emoji": True
							},
							"value": "hour2"
						}
					]
				},
				"label": {
					"type": "plain_text",
					"text": "Every..",
					"emoji": True
				},
				"block_id":"duration"
			}
		]
	 }
	)
	return "",200


if __name__ == "__main__":
  app.run(port=3000)