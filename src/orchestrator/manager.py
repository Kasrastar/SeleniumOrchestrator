from typing_extensions import List, Optional

from selenium.webdriver.chrome.options import Options

from src.orchestrator.selenium_profile import SeleniumProfile


class SeleniumManager:

    instance = None

    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super().__new__(cls, *args, **kwargs)
            cls.profiles: List[SeleniumProfile] = []
        return cls.instance

    def get_or_create_session(
            self,
            driver_name: str,
            tab_name: str,
            options: Options,
            use_cache: bool = False,
            path: Optional[str] = None,
            explicit_wait: int = 5,
            implicit_wait: int = 10,
    ) -> SeleniumProfile:

        driver_instance = self.get_profile(driver_name)
        if driver_instance:
            if driver_instance.is_tab_exist(tab_name):
                return driver_instance
            else:
                driver_instance.open_new_tab(tab_name)
                return driver_instance
        else:
            new_driver_instance = SeleniumProfile(
                name=driver_name,
                tab_name=tab_name,
                options=options,
                use_cache=use_cache,
                explicit_wait=explicit_wait,
                implicit_wait=implicit_wait,
                path=path,
            )
            self.profiles.append(new_driver_instance)
            return new_driver_instance

    def get_profile(self, name: str) -> SeleniumProfile | None:
        for profile in self.profiles:
            if profile.name == name:
                return profile
        return None
