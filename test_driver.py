from driver import DeviceDriver, data_handler

driver = DeviceDriver()


def test_execute():
    result = driver.execute_operation("apple", ["place"], [60])

    assert result == "Not a valid operation."


def test_pick():
    result = driver.execute_operation("pick", ["Destination"], [80])

    assert result == "Wrong combination of parameters"


def test_place():
    result = driver.execute_operation("place", ["Source"], [80])

    assert result == "Wrong combination of parameters"


def test_transfer():
    result = driver.execute_operation("transfer", ["origin", "apple"], [80, 100])

    assert result == "Wrong combination of parameters"


def test_initialize():
    result, scheduled_tasks, initialized, previous_operation = data_handler("initialize", driver, [], 0, "")

    assert result == ""


def test_initialize_twice():
    result, scheduled_tasks, initialized, previous_operation = data_handler("initialize", driver, ["initialize"], 1, "")

    assert result == "Already initialized"


def test_initialize_not():
    result, scheduled_tasks, initialized, previous_operation = data_handler("pick", driver, [], 0, "")

    assert result == "Not initialized"


def test_invalid_operation():
    result, scheduled_tasks, initialized, previous_operation = data_handler("mango", driver, ["initialize"], 1, "")

    assert result == "invalid operation"


def test_wrong_combination():
    result, scheduled_tasks, initialized, previous_operation = data_handler("place ['Source'] [70]", driver, ["initialize"], 1, "")

    assert result == "Wrong combination of parameters"


def test_wrong_combination_2():
    result, scheduled_tasks, initialized, previous_operation = data_handler("pick ['Destination'] [70]", driver, ["initialize"], 1, "")

    assert result == "Wrong combination of parameters"


def test_wrong_combination_3():
    result, scheduled_tasks, initialized, previous_operation = data_handler("pick ['Destination','Source'] [70,80]", driver, ["initialize"], 1, "")

    assert result == "Wrong combination of parameters"


def test_incorrect_input():
    result, scheduled_tasks, initialized, previous_operation = data_handler("pick ['Source'] ['70']", driver, ["initialize"], 1, "")

    assert result == "Incorrect input format, parameter values incorrect"


def test_incorrect_input_2():
    result, scheduled_tasks, initialized, previous_operation = data_handler("place [Destination] ['70']", driver, ["initialize"], 1, "")

    assert result == "Incorrect input format, make sure to use brackets or exclamation marks"


def test_incorrect_input_3():
    result, scheduled_tasks, initialized, previous_operation = data_handler("pick ['Source'] ['70]", driver, ["initialize"], 1, "")

    assert result == "Incorrect input format, make sure to use brackets or exclamation marks"


def test_transfer_after_pick():
    result, scheduled_tasks, initialized, previous_operation = data_handler("transfer ['Destination','Source'] [70,80]", driver, ["initialize"], 1, "pick")

    assert result == "Cannot run transfer operation following pick"


def test_pick_after_pick():
    result, scheduled_tasks, initialized, previous_operation = data_handler("pick ['Source'] [70]", driver, ["initialize"], 1, "pick")

    assert result == "Cannot repeat operation"
