from datetime import datetime

def timestamp(locale = "eu"):
    if locale == "eu":
        return datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    elif locale == "us":
        return datetime.now().strftime("%m-%d-%Y %H:%M:%S")