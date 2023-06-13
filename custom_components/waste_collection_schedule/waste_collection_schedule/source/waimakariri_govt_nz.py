import http.client
import urllib.parse
import json

import datetime
from waste_collection_schedule import Collection

TITLE = "Waiamakariri District Council"
DESCRIPTION = "Source for Waimakariri District Council, New Zealand. Finds both general, organic and recycling dates."
URL = "https://rethinkrubbish.waimakariri.govt.nz/s/#calendar"  # Insert url to service homepage. URL will show up in README.md and info.md
TEST_CASES = { 
    "TestName1": {"arg1": 1, "arg2": "Bell st", "arg3": "Rangiora", "arg4": 7400}, # Collection Day & Week: Wednesday Week 1
    "TestName2": {"arg1": 4, "arg2": "Reeves rd", "arg3": "Rangiora", "arg4": 7400}, # Collection Day & Week: Wednesday Week 2
    "TestName3": {"arg1": 10, "arg2": "Kawakawa st", "arg3": "Pegasus", "arg4": 7612}, # Collection Day & Week: Monday Week 2
}

API_URL = "https://rethinkrubbish.waimakariri.govt.nz/s/sfsites/aura"
ICON_MAP = {
    "GENERALWASTE": "mdi:trash-can",
    "RECYCLE": "mdi:recycle",
    "ORGANIC": "mdi:leaf",
}

# Freqeuncy of collections
FREQUENCY_MAP = {
    "Weekly": 7,
    "Fortnightly": 14
}

class WaimakaririApiInterface:
    def __init__(self, houseNumber, streetName, town, postcode):
        self.conn = http.client.HTTPSConnection("rethinkrubbish.waimakariri.govt.nz")

        self.payload = self.createPayload(houseNumber, streetName, town, postcode)
        
        self.headers = {
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'cookie': 'renderCtx=%7B%22pageId%22%3A%22678c8764-cc28-4fdf-a0f4-70383b62cd05%22%2C%22schema%22%3A%22Published%22%2C%22viewType%22%3A%22Published%22%2C%22brandingSetId%22%3A%22a20e50d9-9043-4083-9906-c3c9930e50fa%22%2C%22audienceIds%22%3A%22%22%7D; CookieConsentPolicy=0:1; LSKey-c$CookieConsentPolicy=0:1; sfdc-stream=!+v5KD2y0thK3AY2Z4SVI1ZA1N8Zl3xu+caY6lLs9JAYuEFMBXDO3Y4qK1lQbyy8a9tUBinKi1AP8YAo=; pctrk=35466ea4-bd73-471e-af30-58b279cdf86d; CookieConsentPolicy=0:1; LSKey-c$CookieConsentPolicy=0:1; sfdc-stream=!20tQvDm6jj7fRFtbt9Our1uX4ONx3xs2vDMhRcWwpDitAH7++b5/7OvLplLkmLrX9siv4CX2QkqqBYo=',
        }


    def createPayload(self, houseNumber, streetName, town, postcode):
        payload_params = {
            "actions": [
                {
                    "id": "178;a",
                    "descriptor": "apex://CouncilAppController/ACTION$getCouncilMaterials",
                    "callingDescriptor": "UNKNOWN",
                    "params": {
                        "selectedAddress": {
                            "Account_Number__c": "WK1 WED",
                            "Action_Type__c": "Lift",
                            "Address__c": streetName,
                            "Council__c": "Waimakariri",
                            "Day_Of_Week__c": "Wednesday",
                            "House_Number__c": houseNumber,
                            "Position__c": "1658",
                            "Post_Code__c": postcode,
                            "Quantity__c": 0,
                            "Route_Description__c": "401 Wk1 REC Wednesday",
                            "Route_Number__c": "40121",
                            "Site_Name__c": "WDC8092",
                            "Site_Order_Id__c": "171507",
                            "Town__c": town,
                            "Id": "a6b2v000000PsxxAAC"
                        },
                        "councilName": "Waimakariri"
                    }
                }
            ]
        }

        return "message=" + urllib.parse.quote(str(payload_params).replace("'", '"').replace(" ", '')) + "&aura.context=%7B%22mode%22%3A%22PROD%22%2C%22fwuid%22%3A%22c1R3MUZhNldLUm1BS0plaUgwaDhnQWI4T1Q3UVpoR0gtemxDX3B4aTM3bVEyNDQuMjAuMS0yLjQxLjQ%22%2C%22app%22%3A%22siteforce%3AcommunityApp%22%2C%22loaded%22%3A%7B%22APPLICATION%40markup%3A%2F%2Fsiteforce%3AcommunityApp%22%3A%22A5RUWR2WpZa7WQPyHOKNVQ%22%2C%22COMPONENT%40markup%3A%2F%2Finstrumentation%3Ao11ySecondaryLoader%22%3A%22WAlywPtXLxVWA9DxV-jd3A%22%7D%2C%22dn%22%3A%5B%5D%2C%22globals%22%3A%7B%7D%2C%22uad%22%3Afalse%7D&aura.pageURI=%2Fs%2F%23calendar&aura.token=null"

    def getResponse(self):
        self.conn.request("POST", "/s/sfsites/aura", self.payload, self.headers)
        res = self.conn.getresponse()
        json_data = json.loads(res.read())
        return_value = json_data["actions"][0]["returnValue"][0]

        return CouncilReturnValue(return_value)

class CouncilReturnValue:
    def __init__(self, return_value):
        self.return_value = return_value

    def get_day_of_week(self):
        return self.return_value["dayOfWeek"]

    def has_organic(self):
        return self.return_value["hasGlass"]

    def get_general_frequency(self):
        return self.return_value["generalFrequency"]

    def get_general_start_date(self):
        return self.return_value["generalStartDate"]

    def get_organic_frequency(self):
        return self.return_value["glassFrequency"]

    def get_organic_start_date(self):
        return self.return_value["glassStartDate"]

    def has_general_waste(self):
        return self.return_value["hasGeneralWaste"]

    def has_recycle(self):
        return self.return_value["hasRecycle"]

    def get_recycle_frequency(self):
        return self.return_value["recycleFrequency"]

    def get_recycle_start_date(self):
        return self.return_value["recycleStartDate"]


class Source:
    def __init__(self, arg1, arg2, arg3, arg4):
        houseNumber = arg1
        streetName = arg2
        town = arg3
        postcode = arg4

        self.api = WaimakaririApiInterface(houseNumber, streetName, town, postcode)

    def fetch(self):
        entries = []  # List that holds collection schedule

        councilReturnValue = self.api.getResponse()

        # date 1 year from now
        endDate = (datetime.datetime.now() + datetime.timedelta(days=365)).date()
        
        # General Waste
        if councilReturnValue.has_general_waste():
            frequencyInDays = FREQUENCY_MAP.get(councilReturnValue.get_general_frequency())
            collectionDate = datetime.datetime.strptime(councilReturnValue.get_general_start_date(), "%Y-%m-%d").date()
            while collectionDate < endDate:
                entries.append(
                    Collection(
                        date = collectionDate,
                        t = "General Waste",
                        icon = ICON_MAP.get("GENERALWASTE")
                    )
                )
                collectionDate += datetime.timedelta(days=frequencyInDays)

        # Recycle
        if councilReturnValue.has_recycle():
            frequencyInDays = FREQUENCY_MAP.get(councilReturnValue.get_recycle_frequency())
            collectionDate = datetime.datetime.strptime(councilReturnValue.get_recycle_start_date(), "%Y-%m-%d").date()
            while collectionDate < endDate:
                entries.append(
                    Collection(
                        date = collectionDate,
                        t = "Recycle",
                        icon = ICON_MAP.get("RECYCLE")
                    )
                )
                collectionDate += datetime.timedelta(days=frequencyInDays)

        # Organic
        if councilReturnValue.has_organic():
            frequencyInDays = FREQUENCY_MAP.get(councilReturnValue.get_organic_frequency())
            collectionDate = datetime.datetime.strptime(councilReturnValue.get_organic_start_date(), "%Y-%m-%d").date()
            while collectionDate < endDate:
                entries.append(
                    Collection(
                        date = collectionDate,
                        t = "Organic",
                        icon = ICON_MAP.get("ORGANIC")
                    )
                )
                collectionDate += datetime.timedelta(days=frequencyInDays)
        
        return entries