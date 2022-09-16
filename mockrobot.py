from time import sleep
import random


class MockRobot:
    
    processID: int
    processStatus: str

    def __init__(self):
        MockRobot.processID = ""
        MockRobot.processStatus = ""

    def home(self):
        sleep(random.randint(0, 2))
        MockRobot.processID = random.randint(1, 1000)
        return self.processID

    def pick(self, sourceLocation: int):
        sleep(random.randint(0, 5))
        MockRobot.processID = sourceLocation + 1
        return self.processID
        
    def place(self, destinationLocation: int):
        sleep(random.randint(0, 5))
        MockRobot.processID = destinationLocation + 1
        return self.processID
        
    def status(self):
        MockRobot.processStatus = random.choice(["In Progress", "Finished Successfully", "Terminated With Error"])
        return MockRobot.processStatus
        

        

