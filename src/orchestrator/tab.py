from src.orchestrator.enums import DefaultTabStatus


class Tab:

    def __init__(self, name: str, window_handle: str, status: DefaultTabStatus):

        self.name = name
        self.window_handle = window_handle
        self.status = status

