# --- application/profile_manager.py ---
from typing import Dict, List, Optional

from ..infra.browser_config_builder import BrowserConfigBuilder
from ..infra.selenium_session import SeleniumSession
from ..domain.driver_status import DefaultDriverStatus
from ..domain.tab import Tab, DefaultTabStatus
from ..application.tab_service import TabService
from ..application.element_service import ElementService
from ..utils.logger import logger


class Profile:
    def __init__(self, driver_name: str, tab_name: str, session: SeleniumSession, profile_options: BrowserConfigBuilder, connection: dict):
        self.driver_name = driver_name
        self.session = session
        self.driver_status = DefaultDriverStatus.OPEN
        self.tabs: List[Tab] = []
        self.tab_service = TabService(session)
        self.element_service = ElementService(session)

        logger.info('requet to initiate new driver.')
        self.session.open(
            browser_type=connection.get('browser_type', 'chrome'),
            options=profile_options,
            connection=connection
        )
        
        # print(self.session.driver)
        window_handle = self.session.driver.current_window_handle  # type: ignore
        self.tabs.append(
            Tab(
                name=tab_name, 
                window_handle=window_handle, 
                status=DefaultTabStatus.ACTIVE
            )
        )
        
    def close(self):
        self.session.close()
        self.driver_status = DefaultDriverStatus.CLOSED

    def new_tab(self, tab_name: str):
        handle = self.session.new_tab()
        # Set current active tab to inactive
        for tab in self.tabs:
            if tab.status == DefaultTabStatus.ACTIVE:
                tab.update_status(DefaultTabStatus.INACTIVE)
        # Add new tab as active
        self.tabs.append(Tab(name=tab_name, window_handle=handle, status=DefaultTabStatus.ACTIVE))
        self.session.switch_tab(handle)

    def get_active_tab(self) -> Optional[Tab]:
        return next((tab for tab in self.tabs if tab.status == DefaultTabStatus.ACTIVE), None)


class ProfileManager:
    def __init__(self):
        self.profiles: Dict[str, Profile] = {}

    def new_profile(
        self,
        driver_name: str,
        tab_name: str,
        session: SeleniumSession, 
        profile_options: BrowserConfigBuilder,
        connection: dict 
    ) -> Profile:
        if driver_name in self.profiles:
            logger.info('retriving existing profile.')
            return self.profiles[driver_name]
        logger.info('initiate new profile.')
        profile = Profile(driver_name, tab_name, session, profile_options, connection)
        self.profiles[driver_name] = profile
        return profile

    def remove_profile(self, driver_name: str):
        profile = self.profiles.get(driver_name)
        if profile:
            profile.close()
            del self.profiles[driver_name]

    def new_tab_profile(self, driver_name: str, tab_name: str):
        profile = self.profiles.get(driver_name)
        if profile:
            profile.new_tab(tab_name)

    def get_profile(self, driver_name: str) -> Optional[Profile]:
        return self.profiles.get(driver_name)