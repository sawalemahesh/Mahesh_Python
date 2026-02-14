import pytest
from POM.utilities.driver_setup import DriverSetup
from POM.utilities.config_reader import read_config


@pytest.fixture(scope="function")
def setup():
    driver = DriverSetup.get_driver()
    driver.get(read_config("APP", "base_url"))
    yield driver
    DriverSetup.quit_driver()
