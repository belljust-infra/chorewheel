#!/usr/bin/env python

from datetime import datetime
import csv
import sys
import os

import sendgrid
from sendgrid.helpers.mail import *

CHORES = [('Counters & Surfaces', 'Clean kitchen island, counters, dishwasher, and living room surfaces'),
	  ('Bathroom', 'Clean toilet, shower, mirrors, and sink'),
	  ('Stove, Fridge, & Pantry', 'Clean stove, interior of fridge, pantry surfaces, and microwave'),
	  ('Floors', 'Clean floors in kitchen, living room, bathroom, and hallway')]

# Keep housemates emails in a seperate file to maintain privacy
def get_housemates(f):
	reader = csv.reader(f, delimiter=',')
	return [(housemate, email) for (housemate, email) in reader]

# Move the wheel using the week as the index offset
def assign(housemates):
	offset = datetime.now().day / 7
	chores = CHORES[offset:] + CHORES[:offset]
	assignments = dict()
	for c, hm in zip(chores, housemates):
		assignments[hm[0]] = c
	return assignments

def compose_assignment_msg(assignments):
	template = "{}\n\t{}: {}\n"
	msg = ""
	for name, chore in assignments.iteritems():
		msg += (template.format(name, chore[0], chore[1]))
	return msg

# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python
def send_assignment(assignments, housemates):
	sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
	from_email = Email("no-reply@belljust.in")
	subject = "Chore Wheel"

	msg = compose_assignment_msg(assignments)
	content = Content("text/plain", msg)
	mail = Mail(from_email, subject, None, content)

	emails = [hm[1] for hm in housemates]
	add_recipients(mail, emails)

	response = sg.client.mail.send.post(request_body=mail.get())

	print(response.status_code)
	print(response.body)
	print(response.headers)

def add_recipients(mail, recipients):
	personalization = Personalization()
	for r in recipients:
		personalization.add_to(Email(r))
	mail.add_personalization(personalization)

if __name__ == '__main__':
	if len(sys.argv) != 2:
		print("Usage: main.py housemates.csv")
		sys.exit(1)

	housemates_fname = sys.argv[1]
	housemates = []
	with open(housemates_fname, 'rb') as f:
		housemates = get_housemates(f)

	assignments = assign(housemates)
	msg = compose_assignment_msg(assignments)
	send_assignment(assignments, housemates)
