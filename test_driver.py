from driver import DeviceDriver, data_handler

driver = DeviceDriver()


# Execute test
def test_execute():
    result = driver.execute_operation("apple", ["place"], [60])

    assert result == "Not a valid operation."


# Pick test
def test_pick():
    result = driver.execute_operation("pick", ["Destination"], [80])

    assert result == "Wrong combination of parameters"


# Place test
def test_place():
    result = driver.execute_operation("place", ["Source"], [80])

    assert result == "Wrong combination of parameters"


# Transfer test
def test_transfer():
    result = driver.execute_operation("transfer", ["origin", "apple"], [80, 100])

    assert result == "Wrong combination of parameters"


# Initialize test
def test_initialize():
    result, scheduled_tasks, initialized, previous_operation = data_handler("initialize", driver, [], 0, "")

    assert result == ""


# Multiple initialization test
def test_initialize_twice():
    result, scheduled_tasks, initialized, previous_operation = data_handler("initialize", driver, ["initialize"], 1, "")

    assert result == "Already initialized"


# Hasn't been initialized test
def test_initialize_not():
    result, scheduled_tasks, initialized, previous_operation = data_handler("pick", driver, [], 0, "")

    assert result == "Not initialized"


# Invalid operation test
def test_invalid_operation():
    result, scheduled_tasks, initialized, previous_operation = data_handler("mango", driver, ["initialize"], 1, "")

    assert result == "invalid operation"


# Invalid combination of parameters test
def test_wrong_combination():
    result, scheduled_tasks, initialized, previous_operation = data_handler("place ['Source'] [70]", driver, ["initialize"], 1, "")

    assert result == "Wrong combination of parameters"


# Invalid combination of parameters test 2
def test_wrong_combination_2():
    result, scheduled_tasks, initialized, previous_operation = data_handler("pick ['Destination'] [70]", driver, ["initialize"], 1, "")

    assert result == "Wrong combination of parameters"


# Invalid combination of parameters test 3
def test_wrong_combination_3():
    result, scheduled_tasks, initialized, previous_operation = data_handler("pick ['Destination','Source'] [70,80]", driver, ["initialize"], 1, "")

    assert result == "Wrong combination of parameters"


# TypeError test
def test_incorrect_input():
    result, scheduled_tasks, initialized, previous_operation = data_handler("pick ['Source'] ['70']", driver, ["initialize"], 1, "")

    assert result == "Incorrect input format, parameter values incorrect"


# ValueError test
def test_incorrect_input_2():
    result, scheduled_tasks, initialized, previous_operation = data_handler("place [Destination] ['70']", driver, ["initialize"], 1, "")

    assert result == "Incorrect input format, make sure to use brackets or exclamation marks"


# SyntaxError test
def test_incorrect_input_3():
    result, scheduled_tasks, initialized, previous_operation = data_handler("pick ['Source'] ['70]", driver, ["initialize"], 1, "")

    assert result == "Incorrect input format, make sure to use brackets or exclamation marks"


# IndexError test
def test_incorrect_input_4():
    result, scheduled_tasks, initialized, previous_operation = data_handler("transfer ['Source'] [60,70]", driver, ["initialize"], 1, "")

    assert result == "Incorrect input format, list parameter mismatch"


# operation order test
def test_transfer_after_pick():
    result, scheduled_tasks, initialized, previous_operation = data_handler("transfer ['Destination','Source'] [70,80]", driver, ["initialize"], 1, "pick")

    assert result == "Cannot run transfer operation following pick"


# repetitive operation test
def test_pick_after_pick():
    result, scheduled_tasks, initialized, previous_operation = data_handler("pick ['Source'] [70]", driver, ["initialize"], 1, "pick")

    assert result == "Cannot repeat operation"
