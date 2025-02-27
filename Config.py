import os


class Config(object):
    API_ID = int(os.environ.get("API_ID", 25024171)
    API_HASH = os.environ.get("API_HASH", "7e709c0f5a2b8ed7d5f90a48219cffd3")
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "8095096286:AAGtId-d51HL7ezrDnqffKeQ4WF9ONEMieI")
    TOKEN = os.environ.get("TOKEN")
