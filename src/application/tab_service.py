from typing import Optional, Any

from ..core.ports import BrowserSessionPort
from ..domain.tab import Tab, DefaultTabStatus
from ..domain.driver_status import DefaultDriverStatus

class TabService:
    def __init__(self, session: BrowserSessionPort):
        self.session = session
        self.tabs: list[Tab] = []
        self.driver_status = DefaultDriverStatus.OPEN

    def start(self, browser_type: str, options: Any, connection: dict, first_tab_name: str):
        self.session.open(browser_type, options, connection)
        handle = self.session.new_tab()
        tab = Tab(name=first_tab_name, window_handle=handle, status=DefaultTabStatus.ACTIVE)
        self.tabs.append(tab)

    def new_tab(self, name: str) -> bool:
        if self.driver_status == DefaultDriverStatus.CLOSED:
            return False
        handle = self.session.new_tab()
        for t in self.tabs:
            t.update_status(DefaultTabStatus.INACTIVE)
        tab = Tab(name=name, window_handle=handle, status=DefaultTabStatus.ACTIVE)
        self.tabs.append(tab)
        return True

    def switch_to(self, name: str) -> None:
        tab = self._find(name)
        if not tab:
            return
        self.session.switch_tab(tab.window_handle)
        for t in self.tabs:
            t.update_status(DefaultTabStatus.ACTIVE if t.name == name else DefaultTabStatus.INACTIVE)

    def close_tab(self, name: str) -> None:
        tab = self._find(name)
        if not tab:
            return
        if len(self.tabs) == 1:
            self.close_all()
            return
        self.session.close_tab(tab.window_handle)
        self.tabs.remove(tab)
        # activate first
        self.switch_to(self.tabs[0].name)

    def close_all(self):
        self.session.close()
        self.tabs.clear()
        self.driver_status = DefaultDriverStatus.CLOSED

    def delete_cookies(self, origin: str, storage: str = 'all'):
        if self.driver_status == DefaultDriverStatus.CLOSED:
            return
        self.session.execute_cdp('Storage.clearDataForOrigin', {'origin': origin, 'storageTypes': storage})

    def _find(self, name: str) -> Optional[Tab]:
        return next((t for t in self.tabs if t.name == name), None)