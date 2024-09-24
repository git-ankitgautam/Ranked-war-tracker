from os import environ
from dotenv import load_dotenv
load_dotenv()
API_KEY = environ["Torn_API_KEY"]


""" for devlins faction ids"""
fac_Ids = environ["Devlins_faction_ids"]
fac_Ids= fac_Ids.split(",")
fac_Ids = [int(num) for num in fac_Ids]