from time import sleep
import random


class MockRobot:
    
    processID: int
    processStatus: str

    def __init__(self):
        MockRobot.processID = ""
        MockRobot.processStatus = ""

    def home(self) -> int:
        sleep(random.randint(0, 2))
        MockRobot.processID = random.randint(1, 1000)
        return MockRobot.processID

    def pick(self, sourceLocation: int) -> int:
        sleep(random.randint(0, 5))
        MockRobot.processID = sourceLocation + 1
        return MockRobot.processID
        
    def place(self, destinationLocation: int) -> int:
        sleep(random.randint(0, 5))
        MockRobot.processID = destinationLocation + 1
        return MockRobot.processID
        
    def status(self) -> str:
        MockRobot.processStatus = random.choice(["In Progress", "Finished Successfully", "Terminated With Error"])
        return MockRobot.processStatus
        

        

