from enum import Enum


class DefaultTabStatus(Enum):
    ACTIVE = 'active'
    INACTIVE = 'inactive'


class Tab:
    def __init__(self, name: str, window_handle: str, status: DefaultTabStatus):
        self.name = name
        self.window_handle = window_handle
        self.status = status

    def update_name(self, new_name: str):
        self.name = new_name

    def update_status(self, new_status: DefaultTabStatus):
        self.status = new_status

    def is_active(self) -> bool:
        return self.status == DefaultTabStatus.ACTIVE

    def __str__(self):
        return f"Tab(name={self.name}, status={self.status}, window_handle={self.window_handle})"

    def __repr__(self):
        return f"Tab(name={self.name!r}, window_handle={self.window_handle!r}, status={self.status!r})"

    def close(self):
        print(f"Closing tab: {self.name} with window handle {self.window_handle}")
        # In a real implementation, you would use something like:
        # driver.switch_to.window(self.window_handle)
        # driver.close()

    def get_info(self):
        return {
            "name": self.name,
            "window_handle": self.window_handle,
            "status": self.status
        }
