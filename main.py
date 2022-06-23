import requests
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
config.read('config.ini')

APIURI = "{schema}{hostname}{path}".format(
    schema=config["API"]["schema"],
    hostname=config["API"]["hostname"],
    path=config["API"]["path"]
)

print(APIURI)

# NotifKey = "a0d949cf-720c-44b2-9323-f0bed0b995ca"
# XPCount = None
# XPError = None

# XPReq = requests.get("https://api.wiseoldman.net/players/username/Zul-raar/records?period=week&metric=overall")
# try:
#     XPCount = XPReq.json()[0]["value"]
# except Exception as e:
#     XPError = e

# if XPCount is not None and XPCount <= 0:
#     NotifData = {
#         "apiKey": NotifKey,
#         "message": "No XP gain for Zul-raar this week.",
#         "description": "Pick up the slack!",
#         "type": "info"
#     }
# elif XPCount is not None and XPCount > 0:
#     NotifData = {
#         "apiKey": NotifKey,
#         "message": "Weekly XP gain for Zul-raar!",
#         "description": "This week, {} Overall XP has been gained.".format(XPCount),
#         "type": "success"
#     }
# elif XPCount is None and XPError is not None:
#     NotifData = {
#         "apiKey": NotifKey,
#         "message": "Error encountered while requesting XP gain.",
#         "description": "Error: {}".format(XPError),
#         "type": "error"
#     }
# else:
#     exit(1)

# requests.post('https://api.mynotifier.app', NotifData)

if __name__ == "__main__":
    print(header)
