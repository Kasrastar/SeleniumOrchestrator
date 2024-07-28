from selenium.webdriver.remote.webelement import WebElement
from typing_extensions import Optional

from chromedriver_py import binary_path
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import selenium.webdriver.support.expected_conditions as ec
from selenium.common.exceptions import (
    SessionNotCreatedException,
    NoSuchElementException
)

from src.orchestrator.enums import DefaultTabStatus, DefaultDriverStatus
from src.orchestrator.tab import Tab


class SeleniumProfile:

    def __init__(
            self,
            name: str,
            tab_name: str,
            options: Options,
            use_cache: bool = False,
            path: Optional[str] = None,
            explicit_wait: int = 5,
            implicit_wait: int = 10,
    ):
        self.status: DefaultDriverStatus = None  # noqa
        self.driver: Chrome = None  # noqa
        self.tabs: list[Tab] = []
        self.name = name
        self.path = path
        self.options = options
        self.explicit_wait = explicit_wait
        self.create_session(tab_name, implicit_wait, use_cache)

    def create_session(
            self,
            tab_name: str,
            implicit_wait: int,
            use_cache: bool = False
    ) -> None:
        try:
            if use_cache:
                self.options.add_argument('--user-data-dir=%s' % self.path)
            self.driver = Chrome(
                service=Service(
                    executable_path=binary_path
                ),
                options=self.options
            )
        except SessionNotCreatedException as e:
            ...
            # if not hasattr(SeleniumProfile, 'driver'):
            #     raise SeleniumErrors(str(e))

        self.status = DefaultDriverStatus.OPEN
        self.driver.implicitly_wait(implicit_wait)
        self.tabs.append(Tab(
            name=tab_name,
            window_handle=self.driver.current_window_handle,
            status=DefaultTabStatus.ACTIVE
        ))

    def get_tab(self, name: str) -> Tab | None:
        for tab in self.tabs:
            if tab.name == name:
                return tab
        return None

    def update_driver_status(self, status: DefaultDriverStatus):
        self.status = status

    def update_tab_status(self, name: str, status: DefaultTabStatus):
        selected_tab = self.get_tab(name)
        if selected_tab:
            selected_tab.status = status

    def is_tab_exist(self, name: str) -> bool:
        selected_tab = self.get_tab(name)
        if selected_tab:
            return True
        return False

    def close_driver(self):
        if not self.status == DefaultDriverStatus.CLOSED:
            self.status = DefaultDriverStatus.CLOSED
            self.driver.quit()

    def close_tab(self, name: str):
        selected_tab = self.get_tab(name)
        if selected_tab:
            if len(self.tabs)-1 == 0:
                self.close_driver()
            else:
                self.switch_to_tab(selected_tab.name)
                self.driver.close()
                self.tabs.remove(selected_tab)
                self.switch_to_tab(self.tabs[0].name)

    def open_new_tab(self, name: str):
        if not self.status == DefaultDriverStatus.CLOSED:
            self.driver.switch_to.new_window()
            self.tabs.append(Tab(
                name=name,
                window_handle=self.driver.current_window_handle,
                status=DefaultTabStatus.ACTIVE
            ))

        for tab in self.tabs:
            if tab.name != name:
                self.update_tab_status(tab.name, DefaultTabStatus.INACTIVE)

    def switch_to_tab(self, name: str):
        selected_tab = self.get_tab(name)
        if selected_tab and not self.status == DefaultDriverStatus.CLOSED:
            self.driver.switch_to.window(selected_tab.window_handle)

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

    def element_locator(self, by: By, addr: str) -> WebElement | None:
        if not self.status == DefaultDriverStatus.CLOSED:
            try:
                element = WebDriverWait(self.driver, self.explicit_wait).until(
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
        if not self.status == DefaultDriverStatus.CLOSED:
            self.close_driver()
