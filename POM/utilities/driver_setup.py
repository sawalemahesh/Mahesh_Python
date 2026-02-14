from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

from POM.utilities.config_reader import read_config


class DriverSetup:
    driver = None

    @staticmethod
    def get_driver():
        if DriverSetup.driver is None:
            browser = read_config("BROWSER", "browser")
            implicit_wait = int(read_config("BROWSER", "implicit_wait"))
            page_load_timeout = int(read_config("BROWSER", "page_load_timeout"))

            if browser.lower() == "chrome":
                chrome_options = Options()
                chrome_options.add_argument("--start-maximized")

                service = Service(ChromeDriverManager().install())
                DriverSetup.driver = webdriver.Chrome(
                    service=service,
                    options=chrome_options
                )

            else:
                raise Exception("Browser not supported")

            DriverSetup.driver.implicitly_wait(implicit_wait)
            DriverSetup.driver.set_page_load_timeout(page_load_timeout)

        return DriverSetup.driver

    @staticmethod
    def quit_driver():
        if DriverSetup.driver:
            DriverSetup.driver.quit()
            DriverSetup.driver = None
