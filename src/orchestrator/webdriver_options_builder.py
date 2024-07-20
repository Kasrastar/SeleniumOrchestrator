from selenium.webdriver.chrome.options import Options


class WebDriverOptionsBuilder:

    # works for now on chrome 
    def __init__(self):
        self.webdriver_options = Options()

    def set_args(self, args: dict):
        for arg_key in args.keys():
            if arg_key == 'argument':
                for arg in args[arg_key]:
                    self.webdriver_options.add_argument(arg)
            if arg_key == 'experimental_options':
                for key in args[arg_key].keys():
                    self.webdriver_options.add_experimental_option(
                        name=key,
                        value=args[arg_key][key]
                    )
            if arg_key == 'capabilities':
                for key in args[arg_key].keys():
                    self.webdriver_options.set_capability(
                        name=key,
                        value=args[arg_key][key]
                    )
