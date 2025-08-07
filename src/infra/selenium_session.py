from typing import Any, Dict, List, Optional

from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException

from ..core.ports import BrowserSessionPort, Locator, WaitCondition
from .browser_factory import BrowserFactory
from ..utils.logger import logger

class SeleniumSession(BrowserSessionPort):
    def __init__(self):
        self.driver = None
        self.factory = BrowserFactory()

    def open(self, browser_type: str, options: Any, connection: Dict[str, Any]) -> None:
        logger.info('send initiate driver reqeuest to browser factory.')
        self.driver = self.factory.create_browser(browser_type, options, connection)
        logger.info('driver stored.')

    def close(self) -> None:
        if self.driver:
            self.driver.quit()
            self.driver = None
    
    def get(self, url: str) -> None:
        if not self.driver:
            raise WebDriverException("Driver not initialized")
        self.driver.get(url)
    
    def new_tab(self) -> str:
        if not self.driver:
            raise WebDriverException("Driver not initialized")
        self.driver.switch_to.new_window()
        return self.driver.current_window_handle

    def switch_tab(self, handle: str) -> None:
        if self.driver:
            self.driver.switch_to.window(handle)

    def close_tab(self, handle: str) -> None:
        if self.driver:
            self.driver.switch_to.window(handle)
            self.driver.close()

    def execute_cdp(self, cmd: str, params: Dict[str, Any]) -> Any:
        if not self.driver:
            raise WebDriverException("Driver not initialized")
        return self.driver.execute_cdp_cmd(cmd, params)

    def execute(self, command: str, params: Dict[str, Any]) -> Any:
        if not self.driver:
            raise WebDriverException("Driver not initialized")
        return self.driver.execute(command, params)

    def find_element(
        self,
        locator: Locator,
        timeout: int = 10,
        condition: str = WaitCondition.PRESENCE_OF_ELEMENT_LOCATED,
        root_element: Optional[WebElement] = None
    ) -> Optional[WebElement]:
        if not self.driver:
            raise WebDriverException("Driver not initialized")

        ec_map = {
            WaitCondition.ELEMENT_TO_BE_CLICKABLE : EC.element_to_be_clickable,
            WaitCondition.PRESENCE_OF_ELEMENT_LOCATED : EC.presence_of_element_located,
            WaitCondition.PRESENCE_OF_ALL_ELEMENTS_LOCATED : EC.presence_of_all_elements_located,
            WaitCondition.VISIBILITY_OF_ELEMENT_LOCATED : EC.visibility_of_element_located,
            WaitCondition.VISIBILITY_OF_ALL_ELEMENTS_LOCATED : EC.visibility_of_all_elements_located,
            WaitCondition.ELEMENT_LOCATED_SELECTION_STATE_TO_BE : EC.element_located_selection_state_to_be,
            WaitCondition.ELEMENT_SELECTION_STATE_TO_BE : EC.element_selection_state_to_be,
            WaitCondition.FRAME_TO_BE_AVAILABLE_AND_SWITCH_TO_IT : EC.frame_to_be_available_and_switch_to_it,
            WaitCondition.INVISIBILITY_OF_ELEMENT : EC.invisibility_of_element,
            WaitCondition.INVISIBILITY_OF_ELEMENT_LOCATED : EC.invisibility_of_element_located,
            WaitCondition.PRESENCE_OF_ALL_ELEMENTS_LOCATED : EC.presence_of_all_elements_located,
            WaitCondition.PRESENCE_OF_ELEMENT_LOCATED : EC.presence_of_element_located,
            WaitCondition.STALENESS_OF : EC.staleness_of,
            WaitCondition.TEXT_TO_BE_PRESENT_IN_ELEMENT : EC.text_to_be_present_in_element,
            WaitCondition.TEXT_TO_BE_PRESENT_IN_ELEMENT_VALUE : EC.text_to_be_present_in_element_value,
            WaitCondition.TITLE_CONTAINS : EC.title_contains,
            WaitCondition.TITLE_IS : EC.title_is,
            WaitCondition.URL_CONTAINS : EC.url_contains,
            WaitCondition.URL_MATCHES : EC.url_matches,
            WaitCondition.URL_TO_BE : EC.url_to_be,
            WaitCondition.VISIBILITY_OF : EC.visibility_of,
            WaitCondition.VISIBILITY_OF_ELEMENT_LOCATED : EC.visibility_of_element_located,
            WaitCondition.VISIBILITY_OF_ALL_ELEMENTS_LOCATED : EC.visibility_of_all_elements_located,
        }
        ec_func = ec_map.get(condition, EC.presence_of_element_located)
        try:
            if root_element:
                # search directly under root
                return root_element.find_element(locator.by, locator.value)
            # top-level search with wait
            return WebDriverWait(self.driver, timeout).until(
                ec_func((locator.by, locator.value))
            )
        except TimeoutException:
            return None

    def find_elements(
        self,
        locator: Locator,
        timeout: int = 10,
        scroll_into_view: bool = False,
        root_element: Optional[WebElement] = None
    ) -> List[WebElement]:
        if not self.driver:
            raise WebDriverException("Driver not initialized")

        try:
            if root_element:
                elements = root_element.find_elements(locator.by, locator.value)
            else:
                elements = WebDriverWait(self.driver, timeout).until(
                    EC.presence_of_all_elements_located((locator.by, locator.value))
                )
            if scroll_into_view:
                for el in elements:
                    try:
                        self.driver.execute_script(
                            "arguments[0].scrollIntoView({block:'center'});", el
                        )
                    except WebDriverException:
                        pass
            return elements
        except TimeoutException:
            return []
