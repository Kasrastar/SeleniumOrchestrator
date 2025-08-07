from src.application.profile_service import ProfileService
from src.infra.browser_config_builder import BrowserConfigBuilder
from src.infra.selenium_session import SeleniumSession
from src.utils.logger import logger



remote_connections = {
    'browser_type': 'remote',
    'remote_url': 'http://localhost:7997/wd/hub',
}

# due the remote driver, is chrome-standalone, the options should be chrome type
options = BrowserConfigBuilder('chrome').set_browser_profile('/home/kasrastar/Desktop/random').build()
session = SeleniumSession()
profile_service = ProfileService()

new_profile = profile_service.new_profile(
    driver_name='test_driver',
    tab_name='initial_tab',
    session=session,
    profile_options=options,
    connection=remote_connections
)

url = 'https://demoqa.com'
new_profile.session.get(url)
logger.info('Navigated to demoqa.com')
