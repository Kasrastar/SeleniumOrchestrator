from selenium.webdriver.chrome.options import Options
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DOWNLOAD_DIR = BASE_DIR / 'downloads'


chrome_driver_options = Options()


args: dict = {
    'argument': [
        # 'headless',  # run in background
        'start-maximized',
        # '--no-sandbox',
        # '--disable-web-security',
        # '--allow-running-insecure-content'
    ],
    'experimental_options': {
        'excludeSwitches': [
            'disable-popup-blocking',
            'enable-logging'
        ],
        'prefs': {
            'download.default_directory': str(DOWNLOAD_DIR),
            'download.prompt_for_download': False,
            'download.directory_upgrade': True,
            'safebrowsing.enabled': True
        },
        # 'detach': False,  # don't close driver after running
    },
    'capabilities': {
        'goog:loggingPrefs': {
            'performance': 'ALL',
            'browser': 'ALL'
        }
    }
}


def add_options():
    for arg_key in args.keys():
        if arg_key == 'argument':
            for arg in args[arg_key]:
                chrome_driver_options.add_argument(arg)
        if arg_key == 'experimental_options':
            for key in args[arg_key].keys():
                chrome_driver_options.add_experimental_option(
                    name=key,
                    value=args[arg_key][key]
                )

        if arg_key == 'capabilities':
            for key in args[arg_key].keys():
                chrome_driver_options.set_capability(
                    name=key,
                    value=args[arg_key][key]
                )


add_options()
