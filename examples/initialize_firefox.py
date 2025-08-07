from src.core.ports import Locator
from src.application.profile_service import ProfileService
from src.infra.browser_config_builder import BrowserConfigBuilder
from src.infra.selenium_session import SeleniumSession
from src.utils.logger import logger

from selenium.webdriver.common.keys import Keys


options = BrowserConfigBuilder('firefox').set_browser_profile('/home/kasrastar/Desktop/random').build()
session = SeleniumSession()
profile_service = ProfileService()

new_profile = profile_service.new_profile(
    driver_name='test_driver',
    tab_name='initial_tab',
    session=session,
    profile_options=options,
    connection={
        'browser_type': 'firefox',
        'binary_path':  '/usr/bin/geckodriver'
    }
)

# localhost:53399 remote driver

logger.info('Profile created successfully')

url = 'https://www.google.com'
new_profile.session.get(url)
logger.info(f'Navigated to {url}')
