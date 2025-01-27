class Trigger:
    
    def __init__(self, predicate):
        self.__predicate = predicate

    def check(self):
        return self.__predicate()
        