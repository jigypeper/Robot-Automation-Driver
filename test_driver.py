from driver import DeviceDriver

robot = DeviceDriver()


def test_execute():
    result = robot.execute_operation("apple", ["place"], [60])

    assert result == "Not a valid operation."


def test_pick():
    result = robot.execute_operation("pick", ["Destination"], [80])

    assert result == "Wrong combination of parameters"


def test_place():
    result = robot.execute_operation("place", ["Source"], [80])

    assert result == "Wrong combination of parameters"


def test_transfer():
    result = robot.execute_operation("transfer", ["origin", "apple"], [80, 100])

    assert result == "Wrong combination of parameters"
