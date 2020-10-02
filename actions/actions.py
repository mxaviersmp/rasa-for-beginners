# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions

# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Dict, EventType, List, Text, Union

from rasa_sdk import Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction


class HealthForm(FormAction):

    def name(self) -> Text:
        return 'health_form'

    @staticmethod
    def required_slots(tracker: 'Tracker') -> List[Text]:
        if tracker.get_slot('confirm_exercise'):
            return ['confirm_exercise', 'exercise', 'sleep', 'diet', 'stress', 'goal']
        else:
            return ['confirm_exercise', 'sleep', 'diet', 'stress', 'goal']

    def submit(
        self,
        dispatcher: 'CollectingDispatcher',
        tracker: 'Tracker',
        domain: Dict[Text, Any]
    ) -> List[EventType]:
        return []

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict[Text, Any]]]]:
        return {
            'confirm_exercise': [
                self.from_intent(intent='affirm', value=True),
                self.from_intent(intent='deny', value=False),
                self.from_intent(intent='inform', value=True),
            ],
            'sleep': [
                self.from_entity(entity='sleep'),
                self.from_intent(intent='deny', value=None),
            ],
            'diet': [
                self.from_text(intent='inform'),
                self.from_text(intent='deny'),
                self.from_text(intent='affirm')
            ],
            'goal': [
                self.from_text(intent='inform'),
                self.from_text(intent='deny'),
                self.from_text(intent='affirm')
            ]
        }
