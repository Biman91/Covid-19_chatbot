# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List, Union
#
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import requests
import json
from rasa_sdk.forms import FormAction
from rasa_sdk.events import AllSlotsReset

#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []


class ActionJoke(Action):
  def name(self):
    return "action_joke"

  def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain):
    request = requests.get('http://api.icndb.com/jokes/random').json() #make an api call
    joke = request['value']['joke'] #extract a joke from returned json response
    dispatcher.utter_message('Here is a joke to cheer you up!')
    dispatcher.utter_message(joke) #send the message back to the user
    return []



class FirstPart(FormAction):
    """Example of a custom form action"""

    def name(self) -> Text:
        """Unique identifier of the form"""

        return "covid_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        """A list of required slots that the form has to fill"""
        return ["name", "email", "mobile", "pin"]

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        """A dictionary to map required slots to
            - an extracted entity
            - intent: value pairs
            - a whole message
            or a list of them, where a first match will be picked"""
        return {
            "name": [
                self.from_text(),
            ],
            "email": [
                self.from_text(),
            ],
            "mobile": [
                self.from_text(),
            ],
            "pin": [
                self.from_text(),
            ],
        }

    def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:
        """Define what the form has to do
            after all required slots are filled"""

        # utter submit template
        dispatcher.utter_message(template="utter_submit", name=tracker.get_slot('name'), email=tracker.get_slot('email'), ph=tracker.get_slot('mobile'), pin=tracker.get_slot('pin'),)
        return []

class CovidCase(FormAction):

    def name(self) -> Text:
        return "covid_case"

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
        request = requests.get('https://api.covid19india.org/v2/state_district_wise.json').json()
        a = {}
        for i in request:
            nc = 0
            for j in i['districtData']:
                a[j['district']] = j['confirmed']
                nc += int(j['confirmed'])
            a[i['state']] = nc
        if sn.title() in a:
            result = a[sn.title()]
        else:
            result = "Your area is not listed or check your spelling"

        dispatcher.utter_message(template="utter_case", state=tracker.get_slot('state'), result=result)
        # print(tracker.get_slot('state'))
        return [AllSlotsReset()]
