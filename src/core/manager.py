from typing_extensions import List, Optional

from selenium.webdriver.chrome.options import Options

from .selenium.profile import SeleniumProfile
from .browser.browser_config_builder import BrowserConfigBuilder


class SeleniumManager:

    def __init__(self):
        self.profiles: list[SeleniumProfile] = []

    def new_profile(
            self,
            driver_name: str,
            tab_name: str,
            profile_options: BrowserConfigBuilder,
            connection: dict
    ):
        instance = self.get_profile(driver_name)
        if instance:
            return instance
        else:
            new_instance = SeleniumProfile(
                driver_name=driver_name,
                tab_name=tab_name,
                profile_options=profile_options,
                connection=connection
            )
            self.profiles.append(new_instance)
            return new_instance

    def remove_profile(self, driver_name: str):
        instance = self.get_profile(driver_name)
        if instance:
            instance.close_driver()
            self.profiles.remove(instance)

    def new_tab_profile(self, driver_name: str, tab_name: str):
        instance = self.get_profile(driver_name)
        if instance:
            instance.new_tab(tab_name)

    def get_profile(self, name: str) -> SeleniumProfile | None:
        """
        Retrieves a profile by its name.

        :param name: The name of the profile to retrieve.
        :return: The SeleniumProfile object if found, otherwise None.
        """
        return next((profile for profile in self.profiles if profile.driver_name == name), None)
