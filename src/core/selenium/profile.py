import selenium
from selenium.webdriver.remote.webelement import WebElement

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import selenium.webdriver.support.expected_conditions as ec
from selenium.common.exceptions import NoSuchElementException

from ..browser.browser_factory import BrowserFactory
from ..browser.browser_config_builder import BrowserConfigBuilder
from ..enums import DefaultTabStatus, DefaultDriverStatus
from .tab import Tab

class SeleniumProfile:

    def __init__(
            self,
            driver_name: str,
            tab_name: str,
            profile_options: BrowserConfigBuilder,
            connection: dict
    ):

        self.tabs: list[Tab] = []
        self.driver_name = driver_name
        self.driver: selenium.webdriver.common = None
        self.status: DefaultDriverStatus = DefaultDriverStatus.OPEN
        
        self.create_session(
            browser_name=connection.get('browser_type', 'chrome'),
            tab_name=tab_name,
            options=profile_options,
            connection=connection
        )

    def create_session(
            self,
            browser_name: str,
            tab_name: str,
            options: BrowserConfigBuilder,
            connection: dict
    ) -> None:
        driver_factory: BrowserFactory = BrowserFactory()
        self.driver = driver_factory.create_browser(
            browser_name=browser_name,
            options=options,
            connection=connection
        )
        new_tab = Tab(
            name=tab_name,
            window_handle=self.driver.current_window_handle,
            status=DefaultTabStatus.ACTIVE
        )
        self.tabs.append(new_tab)

    def get_tab(self, name: str) -> Tab | None:
        """
        Retrieves a tab by its name.

        :param name: The name of the tab to retrieve.
        :return: The Tab object if found, otherwise None.
        """
        return next((tab for tab in self.tabs if tab.name == name), None)

    def update_driver_status(self, status: DefaultDriverStatus):
        """
        Updates the status of the driver.
        :param status: The new status to set for the driver.
        """
        self.status = status

    def update_tab_status(self, name: str, new_status: DefaultTabStatus):
        """
        Updates the status of a tab identified by its name.
        :param name: The name of the tab to update.
        :param new_status: The new status for the tab.
        """
        tab = self.get_tab(name)
        if tab:
            tab.update_status(new_status)

    def is_tab_exist(self, name: str) -> bool:
        """
        Checks if a tab with the given name exists.
        :param name: The name of the tab to check.
        :return: True if the tab exists, False otherwise.
        """
        return any(tab.name == name for tab in self.tabs)

    def close_driver(self):
        if not self.status == DefaultDriverStatus.CLOSED:
            self.status = DefaultDriverStatus.CLOSED
            self.driver.quit()

    def close_tab(self, name: str):
        selected_tab = self.get_tab(name)
        if selected_tab:
            if len(self.tabs) - 1 == 0:
                self.close_driver()
            else:
                self.switch_to_tab(selected_tab.name)
                self.driver.close()
                self.tabs.remove(selected_tab)
                self.switch_to_tab(self.tabs[0].name)

    def new_tab(self, name: str) -> bool:
        if not self.status == DefaultDriverStatus.CLOSED:
            self.driver.switch_to.new_window()

            new_tab = Tab(
                name=name,
                window_handle=self.driver.current_window_handle,
                status=DefaultTabStatus.ACTIVE
            )

            self.tabs.append(new_tab)
            [tab.update_status(DefaultTabStatus.INACTIVE) for tab in self.tabs if tab.name != name]
            return True
        else:
            return False

    def switch_to_tab(self, name: str):
        if not self.status == DefaultDriverStatus.CLOSED:
            tab = self.get_tab(name)
            if tab:
                self.driver.switch_to.window(tab.window_handle)

    def get_tab_status(self, name: str) -> DefaultTabStatus:
        selected_tab = self.get_tab(name)
        if selected_tab:
            return selected_tab.status

    def delete_all_cookies(self, origin: str, storage_type: str = 'all') -> None:
        if not self.status == DefaultDriverStatus.CLOSED:
            self.driver.execute_cdp_cmd('Storage.clearDataForOrigin', {
                "origin": origin,
                "storageTypes": storage_type,
            })

    def element_locator(self, by: By, addr: str, explicit_wait: int = 10) -> WebElement | None:
        if not self.status == DefaultDriverStatus.CLOSED:
            try:
                element = WebDriverWait(self.driver, explicit_wait).until(
                    ec.presence_of_element_located((  # noqa
                        by, addr
                    ))
                )
                return element
            except NoSuchElementException:
                pass
        return None

    def clicker(self, by: By, addr: str) -> None:
        element = self.element_locator(by, addr)
        if element:
            element.click()

    def sender(self, by: By, addr: str, msg: str) -> None:
        element = self.element_locator(by, addr)
        if element:
            element.send_keys(msg)

    def cleaner(self, by: By, addr: str) -> None:
        element = self.element_locator(by, addr)
        if element:
            element.clear()

    def __del__(self):
        if not self.status == DefaultDriverStatus.CLOSED and not self.driver is None:
            self.close_driver()
