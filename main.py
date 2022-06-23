from time import sleep
import requests, schedule, datetime
from configparser import ConfigParser

header = """
 __   _______   _____       _       _   _       _   _  __ _           
 \ \ / /  __ \ / ____|     (_)     | \ | |     | | (_)/ _(_)          
  \ V /| |__) | |  __  __ _ _ _ __ |  \| | ___ | |_ _| |_ _  ___ _ __ 
   > < |  ___/| | |_ |/ _` | | '_ \| . ` |/ _ \| __| |  _| |/ _ \ '__|
  / . \| |    | |__| | (_| | | | | | |\  | (_) | |_| | | | |  __/ |   
 /_/ \_\_|     \_____|\__,_|_|_| |_|_| \_|\___/ \__|_|_| |_|\___|_|   

"""  # noqa: W291, W605

config = ConfigParser()
config.read("config.ini")

USERNAME = config["ACCOUNT"].get("username")
PERIOD = config["FILTERS"].get("period")
SKILL = config["FILTERS"].get("skill")
APIKEY = config["API"].get("key")
APIURI = "{schema}{hostname}{path}".format(
    schema=config["API"].get("schema"),
    hostname=config["API"].get("hostname"),
    path=config["API"].get("path"),
)


def getSkillDeltas():
    if (
        requests.post(
            "https://api.wiseoldman.net/players/track",
            {"username": USERNAME},
        ).status_code
        != 200
    ):
        print("Updating skill metrics failed. Results might be outdated...")

    sleep(15)

    # Single skill request
    resp = requests.get(
        # To support multi skill lookups, remove the 'metric' parameter from the request.
        # After that, filter the response to obtain the needed skill metrics!
        "https://api.wiseoldman.net/players/username/{user}/records?period={period}&metric={skill}".format(
            user=USERNAME,
            period=PERIOD,
            skill=SKILL,
        )
    )

    if resp.status_code == 200:
        data = resp.json()[0]
        return {data["metric"]: data["value"]}
    else:
        print(
            "No data found with current settings, please check the configuration file for errors."
        )
        exit(1)


def buildNotification():
    frequency = {"day": "Daily", "week": "Weekly", "month": "Monthly", "year": "Yearly"}

    for skill, xp in getSkillDeltas().items():
        if xp is not None and xp <= 0:
            NotifData = {
                "apiKey": APIKEY,
                "message": "No XP gain for {username} this week.".format(
                    username=USERNAME
                ),
                "description": "Pick up the slack!",
                "type": "info",
            }
        elif xp is not None and xp > 0:
            NotifData = {
                "apiKey": APIKEY,
                "message": "{periodic} {skillname} XP gain for {username}!".format(
                    periodic=frequency[PERIOD], skillname=skill, username=USERNAME
                ),
                "description": "This {time}, {gain} {skillname} XP has been gained.".format(
                    time=PERIOD, gain=xp, skillname=skill
                ),
                "type": "success",
            }
        elif xp is None:
            NotifData = {
                "apiKey": APIKEY,
                "message": "Error encountered while requesting XP gain.",
                "description": "Please try again later.",
                "type": "error",
            }
        else:
            exit(1)

    return NotifData


def sendNotification():
    body = buildNotification()

    resp = requests.post("https://api.mynotifier.app", body)

    logprefix = "[{datetime}]: ".format(
        datetime=datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    )

    if resp.status_code == 200:
        return "{prefix} Success!".format(prefix=logprefix)
    else:
        return "{prefix} Statuscode != 200 so the notification call might have failed, reason: {reason}".format(
            prefix=logprefix, reason=resp.json()
        )


def variableReminder(yearly=False):
    if datetime.date.today().day != 1:
        return
    elif yearly and datetime.date.today().month != 1:
        return
    else:
        return sendNotification()


if __name__ == "__main__":
    print(header)

    match PERIOD:
        case "day":
            schedule.every().day.at("12:00").do(sendNotification)
        case "week":
            schedule.every().sunday.at("12:00").do(sendNotification)
        case "month":
            schedule.every().day.at("12:00").do(variableReminder)
        case "year":
            schedule.every().day.at("12:00").do(variableReminder, True)

    while True:
        schedule.run_pending()
