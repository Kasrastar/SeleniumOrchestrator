from src.orchestrator.enums import DefaultTabStatus


class Tab:
    def __init__(self, name: str, window_handle: str, status: DefaultTabStatus):
        self.name = name
        self.window_handle = window_handle
        self.status = status

    def update_name(self, new_name: str):
        """
        Updates the name of the tab.
        :param new_name: New name for the tab.
        """
        self.name = new_name

    def update_status(self, new_status: DefaultTabStatus):
        """
        Updates the status of the tab.
        :param new_status: New status for the tab.
        """
        self.status = new_status

    def is_active(self) -> bool:
        """
        Checks if the tab is active based on its status.
        :return: True if the tab is active, False otherwise.
        """
        return self.status == DefaultTabStatus.ACTIVE

    def __str__(self):
        """
        Returns a human-readable string representation of the Tab object.
        :return: String representation of the tab's name, status, and window handle.
        """
        return f"Tab(name={self.name}, status={self.status}, window_handle={self.window_handle})"

    def __repr__(self):
        """
        Provides a more formal string representation of the Tab object.
        :return: A formal string representation for debugging.
        """
        return f"Tab(name={self.name!r}, window_handle={self.window_handle!r}, status={self.status!r})"

    def close(self):
        """
        Placeholder method for closing the tab.
        In a real-world scenario, this could interface with Selenium to close the tab.
        """
        print(f"Closing tab: {self.name} with window handle {self.window_handle}")
        # In a real implementation, you would use something like:
        # driver.switch_to.window(self.window_handle)
        # driver.close()

    def get_info(self):
        """
        Returns a dictionary with the tab's information.
        :return: A dictionary containing the tab's name, status, and window handle.
        """
        return {
            "name": self.name,
            "window_handle": self.window_handle,
            "status": self.status
        }
