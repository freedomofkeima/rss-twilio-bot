# rss-twilio-bot

An experimentation to use Twilio Trial SMS as a notification medium for RSS Feed updates from http://www.nyaa.se/.


## Screenshot

![SMS](https://raw.githubusercontent.com/freedomofkeima/rss-twilio-bot/master/screenshot.png)


## Format (user.json)

```
{
  "Subaru": {
    "phone_number": "+818012345678",
    "subscribed_url": [
      "http://www.nyaa.se/?page=rss&cats=1_37&term=720p+horriblesubs+01+mkv&minage=0&maxage=30"
    ]
  },
  "Barusu": {
    "phone_number": "+818023456789",
    "subscribed_url": [
      "http://www.nyaa.se/?page=rss&cats=1_37&term=720p+horriblesubs+01+mkv&minage=0&maxage=30"
    ]
  }
}
```

Each records will have a unique identifier of a record (in this case, user's name). 

`phone_number` should conform to Twilio phone number format.

`subscribed_url` is a list of URLs feed which you want to get notification from if a new update occurs.

The RSS Feed URL above will give you an update for all first (ep. 1) release from [HorribleSubs](http://horriblesubs.info/).


## Installation

```
$ pip install -r requirements.txt
```


Required TWILIO values (`main.py`):

- TWILIO_ACCOUNT_SID
- TWILIO_AUTH_TOKEN
- TWILIO_PHONE_NUMBER

You can get those values for free with [Twilio](https://www.twilio.com/) trial account. One of the side note of trial account is that you can only send your messages to [verified number](https://www.twilio.com/console/phone-numbers/verified). 

## Run

After correctly configuring `user.json`, you can execute the script by running:

```
$ python main.py
```

For best usage, you need to set a **cron job** (e.g.: every 10 minutes) to run this script and check periodically.


## Future Idea

- Add AWS Lambda (scheduled events) + S3 integration (`db.json` and `user.json`) to run this script serverless.


Last Updated: September 29, 2016
