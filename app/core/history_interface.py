from abc import ABC, abstractmethod

class HistoryInterface(ABC):
    """Abstract base class defining the interface for calculator history."""
    @abstractmethod
    def add(self, expression, result):
        """Add a calculation record (expression and result) to the history."""
        pass
    @abstractmethod
    def get_last(self):
        """Retrieve the last recorded calculation."""
        pass
    @abstractmethod
    def get_all(self):
        """Retrieve all calculation records."""
        pass
    @abstractmethod
    def search(self, keyword):
        """Search the history for records containing the given keyword."""
        pass
    @abstractmethod
    def remove_last(self):
        """Remove the last record and return it."""
        pass
    @abstractmethod
    def clear(self):
        """Clear all history records."""
        pass
    @abstractmethod
    def count(self):
        """Return the number of records in the history."""
        pass
