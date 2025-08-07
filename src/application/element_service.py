from typing import Optional, List, Any

from ..core.ports import BrowserSessionPort, Locator, WaitCondition

class ElementService:
    def __init__(self, session: BrowserSessionPort):
        self.session = session
    
    def click(self, locator: Locator, root_handle: Optional[str] = None, root_element: Optional[Any] = None):
        el = self._locate(locator, WaitCondition.ELEMENT_TO_BE_CLICKABLE, root_handle, root_element)
        if el:
            el.click()

    def send_keys(self, locator: Locator, text: str, root_handle: Optional[str] = None, root_element: Optional[Any] = None):
        el = self._locate(locator, WaitCondition.PRESENCE_OF_ELEMENT_LOCATED, root_handle, root_element)
        if el:
            el.send_keys(text)

    def clear(self, locator: Locator, root_handle: Optional[str] = None, root_element: Optional[Any] = None):
        el = self._locate(locator, WaitCondition.PRESENCE_OF_ELEMENT_LOCATED, root_handle, root_element)
        if el:
            el.clear()

    def find_all(self, locator: Locator, timeout: int = 10, root_element: Optional[Any] = None) -> List[Any]:
        return self.session.find_elements(locator, timeout=timeout, scroll_into_view=True, root_element=root_element)

    def _locate(self, locator: Locator, condition: str, root_handle: Optional[str] = None, root_element: Optional[Any] = None) -> Optional[Any]:
        if root_handle:
            self.session.switch_tab(root_handle)
        return self.session.find_element(locator, condition=condition, root_element=root_element)
