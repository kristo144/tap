from inspect import signature

#import trigger
#import action

class Bot:
    __triggers = list()
    __actions  = list()

    def __init__(self, name):
        self.__name = name
        
    @staticmethod
    def __check_closure(closure, type):
        if not callable(closure):
            raise TypeError(type + " must be a callable")
        if len(signature(closure).parameters) != 1:
            raise TypeError(type + " must take 1 argument and return boolean")

    @staticmethod
    def __call_list(l, env):
        f = lambda callable: callable(env)
        return list(map(f, l))


    def get_name(self):
        return self.__name
    
    def add_trigger(self, trigger):
        Bot.__check_closure(trigger, "Trigger")
        self.__triggers.append(trigger)
        
    def add_action(self, action):
        Bot.__check_closure(action, "Action")
        self.__actions.append(action)
        
    def check_triggers(self, env):
        return any(Bot.__call_list(self.__triggers, env))

    def execute_actions(self, env):
        Bot.__call_list(self.__actions, env)
