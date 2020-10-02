# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions

# This is a simple example for a custom action which utters "Hello World!"

import json
import os
from typing import Dict, List, Text

import requests
from dotenv import load_dotenv
from rasa_sdk import Action, Tracker
from rasa_sdk.events import EventType, SlotSet
from rasa_sdk.executor import CollectingDispatcher

load_dotenv()

AIRTABLE_API_KEY = os.getenv('AIRTABLE_API_KEY')
BASE_ID = os.getenv('BASE_ID')
TABLE_NAME = os.getenv('TABLE_NAME')


def create_health_log(confirm_exercise, exercise, sleep, diet, stress, goal):
    request_url = 'https://api.airtable.com/v0/{}/{}'.format(BASE_ID, TABLE_NAME)
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': 'Bearer {}'.format(AIRTABLE_API_KEY)
    }

    data = {
        'fields': {
            'Exercised?': confirm_exercise,
            'Type of exercise': exercise,
            'Amount of sleep': sleep,
            'Diet': diet,
            'Stress': stress,
            'Goal': goal,
        }
    }

    try:
        response = requests.post(
            request_url, headers=headers, data=json.dumps(data)
        )
    except requests.exceptions.HTTPError as e:
        raise SystemError(e)

    print('submit status is {}'.format(response.status_code))
    return response


class ValidateHealthForm(Action):

    def name(self) -> Text:
        return 'validate_health_form'

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:
        if tracker.get_slot('confirm_exercise'):
            required_slots = [
                'confirm_exercise', 'exercise', 'sleep', 'diet', 'stress', 'goal'
            ]
        else:
            required_slots = [
                'confirm_exercise', 'sleep', 'diet', 'stress', 'goal'
            ]

        for slot_name in required_slots:
            if tracker.slots.get(slot_name) is None:
                # The slot is not filled yet. Request the user to fill this slot next.
                return [SlotSet('requested_slot', slot_name)]

        # All slots are filled.
        return [SlotSet('requested_slot', None)]


class SubmitHealthForm(Action):

    def name(self) -> Text:
        return 'submit_health_form'

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:
        response = create_health_log(
            tracker.get_slot('confirm_exercise'),
            tracker.get_slot('exercise'),
            tracker.get_slot('sleep'),
            tracker.get_slot('diet'),
            tracker.get_slot('stress'),
            tracker.get_slot('goal')
        )
        dispatcher.utter_message(template='utter_submit')
        return []
