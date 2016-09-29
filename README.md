# rss-twilio-bot

An experimentation to use Twilio Trial SMS as a notification medium for RSS Feed updates from http://www.nyaa.se/ (Anime) and http://mangastream.com/rss (Manga).


## Screenshot

<img src="https://raw.githubusercontent.com/freedomofkeima/rss-twilio-bot/master/screenshot.png" width="400">

<img src="https://raw.githubusercontent.com/freedomofkeima/rss-twilio-bot/master/screenshot2.png" width="400">


## Requirements

- Python 2.7
- [Twilio trial account](https://www.twilio.com/)


## Format (user.json)

```
{
  "Subaru": {
    "phone_number": "+818012345678",
    "subscribed_urls": [
        {
            "url": "http://www.nyaa.se/?page=rss&cats=1_37&term=720p+horriblesubs+01+mkv&minage=0&maxage=30"
        }
    ]
  },
  "Barusu": {
    "phone_number": "+818023456789",
    "subscribed_urls": [
        {
            "url": "http://mangastream.com/rss",
            "pattern": "Shokugeki no Souma [0-9]+"
        }
    ]
  }
}
```

Each records will have a unique identifier of a record (in this case, user's name). 

`phone_number` should conform to Twilio phone number format.

`subscribed_urls` is a list of `url` feed (required) and `pattern` (optional, which is targeted to RSS `title` in `entries`) which you want to get notification from if a new update occurs.

The RSS Feed URL above will give you an update for all first (ep. 1) release from [HorribleSubs](http://horriblesubs.info/).


## Installation

It is recommended to use `virtualenv` instead of installing dependencies in global system with:

```
$ virtualenv venv
$ . venv/bin/activate
```

After that, you can install Python dependencies with:

```
$ pip install -r requirements.txt
```

Required TWILIO values (`main.py`):

- TWILIO_ACCOUNT_SID
- TWILIO_AUTH_TOKEN
- TWILIO_PHONE_NUMBER

You can get those values for free with [Twilio](https://www.twilio.com/) trial account. One of the side note of trial account is that you can only send your messages to [verified number](https://www.twilio.com/console/phone-numbers/verified). 

Twilio phone number can be acquired by following the tutorial here: https://support.twilio.com/hc/en-us/articles/223136107-How-does-Twilio-s-Free-Trial-work-


## Run

After correctly configuring `user.json`, you can execute the script by running:

```
$ python main.py
```

For best usage, you need to set a **cron job** (e.g.: every 10 minutes) to run this script and check periodically.


## Future Idea

- Add AWS Lambda (scheduled events) + S3 integration (`db.json` and `user.json`) to run this script serverless.


## License

MIT License.

Last Updated: September 29, 2016
