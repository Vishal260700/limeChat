from typing import Any, Text, Dict, List, Union
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet, UserUtteranceReverted
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction

import datetime


class BookRoomInfo(FormAction):
    def name(self):
        return "form_book_room"

    @staticmethod
    def required_slots(tracker: Tracker):
        return ["number", "room_type"]

    def submit(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]):
        # Submit 
        dispatcher.utter_message(template="utter_submit", number=tracker.get_slot('number'),
                                 room_type=tracker.get_slot('room_type'))
        return []

    def slot_mappings(self):

        return {
            "number": self.from_entity(entity="number", intent='num_rooms'),
            "room_type": self.from_entity(entity="room_type", intent="type_rooms")
        }

class BookRoomNumberInfo(FormAction):
    def name(self):
        return "form_book_room_number"

    @staticmethod
    def required_slots(tracker: Tracker):
        return ["room_type"]

    def submit(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]):
        # Submit
        dispatcher.utter_message(template="utter_submit", 
                                room_type=tracker.get_slot('room_type'))
        return []

    def slot_mappings(self):

        return {
            "room_type": self.from_entity(entity="room_type", intent="type_rooms")
        }

class BookTimeRelativeInfo(FormAction):
    def name(self):
        return "form_book_time_relative"
    
    @staticmethod
    def required_slots(tracker : Tracker):
        return ["number"]
    
    def submit(self, dispatcher : CollectingDispatcher, tracker : Tracker, domain: Dict[Text, Any]):
        # Submit
        dispatcher.utter_message(template = "utter_clean_room_relative",
                                 book_time = tracker.get_slot('number'))
        return []
    
    def slot_mappings(self):
        return {
            "book_time": self.from_entity(entity = "number", intent = "clean_room_relative")
        }

class ResetSlots(Action):

    def name(self):
        return "action_reset_slots"

    def run(self, dispatcher, tracker, domain):
        return [SlotSet("number", None), SlotSet("room_type", None)]

class MyFallbackAction(Action):
    def name(self):
        return "action_my_fallback"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_template("utter_fallback_message", tracker)       
        return [UserUtteranceReverted()]