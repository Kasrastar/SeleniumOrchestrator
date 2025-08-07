from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By 

class Locator:
    VALID_STRATEGIES = {
        By.ID,
        By.XPATH,
        By.LINK_TEXT,
        By.PARTIAL_LINK_TEXT,
        By.NAME,
        By.TAG_NAME,
        By.CLASS_NAME,
        By.CSS_SELECTOR,
    }

    def __init__(self, by: str, value: str):
        if by not in self.VALID_STRATEGIES:
            raise ValueError(f"Invalid locator strategy: {by}. Must be one of {list(self.VALID_STRATEGIES)}")
        self.by = by
        self.value = value

    def as_tuple(self):
        return self.by, self.value

class WaitCondition:
    ELEMENT_TO_BE_CLICKABLE = 'element_to_be_clickable'
    PRESENCE_OF_ELEMENT_LOCATED = 'presence_of_element_located'
    PRESENCE_OF_ALL_ELEMENTS_LOCATED = 'presence_of_all_elements_located'
    VISIBILITY_OF_ELEMENT_LOCATED = 'visibility_of_element_located'
    VISIBILITY_OF_ALL_ELEMENTS_LOCATED = 'visibility_of_all_elements_located'
    ELEMENT_LOCATED_SELECTION_STATE_TO_BE = 'element_located_selection_state_to_be'
    ELEMENT_SELECTION_STATE_TO_BE = 'element_selection_state_to_be'
    FRAME_TO_BE_AVAILABLE_AND_SWITCH_TO_IT = 'frame_to_be_available_and_switch_to_it'
    INVISIBILITY_OF_ELEMENT = 'invisibility_of_element'
    INVISIBILITY_OF_ELEMENT_LOCATED = 'invisibility_of_element_located'
    PRESENCE_OF_ALL_ELEMENTS_LOCATED = 'presence_of_all_elements_located'
    PRESENCE_OF_ELEMENT_LOCATED = 'presence_of_element_located'
    STALENESS_OF = 'staleness_of'
    TEXT_TO_BE_PRESENT_IN_ELEMENT = 'text_to_be_present_in_element'
    TEXT_TO_BE_PRESENT_IN_ELEMENT_VALUE = 'text_to_be_present_in_element_value'
    TITLE_CONTAINS = 'title_contains'
    TITLE_IS = 'title_is'
    URL_CONTAINS = 'url_contains'
    URL_MATCHES = 'url_matches'
    URL_TO_BE = 'url_to_be'
    VISIBILITY_OF = 'visibility_of'
    VISIBILITY_OF_ELEMENT_LOCATED = 'visibility_of_element_located'
    VISIBILITY_OF_ALL_ELEMENTS_LOCATED = 'visibility_of_all_elements_located'


class BrowserSessionPort(ABC):
    @abstractmethod
    def open(self, browser_type: str, options: Any, connection: Dict[str, Any]):
        pass

    @abstractmethod
    def close(self) -> None:
        pass

    @abstractmethod
    def new_tab(self) -> str:
        """Opens a new tab and returns its window handle"""
        pass

    @abstractmethod
    def switch_tab(self, handle: str) -> None:
        pass

    @abstractmethod
    def close_tab(self, handle: str) -> None:
        pass

    @abstractmethod
    def execute_cdp(self, cmd: str, params: Dict[str, Any]) -> Any:
        pass

    @abstractmethod
    def execute(self, command: str, params: Dict[str, Any]) -> Any:
        pass

    @abstractmethod
    def find_element(
        self, 
        locator: Locator, 
        timeout: int = 10, 
        condition: str = WaitCondition.PRESENCE_OF_ELEMENT_LOCATED,
        root_element: Optional[Any] = None
    ) -> Any:
        pass

    @abstractmethod
    def find_elements(
        self, 
        locator: Locator, 
        timeout: int = 10, 
        scroll_into_view: bool = False,
        root_element: Optional[Any] = None
    ) -> List[Any]:

        pass