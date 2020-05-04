# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"
from typing import Any, Text, Dict, List, Union
import re
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import requests
import json
from rasa_sdk.forms import FormAction
from rasa_sdk.events import AllSlotsReset


class StateCovidCase(FormAction):

    def name(self) -> Text:
        return "state_covid_case"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        return ["state"]

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        return {
            "state": [
                self.from_text(),
            ],
        }

    def submit(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        sn = tracker.get_slot('state')
        request = requests.get("https://api.covid19india.org/data.json").json()
        stateWiseCases = request["statewise"]
        result = ''
        try:
            for i in stateWiseCases:
                if sn.title() in i['state']:
                    result += f"\nConfirmed: {i['confirmed']},\nRecovered: {i['recovered']},\nDeath: {i['deaths']}"
                    break
            else:
                result += f"There is no cases or check the correct spelling."
        except:
            print("Error")
        dispatcher.utter_message(template="utter_case", state=tracker.get_slot('state'), result=result)
        return [AllSlotsReset()]

class CountryCovidCase(FormAction):

    def name(self) -> Text:
        return "country_covid_case"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        return ["country"]

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        return {
            "country": [
                self.from_text(),
            ],
        }

    def submit(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        cn = tracker.get_slot('country')
        request = requests.get("https://api.covid19api.com/summary").json()
        result = ''
        try:
            for i in request['Countries']:
                if cn in ['united states of america', 'United States of America', 'America', 'america']:
                    cn = 'United States of America'
                    if cn == i['Country']:
                        result += f"\nConfirmed: {i['TotalConfirmed']},\nRecovered {i['TotalRecovered']},\nDeath: {i['TotalDeaths']}"
                        break
                elif cn.title() == i['Country']:
                    result += f"\nConfirmed: {i['TotalConfirmed']},\nRecovered {i['TotalRecovered']},\nDeath: {i['TotalDeaths']}"
                    break
            else:
                result += "There is no cases or check the correct spelling."
        except:
            print("Error")

        dispatcher.utter_message(template="utter_case1", country=tracker.get_slot('country'), result=result)
        return [AllSlotsReset()]



class PinCovidCase(FormAction):

    def name(self) -> Text:
        return "pin_covid_case"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        return ["pin"]

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        return {
            "pin": [
                self.from_entity(entity="pincode"),
                self.from_text(intent="enter_name"),
            ],
        }

    def submit(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        pin = str(tracker.get_slot("pin"))
        regex_pincode = "[0-9]{6}"
        if re.search(regex_pincode, pin) is None:
            dispatcher.utter_message(f"Please enter a valid PIN Code.")
            return {"pin": None}

        result = ''
        try:
            url = "https://api.postalpincode.in/pincode/" + pin
            jsonRes = requests.get(url).json()
            postOffice = jsonRes[0]["PostOffice"]
            state = postOffice[0]["State"]
            district = postOffice[0]["District"]
            sd = requests.get("https://api.covid19india.org/v2/state_district_wise.json").json()
            for i in sd:
                if i['state'] == state:
                    for j in i['districtData']:
                        if j['district'] == district:
                            result += f"\nState: {j['district']}\nConfirmed: {j['confirmed']}\nActive: {j['active']}\nRecovered: {j['recovered']}\nDeath: {j['deceased']}"
                            break
                    else:
                        result += f"There is no cases or check the correct spelling."
        except:
            print('Error')
        dispatcher.utter_message(template="utter_case2", pin=tracker.get_slot('pin'), result=result)
        return [AllSlotsReset()]



class DistCovidCase(FormAction):
    def name(self) -> Text:
        return "dist_covid_case"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        return ["dist"]

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        return {
            "dist": [
                self.from_text(),
            ],
        }

    def submit(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        d = tracker.get_slot('dist')
        request = requests.get("https://api.covid19india.org/v2/state_district_wise.json").json()
        result = ""
        try:
            a = ""
            for i in request:
                for j in i['districtData']:
                    if d.title() == j['district']:
                        a += f"\nConfirmed: {j['confirmed']}\nActive: {j['active']}\nRecovered: {j['recovered']}\nDeath: {j['deceased']}"
            if len(a) > 0:
                result += a
            else:
                result += "There is no cases or check the correct spelling."
        except:
            print("Error")
        dispatcher.utter_message(template="utter_case3", dist=tracker.get_slot('dist'), result=result)
        return [AllSlotsReset()]