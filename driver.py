from mockrobot import MockRobot
import socket
import ast


class DeviceDriver(socket.socket):
    ip = "localhost"
    port = 4500
    operations = ["pick", "place", "transfer"]

    def __init__(self):
        super().__init__()
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.robot = MockRobot()
        self.robot.home()

    
    def open_connection(self):
        # Create a TCP/IP socket
        address = (DeviceDriver.ip, DeviceDriver.port)
        self.server.bind(address)
        self.server.listen(1)
        return ""

    def check_status():
        result = MockRobot.status()
        if "Error" in result:
            return result
        else:
            return ""
        
    def initialize(self):
        self.robot.home()
        result = DeviceDriver.check_status()
        if "Error" in result:
            return result
        else:
            return ""

        
    def execute_operation(self, operation: str, parameter_name: list, parameter_values: list):
        if operation in DeviceDriver.operations:
            if len(parameter_values) == 1 and (operation == "pick" or operation == "place"):
                if operation == "pick" and "Source" in parameter_name:
                    self.robot.pick(parameter_values[0])
                    result = DeviceDriver.check_status()
                    return result
                elif operation == "place" and "Destination" in parameter_name:
                    self.robot.place(parameter_values[0])
                    result = DeviceDriver.check_status()
                    return result
                else:
                    print("got here")
                    return "Wrong combination of parameters"
            else:
                if "Destination" in parameter_name[0] \
                        and "Source" in parameter_name[1] and operation == "transfer":
                    self.robot.pick(parameter_values[1])
                    self.robot.place(parameter_values[0])
                    result = DeviceDriver.check_status()
                    return result
                elif "Source" in parameter_name[0] \
                        and "Destination" in parameter_name[1] and operation == "transfer":
                    self.robot.pick(parameter_values[0])
                    self.robot.place(parameter_values[1])
                    result = DeviceDriver.check_status()
                    return result
                else:
                    return "Wrong combination of parameters"
        else:
            return "Not a valid operation."

        
    def abort(self):
        return ""
        

if __name__ == "__main__":

    driver = DeviceDriver()
    conn = driver.open_connection()
    scheduled_tasks = []
    initialized = 0
    while True:
        client, addr = driver.server.accept()
        print('Start listening on', driver.ip, ':', driver.port)
        print('Received connection from', addr[0], ':', addr[1])
        while True:
            data = client.recv(1024).decode('utf-8')
            data = data.split()
            print('Received', data, 'from the client')
            if data not in scheduled_tasks:
                scheduled_tasks.extend(data)
            print(scheduled_tasks)
            if scheduled_tasks[0] == "initialize" and initialized == 0:
                response = driver.initialize()
                pass
            else:
                response = "Not initialized!"
                scheduled_tasks = []
                pass

            while "" not in response and initialized == 0:
                response = driver.initialize()
                if "" in response:
                    initialized += 1
            try:
                if scheduled_tasks[1] in driver.operations and len(scheduled_tasks) >= 3 \
                        and ("Destination" in ast.literal_eval(scheduled_tasks[2])
                             or "Source" in ast.literal_eval(scheduled_tasks[2])):
                    response = driver.execute_operation(
                        scheduled_tasks[1],
                        ast.literal_eval(scheduled_tasks[2]),
                        ast.literal_eval(scheduled_tasks[3])
                    )
                else:
                    #response = "incorrect input order"
                    scheduled_tasks = []
                    pass
            except IndexError:
                pass
            except ValueError:
                response = "Incorrect input parameter"

            if "abort" in data:
                scheduled_tasks = []
                response = driver.abort()
            elif len(scheduled_tasks) >= 4:
                scheduled_tasks = []

            # DO something.....
            print(response)
            client.send(response.encode('utf-8'))

            client.close()
            break