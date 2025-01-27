class Action:

    def __init__(self, action):
        #TODO: check that action takes player argument
        self.__action = action

    def execute(self, player):
        self.__action(player)
        