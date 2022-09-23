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


def data_handler(operation: str, driver_instance: DeviceDriver,
                 operation_list: list, initialized_check: int, previous_task: str):
    if operation != "initialize":
        # Create list from operation
        operation = operation.split()

    print("Received", operation, "from the client")

    # Add received operation to scheduled tasks list
    if operation not in operation_list:
        if type(operation) == list:
            operation_list.extend(operation)
        else:
            operation_list.append(operation)

    print(operation_list)

    # Check for initialization as first operation
    if operation_list[0] == "initialize" and initialized_check == 0:
        response = driver_instance.initialize()
        # Ensure initialization is successful
        if "Error" in response:
            while "Error" in response and initialized_check == 0:
                response = driver_instance.initialize()
                if response == "":
                    initialized_check += 1
                    return response, operation_list, initialized_check, previous_task
        else:
            operation_list = ["initialize"]
            initialized_check += 1
            return response, operation_list, initialized_check, previous_task
    elif operation_list[0] == "initialize" and initialized_check == 1 and operation == "initialize":
        response = "Already initialized"
        operation_list = ["initialize"]
        return response, operation_list, initialized_check, previous_task
    elif operation_list[0] != "initialize" and operation != "initialize":
        response = "Not initialized"
        operation_list = []
        initialized_check = 0
        return response, operation_list, initialized_check, previous_task

    # execute operation only if initialized and not abort
    if len(operation_list) > 1 and operation_list[0] == "initialize" and operation_list[1] != "abort":
        try:
            print(operation_list)
            if operation_list[1] in driver_instance.operations \
                    and ("Destination" in ast.literal_eval(operation_list[2])
                            or "Source" in ast.literal_eval(operation_list[2])):
                # make sure operation isn't repeated if response is successful
                if previous_task == "pick" \
                        and operation_list[1] == "transfer":
                    response = "Cannot run transfer operation following pick"
                    operation_list = ["initialize"]
                    initialized_check = 1
                    previous_task = "pick"
                    return response, operation_list, initialized_check, previous_task
                elif previous_task != operation_list[1]:
                    response = driver_instance.execute_operation(
                        operation_list[1],
                        ast.literal_eval(operation_list[2]),
                        ast.literal_eval(operation_list[3])
                    )
                    if response == "":
                        previous_task = operation_list[1]
                        initialized_check = 1
                        operation_list = ["initialize"]
                        return response, operation_list, initialized_check, previous_task
                else:
                    response = "Cannot repeat operation"
                    previous_task = operation_list[1]
                    operation_list = ["initialize"]
                    initialized_check = 1
                    return response, operation_list, initialized_check, previous_task
            else:
                response = "invalid operation"
                operation_list = ["initialize"]
                return response, operation_list, initialized_check, previous_task
        except IndexError:
            response = "Incorrect input format, list parameter mismatch"
            operation_list = ["initialize"]
            return response, operation_list, initialized_check, previous_task
        except TypeError:
            response = "Incorrect input format, parameter values incorrect"
            operation_list = ["initialize"]
            return response, operation_list, initialized_check, previous_task
        except ValueError:
            response = "Incorrect input format, make sure to use brackets or exclamation marks"
            operation_list = ["initialize"]
            return response, operation_list, initialized_check, previous_task
        except SyntaxError:
            response = "Incorrect input format, make sure to use brackets or exclamation marks"
            operation_list = ["initialize"]
            return response, operation_list, initialized_check, previous_task

    if "abort" in operation:
        operation_list = []
        initialized_check = 0
        previous_task = ""
        response = driver_instance.abort()
        return response, operation_list, initialized_check, previous_task
    elif len(operation_list) == 4:
        operation_list = ["initialize"]
        return response, operation_list, initialized_check, previous_task


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
        print("Start listening on", driver.ip, ":", driver.port)
        client, addr = driver.server.accept()
        print("Received connection from", addr[0], ":", addr[1])
        while True:
            # Listen for operation
            data = client.recv(1024).decode("utf-8")

            result, scheduled_tasks, initialized, previous_operation = data_handler(
                data, 
                driver, 
                scheduled_tasks, 
                initialized, 
                previous_operation
            )

            # send result to scheduler
            print(scheduled_tasks)
            print(initialized)
            print(result)
            client.send(result.encode("utf-8"))

            client.close()
            break
