#!/usr/bin/env python
# -*- coding: utf-8 -*-
import feedparser
import json
import re
from time import mktime
from datetime import datetime
from twilio.rest import TwilioRestClient

# Your Account SID from www.twilio.com/console
TWILIO_ACCOUNT_SID = "TWILIO_ACCOUNT_SID_HERE"
TWILIO_AUTH_TOKEN = "TWILIO_AUTH_TOKEN_HERE"
TWILIO_PHONE_NUMBER = "+12012345678"

# {} will be replaced with user's name
WELCOME_MESSAGE = "Welcome, {}!"
BODY_MESSAGE = "\"{}\" is now available, {}!"

DEFAULT_RECORD = {
    "is_first_hello_sent": 0,
    "subscribed_status": []
}


def send_sms(client, body, phone_number):
    """
    Use Twilio Trial account to send SMS
    """
    message = client.messages.create(
        body=body,
        to=phone_number,
        from_=TWILIO_PHONE_NUMBER
    )
    try:
        if message.sid:
            return True
    except AttributeError:
        pass
    return False


def process_user(user_name, user_data, db, twilio_client):
    # Phone number
    phone_number = user_data.get('phone_number')

    if not phone_number:
        return

    # Search for user's data from database
    current_data = db.get(user_name)

    # If the record still doesn't exist
    if not current_data:
        db[user_name] = {}
        current_data = DEFAULT_RECORD

    last_updated_info = {}
    for data in current_data['subscribed_status']:
        last_updated_info[data['url']] = data['timestamp']

    if current_data['is_first_hello_sent'] == 0:
        # Send a welcome message
        body = WELCOME_MESSAGE.format(user_name)
        is_success = send_sms(twilio_client, body, phone_number)
        if not is_success:  # skipping
            return
        db[user_name]['is_first_hello_sent'] = 1

    for url_info in user_data.get('subscribed_urls', []):
        url = url_info.get('url')

        if not url:
            continue

        regex_pattern = url_info.get('pattern', "")

        last_updated_timestamp = last_updated_info.get(url, 0)
        latest_timestamp = last_updated_timestamp  # temporary variable

        try:
            d = feedparser.parse(url)
        except:
            continue

        for entry in d.get('entries', {}):
            # Compare against regex_pattern if exists
            if regex_pattern:
                m = re.search(regex_pattern, entry['title'])
                if not m:
                    continue

            dt = datetime.fromtimestamp(mktime(entry['published_parsed']))
            feed_timestamp = int((dt - datetime(1970, 1, 1)).total_seconds())

            # Take the uppermost RSS feed if the current value is still 0
            if last_updated_timestamp == 0:
                latest_timestamp = feed_timestamp
                break

            # Compare timestamp (we may send multiple messages)
            if last_updated_timestamp < feed_timestamp:
                body = BODY_MESSAGE.format(entry['title'], user_name)
                is_success = send_sms(twilio_client, body, phone_number)
                if not is_success:  # go to next URL
                    continue
                if latest_timestamp < feed_timestamp:
                    latest_timestamp = feed_timestamp

        # Update dict based on newest information
        last_updated_info[url] = latest_timestamp

    # Finalize, return last_updated_info to db
    db[user_name]['subscribed_status'] = []
    for k, v in last_updated_info.iteritems():
        new_record = {
            "url": k,
            "timestamp": v
        }
        db[user_name]['subscribed_status'].append(new_record)

    # Update db
    with open('db.json', 'w') as fp:
        json.dump(db, fp)


def main():
    # Initialize Twilio Client
    twilio_client = TwilioRestClient(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    # Open JSON files
    try:
        with open('db.json') as fp:
            db = json.load(fp)
    except IOError:  # File doesn't exist
        db = {}

    try:
        with open('user.json') as fp:
            users = json.load(fp)
    except IOError:  # File doesn't exist
        users = {}

    for user_name, user_data in users.iteritems():
        process_user(user_name, user_data, db, twilio_client)


if __name__ == '__main__':
    main()
