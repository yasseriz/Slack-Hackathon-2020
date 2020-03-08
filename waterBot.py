from flask import request, Flask
import os
import slack
from threading import Thread
import json

SLACK_BOT_USER_TOKEN = "<YOUR_SLACK_BOT_USER_TOKEN>"
Client = slack.WebClient(SLACK_BOT_USER_TOKEN)

app = Flask(__name__)

def backgroundworker(payload, userID, checkApp, userName):
	print(payload)

	# workingDuration = payload['view']['state']['values']['workinghours']['workinghours']['value']
	startingTime = payload['view']['state']['values']['startingTime']['startingTime']['selected_option']['value']
	endingTime = payload['view']['state']['values']['endingTime']['endingTime']['selected_option']['value']
	selectedDays = payload['view']['state']['values']['days']['days']['selected_options']
	duration = payload['view']['state']['values']['duration']['duration']['selected_option']['text']['text']

	message = " I've got your request, I shall remind you to drink water on" + "\n " + str(selectedDays) + "\n every " +  str(duration) + " starting from " + str(startingTime) + " to " + str(endingTime)
	Client.chat_postMessage(channel='general', text=message, token= '<YOUR_OAUTH_TOKEN>')

@app.route('/slack/getco', methods=['POST'])
def getco():

	print("Received something")
	# print(request.form)
	payload = json.loads(request.form.get('payload'))
	checkApp = payload['view']['title']['text']
	userID = payload['user']['id']
	userName = payload['user']['username']
	
	thr = Thread(target=backgroundworker, args=[payload, userID, checkApp, userName])
	thr.start()
	return "", 200

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
			"text": "Set :droplet: Breaks",
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
					"text": "*Hi There! I'm :watermelon:WaterMeLot:watermelon:,* \n*Your Friendly Neighbourhood Bot that tells you to drink water. *\n*With a few simple steps, You'll be hydrated in no time!*" #\n*Introduce Yourself to :watermelon:WaterMeLot:watermelon: :smile:*"
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
						"text": "Select Starting Time",
						"emoji": True
					},
					"action_id": "startingTime",
					"options": [
						{
							"text": {
								"type": "plain_text",
								"text": "8 AM"
							},
							"value": "8am"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "9 AM"
							},
							"value": "9am"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "10 AM"
							},
							"value": "10am"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "11 AM"
							},
							"value": "11am"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "12 PM"
							},
							"value": "12pm"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "1 PM"
							},
							"value": "1pm"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "2 PM"
							},
							"value": "2pm"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "3 PM"
							},
							"value": "3pm"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "4 PM"
							},
							"value": "4pm"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "5 PM"
							},
							"value": "5pm"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "6 PM"
							},
							"value": "6pm"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "7 PM"
							},
							"value": "7pm"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "8 PM"
							},
							"value": "8pm"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "9 PM"
							},
							"value": "9pm"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "10 PM"
							},
							"value": "10pm"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "11 PM"
							},
							"value": "11pm"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "12 AM"
							},
							"value": "12am"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "1 AM"
							},
							"value": "1am"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "2 AM"
							},
							"value": "2am"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "3 AM"
							},
							"value": "3am"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "4 AM"
							},
							"value": "4am"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "5 AM"
							},
							"value": "5am"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "6 AM"
							},
							"value": "6am"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "7 AM"
							},
							"value": "7am"
						}
					]
				},
				"label": {
					"type": "plain_text",
					"text": ":female-office-worker::skin-tone-4: What Time Do You Start Work?:male-office-worker:",
					"emoji": True
				},
				"block_id": "startingTime"

			},
			{
				"type": "input",
				"element": {
					"type": "static_select",
					"placeholder": {
						"type": "plain_text",
						"text": "Select Ending Time",
						"emoji": True
					},
					"action_id": "endingTime",
					"options": [
						{
							"text": {
								"type": "plain_text",
								"text": "8 AM"
							},
							"value": "8am"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "9 AM"
							},
							"value": "9am"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "10 AM"
							},
							"value": "10am"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "11 AM"
							},
							"value": "11am"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "12 PM"
							},
							"value": "12pm"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "1 PM"
							},
							"value": "1pm"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "2 PM"
							},
							"value": "2pm"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "3 PM"
							},
							"value": "3pm"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "4 PM"
							},
							"value": "4pm"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "5 PM"
							},
							"value": "5pm"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "6 PM"
							},
							"value": "6pm"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "7 PM"
							},
							"value": "7pm"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "8 PM"
							},
							"value": "8pm"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "9 PM"
							},
							"value": "9pm"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "10 PM"
							},
							"value": "10pm"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "11 PM"
							},
							"value": "11pm"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "12 AM"
							},
							"value": "12am"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "1 AM"
							},
							"value": "1am"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "2 AM"
							},
							"value": "2am"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "3 AM"
							},
							"value": "3am"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "4 AM"
							},
							"value": "4am"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "5 AM"
							},
							"value": "5am"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "6 AM"
							},
							"value": "6am"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "7 AM"
							},
							"value": "7am"
						}
					]
				},
				"label": {
					"type": "plain_text",
					"text": ":construction_worker::skin-tone-3: What Time Do You End Work? :female-construction-worker::skin-tone-2:",
					"emoji": True
				},
				"block_id": "endingTime"
			},
			{
				"type": "divider"
			},
			{
				"type": "input",
				"label": {
					"type": "plain_text",
					"text": ":male-factory-worker::skin-tone-6:When Do You Work?:female-factory-worker::skin-tone-3:",
					"emoji": True
				},
				"block_id": "days",
				"element": {
					"type": "multi_static_select",
					"placeholder": {
						"type": "plain_text",
						"text": "Select Days",
						"emoji": True
					},
					"action_id": "days",
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
					"action_id": "duration",
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
								"text": "2 hours",
								"emoji": True
							},
							"value": "hour2"
						}
					]
				},
				"label": {
					"type": "plain_text",
					"text": ":droplet:How Often Do You Want To Drink?:droplet:",
					"emoji": True
				},
				"block_id": "duration"
			}
		]
	}
	)
	return "",200


if __name__ == "__main__":
  app.run(port=3000)