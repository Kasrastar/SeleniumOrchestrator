from .selenium.profile import SeleniumProfile
from .browser.browser_config_builder import BrowserConfigBuilder


# The `SeleniumManager` class manages Selenium profiles, allowing for the creation, removal, and
# retrieval of profiles associated with different drivers and tabs.
class SeleniumManager:

    def __init__(self):
        """
        The `__init__` function initializes an empty list of `SeleniumProfile` objects in a Python
        class.
        """
        self.profiles: list[SeleniumProfile] = []

    def new_profile(
            self,
            driver_name: str,
            tab_name: str,
            profile_options: BrowserConfigBuilder,
            connection: dict
    ):
        """
        The `new_profile` function creates a new Selenium profile if one does not already exist for the
        specified driver and tab.
        
        :param driver_name: The `driver_name` parameter in the `new_profile` function is a string that
        represents the name of the driver being used for the Selenium profile. It could be something
        like "Chrome", "Firefox", "Safari", etc
        :type driver_name: str
        :param tab_name: The `tab_name` parameter in the `new_profile` function is a string that
        represents the name of the tab associated with the profile being created. It is used as a
        reference to identify the specific tab within the browser profile
        :type tab_name: str
        :param profile_options: The `profile_options` parameter in the `new_profile` function is of type
        `BrowserConfigBuilder`. This parameter likely contains configuration options and settings for
        the browser profile being created. It is used to customize the behavior and settings of the
        Selenium profile being instantiated in the function
        :type profile_options: BrowserConfigBuilder
        :param connection: The `connection` parameter in the `new_profile` function is expected to be a
        dictionary containing information related to the connection settings or details needed for the
        Selenium profile. This could include details such as host, port, username, password, or any
        other connection-related information required for the Selenium profile to establish
        :type connection: dict
        :return: The `new_profile` method returns either an existing instance of a SeleniumProfile if
        one already exists for the specified driver_name, or it creates a new instance of
        SeleniumProfile with the provided parameters (driver_name, tab_name, profile_options,
        connection), adds it to the list of profiles, and then returns the new instance.
        """
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
        """
        The function removes a profile associated with a specific driver name.
        
        :param driver_name: The `driver_name` parameter is a string that represents the name of the
        driver profile that you want to remove from the list of profiles
        :type driver_name: str
        """
        instance = self.get_profile(driver_name)
        if instance:
            instance.close_driver()
            self.profiles.remove(instance)

    def new_tab_profile(self, driver_name: str, tab_name: str):
        """
        The function `new_tab_profile` creates a new tab in a specified driver profile.
        
        :param driver_name: The `driver_name` parameter is a string that represents the name of the
        driver for which you want to create a new tab profile
        :type driver_name: str
        :param tab_name: The `tab_name` parameter in the `new_tab_profile` method refers to the name of
        the new tab that will be created within the profile associated with the specified `driver_name`
        :type tab_name: str
        """
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
