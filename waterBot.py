from flask import request, Flask
import os
import slack
from threading import Thread
import json
import calendar
import time
from datetime import datetime

SLACK_BOT_USER_TOKEN = 'xoxb-974374833842-975733718883-7oEpBjSk9B92qE4CBWOw9Sfr'
Client = slack.WebClient(SLACK_BOT_USER_TOKEN)

app = Flask(__name__)

def backgroundworker(payload, userID, checkApp, userName):
	# print(payload)
	scheduledList = Client.chat_scheduledMessages_list()['scheduled_messages']
	for i in range(len(scheduledList)):
		try:
			Client.chat_deleteScheduledMessage(channel=scheduledList[i]['channel_id'], scheduled_message_id=scheduledList[i]['id'])
		except:
			pass

	startingTime = payload['view']['state']['values']['startingTime']['startingTime']['selected_option']['value']
	startingTimeStr = payload['view']['state']['values']['startingTime']['startingTime']['selected_option']['text']['text']
	endingTime = payload['view']['state']['values']['endingTime']['endingTime']['selected_option']['value']
	endingTimeStr = payload['view']['state']['values']['endingTime']['endingTime']['selected_option']['text']['text']

	selectedDays = payload['view']['state']['values']['days']['days']['selected_options']
	reminderDays = []
	for i in range(len(selectedDays)):
		reminderDays.append(calendar.day_name[(int(selectedDays[i]['value']))])
	duration = payload['view']['state']['values']['duration']['duration']['selected_option']['text']['text']
	waitingTime = payload['view']['state']['values']['duration']['duration']['selected_option']['value']

	# calculate the amount of time needed to wait
	if waitingTime == "minute30":
		waitFor = 30 * 60
	elif waitingTime == "hour1":
		waitFor = 60 * 60
	elif waitingTime == "hour2":
		waitFor = 120 * 60
		

	dayString = ""
	for i in range(len(reminderDays)):
		if i != len(reminderDays) - 1: 
			dayString += reminderDays[i] + "s, "
		else:
			dayString += reminderDays[i] + "s"

	message = ":watermelon:WaterMeLot:watermelon: here. I've got your request, I shall remind you to drink water on *" + dayString + "* every *" +  str(duration) + "* starting from *" + str(startingTimeStr) + "* to *" + str(endingTimeStr) + "*"
	Client.chat_postMessage(channel='general', text=message, token= 'xoxp-974374833842-975694945859-977717198561-68bf11c6366bf5f6979db26b46a77c68')
	reminderMessage = ":droplet::droplet::droplet::droplet::droplet::droplet::droplet::droplet::droplet::droplet::droplet::droplet::droplet:\n:watermelon:WaterMeLot:watermelon: here. *It's Water Time! Drink Up and Stay Hydrated!*\n:droplet::droplet::droplet::droplet::droplet::droplet::droplet::droplet::droplet::droplet::droplet::droplet::droplet:"
	# Client.chat_scheduleMessage(channel='general', text=reminderMessage, token= 'xoxp-974374833842-975694945859-977717198561-68bf11c6366bf5f6979db26b46a77c68', post_at = 1583685067)
	# schedules a message, using post_at  (fking UNIX timestamp)
	
	# we add a offset to the timestamp because by the time the request reaches the api, it will be in the past
	timeLower = datetime.strptime(startingTime,'%H%M')
	timeLower = datetime.now().replace(hour=timeLower.hour, minute=timeLower.minute, second=timeLower.second)
	print(timeLower.hour)
	timeUpper = datetime.strptime(endingTime,'%H%M')
	timeUpper = datetime.now().replace(hour=timeUpper.hour, minute=timeUpper.minute, second=timeUpper.second)
	print(timeUpper.hour)

	# totalHours = timeUpper.hour - timeLower.hour
	
	# can only schedule up to 120 days, any more would throw an error
	current = int(time.time()) + 20
	while True:
		try:
			current = int(time.time()) + 20
			# only schedule if the it falls on the corresponding day of the week
			if ep_to_day(current) in reminderDays and time.localtime(current).tm_hour >= timeLower.hour and time.localtime(current).tm_hour <= timeUpper.hour:
				# Client.chat_scheduleMessage(channel='general', text=reminderMessage, token= 'xoxp-974374833842-975694945859-977717198561-68bf11c6366bf5f6979db26b46a77c68', post_at = current)
				Client.chat_postMessage(channel='general', text=reminderMessage, token= 'xoxp-974374833842-975694945859-977717198561-68bf11c6366bf5f6979db26b46a77c68')
				# current = current + waitFor
				# print(Client.chat_scheduledMessages_list()['scheduled_messages'])
				time.sleep(waitFor)


		except:
			break

def ep_to_day(ep):
    return datetime.fromtimestamp(ep/1000).strftime("%A")


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
							"value": "0800"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "9 AM"
							},
							"value": "0900"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "10 AM"
							},
							"value": "1000"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "11 AM"
							},
							"value": "1100"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "12 PM"
							},
							"value": "1200"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "1 PM"
							},
							"value": "1300"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "2 PM"
							},
							"value": "1400"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "3 PM"
							},
							"value": "1500"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "4 PM"
							},
							"value": "1600"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "5 PM"
							},
							"value": "1700"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "6 PM"
							},
							"value": "1800"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "7 PM"
							},
							"value": "1900"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "8 PM"
							},
							"value": "2000"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "9 PM"
							},
							"value": "2100"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "10 PM"
							},
							"value": "2200"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "11 PM"
							},
							"value": "2300"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "12 AM"
							},
							"value": "0000"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "1 AM"
							},
							"value": "0100"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "2 AM"
							},
							"value": "0200"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "3 AM"
							},
							"value": "0300"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "4 AM"
							},
							"value": "0400"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "5 AM"
							},
							"value": "0500"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "6 AM"
							},
							"value": "0600"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "7 AM"
							},
							"value": "0700"
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
							"value": "800"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "9 AM"
							},
							"value": "900"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "10 AM"
							},
							"value": "1000"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "11 AM"
							},
							"value": "1100"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "12 PM"
							},
							"value": "1200"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "1 PM"
							},
							"value": "1300"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "2 PM"
							},
							"value": "1400"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "3 PM"
							},
							"value": "1500"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "4 PM"
							},
							"value": "1600"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "5 PM"
							},
							"value": "1700"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "6 PM"
							},
							"value": "1800"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "7 PM"
							},
							"value": "1900"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "8 PM"
							},
							"value": "2000"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "9 PM"
							},
							"value": "2100"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "10 PM"
							},
							"value": "2200"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "11 PM"
							},
							"value": "2300"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "12 AM"
							},
							"value": "0000"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "1 AM"
							},
							"value": "0100"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "2 AM"
							},
							"value": "0200"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "3 AM"
							},
							"value": "0300"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "4 AM"
							},
							"value": "0400"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "5 AM"
							},
							"value": "0500"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "6 AM"
							},
							"value": "0600"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "7 AM"
							},
							"value": "0700"
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
							"value": "5"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "Sunday",
								"emoji": True
							},
							"value": "6"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "Monday",
								"emoji": True
							},
							"value": "0"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "Tuesday",
								"emoji": True
							},
							"value": "1"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "Wednesday",
								"emoji": True
							},
							"value": "2"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "Thursday",
								"emoji": True
							},
							"value": "3"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "Friday",
								"emoji": True
							},
							"value": "4"
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