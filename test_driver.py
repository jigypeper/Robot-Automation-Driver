from driver import DeviceDriver

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
