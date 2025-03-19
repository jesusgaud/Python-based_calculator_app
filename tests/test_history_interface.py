import pytest
from app.core.history_interface import HistoryInterface

# Concrete subclass implementing all abstract methods for testing
class ConcreteHistory(HistoryInterface):
    def __init__(self):
        # initialize an empty list to store history entries as (expression, result) tuples
        self.records = []

    def add(self, expression, result):
        # Call base class method (executes abstract method body in HistoryInterface)
        super().add(expression, result)
        # Add the record to history
        self.records.append((expression, result))
        # Return a value to indicate success (could be True or the added record)
        return True

    def get_last(self):
        super().get_last()
        # Return the last record if available, else None
        return self.records[-1] if self.records else None

    def get_all(self):
        super().get_all()
        # Return a copy of all records to avoid external modification
        return list(self.records)

    def search(self, keyword):
        super().search(keyword)
        # Return all records where the keyword is in the expression or result (as string)
        return [
            record for record in self.records
            if keyword in record[0] or keyword in str(record[1])
        ]

    def remove_last(self):
        super().remove_last()
        # Pop the last record if it exists, otherwise return None
        return self.records.pop() if self.records else None

    def clear(self):
        super().clear()
        # Clear all records and return True as confirmation
        self.records.clear()
        return True

    def count(self):
        super().count()
        # Return the number of records currently in history
        return len(self.records)

def test_add_and_retrieve():
    """Test adding entries and retrieving the last entry and all entries."""
    history = ConcreteHistory()
    # After adding an entry, get_last should return that entry, and get_all should include it
    result = history.add("1+1", "2")
    assert result is True  # add returns True on success
    assert history.get_last() == ("1+1", "2")
    assert history.get_all() == [("1+1", "2")]

def test_search_functionality():
    """Test searching within the history records."""
    history = ConcreteHistory()
    # Add multiple entries
    history.add("2+2", "4")
    history.add("3+5", "8")
    history.add("10-3", "7")
    # Search by expression substring
    assert history.search("2+2") == [("2+2", "4")]
    # Search by result value (as string)
    assert history.search("8") == [("3+5", "8")]
    # Search for a term not present
    assert history.search("9") == []

def test_remove_last_and_count():
    """Test removing the last entry and the count method."""
    history = ConcreteHistory()
    # Removing from empty history should yield None
    assert history.remove_last() is None
    # Add two entries
    history.add("5*5", "25")
    history.add("6*6", "36")
    assert history.count() == 2
    # Remove last entry and verify it was the second one added
    removed = history.remove_last()
    assert removed == ("6*6", "36")
    # After removal, count should decrement and last entry should be the first one
    assert history.count() == 1
    assert history.get_last() == ("5*5", "25")

def test_clear_history():
    """Test clearing the history."""
    history = ConcreteHistory()
    history.add("9/3", "3")
    history.add("7-2", "5")
    # Ensure history has entries before clearing
    assert history.count() == 2
    assert history.get_all() == [("9/3", "3"), ("7-2", "5")]
    # Clear history and verify it is empty
    assert history.clear() is True
    assert history.count() == 0
    assert history.get_all() == []
    assert history.get_last() is None

def test_abstract_class_cannot_instantiate():
    """Ensure that HistoryInterface cannot be instantiated directly (abstract)."""
    with pytest.raises(TypeError):
        _ = HistoryInterface()
