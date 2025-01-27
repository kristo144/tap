from functools import partial

import trigger
import action

class bot:
    __triggers = list()
    __actions  = list()

    def __init__(self, name):
        self.__name = name

    def get_name(self):
        return self.__name
    
    def add_trigger(self, trigger):
        # todo: check if trigger is of type trigger
        __triggers.append(trigger)
        
    def add_action(self, action):
        # todo: check if action is of type action
        __actions.append(action)
        
    def check_triggers(self):
        return any(list(map(trigger.check, self.__triggers)))

    def execute_actions(self, player):
        part = partial(Action.execute, player)
        return any(list(map(part, self.__actions)))
