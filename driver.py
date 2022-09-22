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

    def check_status(self):
        result = self.robot.status()
        if "Error" in result:
            return result
        else:
            return ""

    def initialize(self):
        self.robot.home()
        result = DeviceDriver.check_status(self)
        return result

    def execute_operation(self, operation: str, parameter_name: list, parameter_values: list):
        # check operation is valid
        if operation in DeviceDriver.operations:
            # check if operation is pick/place
            if len(parameter_values) == 1 and (operation == "pick" or operation == "place"):
                if operation == "pick" and "Source" in parameter_name:
                    self.robot.pick(parameter_values[0])
                    result = DeviceDriver.check_status(self)
                    return result
                elif operation == "place" and "Destination" in parameter_name:
                    self.robot.place(parameter_values[0])
                    result = DeviceDriver.check_status(self)
                    return result
                else:
                    return "Wrong combination of parameters"
            # check if operation is "pick and place i.e. transfer"
            elif operation == "transfer" and len(parameter_values) == 2:
                if "Destination" in parameter_name[0] \
                        and "Source" in parameter_name[1] and operation == "transfer":
                    self.robot.pick(parameter_values[1])
                    self.robot.place(parameter_values[0])
                    result = DeviceDriver.check_status(self)
                    return result
                elif "Source" in parameter_name[0] \
                        and "Destination" in parameter_name[1] and operation == "transfer":
                    self.robot.pick(parameter_values[0])
                    self.robot.place(parameter_values[1])
                    result = DeviceDriver.check_status(self)
                    return result
                else:
                    return "Wrong combination of parameters"
            # for case that scheduler inputs both source and destination for pick or place operation
            else:
                return "Wrong combination of parameters"
        else:
            return "Not a valid operation."

    def abort(self):
        return ""


if __name__ == "__main__":
    # create instance of the device driver and open connection
    driver = DeviceDriver()
    conn = driver.open_connection()
    # empty list and variable for controlling task flow and initialization
    scheduled_tasks = []
    initialized = 0
    previous_operation = ""
    while True:
        # Accept connection from scheduler
        client, addr = driver.server.accept()
        print('Start listening on', driver.ip, ':', driver.port)
        print('Received connection from', addr[0], ':', addr[1])
        while True:
            # Listen for operation
            data = client.recv(1024).decode('utf-8')

            if data != "initialize":
                # Create list from operation
                data = data.split()

            print('Received', data, 'from the client')

            # Add received data to scheduled tasks list
            if data not in scheduled_tasks:
                if type(data) == list:
                    scheduled_tasks.extend(data)
                else:
                    scheduled_tasks.append(data)

            print(scheduled_tasks)

            # Check for initialization as first operation
            if scheduled_tasks[0] == "initialize" and initialized == 0:
                response = driver.initialize()
            elif scheduled_tasks[0] == "initialize" and initialized == 1 and data == "initialize":
                response = "Already initialized"
            elif scheduled_tasks[0] != "initialize" and data != "initialize":
                response = "Not initialized"
                scheduled_tasks = []
                initialized = 0

            # Ensure initialization is successful
            while "Error" in response and initialized == 0:
                response = driver.initialize()
                if response == "":
                    initialized += 1

            # execute operation only if initialized
            if len(scheduled_tasks) > 1 and scheduled_tasks[0] == "initialize":
                try:
                    if scheduled_tasks[1] in driver.operations \
                            and ("Destination" in ast.literal_eval(scheduled_tasks[2])
                                 or "Source" in ast.literal_eval(scheduled_tasks[2])):
                        # make sure operation isn't repeated if response is successful
                        if previous_operation == "pick" \
                                and scheduled_tasks[1] == "transfer":
                            response = "Cannot run transfer operation following pick"
                        elif previous_operation != scheduled_tasks[1]:
                            response = driver.execute_operation(
                                scheduled_tasks[1],
                                ast.literal_eval(scheduled_tasks[2]),
                                ast.literal_eval(scheduled_tasks[3])
                            )
                            if response == "":
                                previous_operation = scheduled_tasks[1]
                        else:
                            response = "Cannot repeat operation"
                    else:
                        response = "invalid operation"
                        scheduled_tasks = ["initialize"]
                except IndexError:
                    response = "Incorrect input format"
                    scheduled_tasks = ["initialize"]
                except TypeError:
                    response = "Incorrect input format"
                    scheduled_tasks = ["initialize"]
                except ValueError:
                    response = "Incorrect input parameter"
                    scheduled_tasks = ["initialize"]
                except SyntaxError:
                    response = "Incorrect input format"
                    scheduled_tasks = ["initialize"]

            if "abort" in data:
                scheduled_tasks = []
                initialized = 0
                previous_operation = ""
                response = driver.abort()
            elif len(scheduled_tasks) == 4:
                scheduled_tasks = ["initialize"]

            # send result to scheduler
            print(response)
            client.send(response.encode('utf-8'))

            client.close()
            break
