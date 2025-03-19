import pytest
from app.calculations_global import Calculations

# Auto-use fixture to reset singleton before and after each test
@pytest.fixture(autouse=True)
def reset_calculations():
    Calculations._reset_instance()    # ensure a new instance for each test
    yield
    Calculations._reset_instance()    # clean up instance after test

def test_singleton_identity():
    """Calculations() should return a singleton instance."""
    calc1 = Calculations()
    calc2 = Calculations()
    assert calc1 is calc2, "Calculations should be a singleton (same instance)"
    # Ensure that repeated instantiation did not reinitialize state
    calc1.add_history("X")
    # Calling Calculations() again returns the same instance with existing state
    calc3 = Calculations()
    assert "X" in calc3.get_history(), "Singleton instance should retain history between calls"

def test_history_operations():
    """Test add_history, get_history, and clear_history functionality."""
    calc = Calculations()
    # Initially, history should be empty
    assert calc.get_history() == [], "History should start empty"
    # Add entries to history
    calc.add_history("first")
    calc.add_history("second")
    assert calc.get_history() == ["first", "second"], "History entries not recorded correctly"
    # Clear the history and verify
    calc.clear_history()
    assert calc.get_history() == [], "History was not cleared properly"

def test_reset_instance_allows_new():
    """_reset_instance should allow creating a new Calculations instance."""
    calc1 = Calculations()
    id1 = id(calc1)
    # Reset the singleton and create a new instance
    Calculations._reset_instance()
    calc2 = Calculations()
    id2 = id(calc2)
    assert id1 != id2, "Resetting the singleton should yield a new instance"

def test_history_interface_methods():
    """Test that Calculations implements HistoryInterface methods correctly."""
    calc = Calculations()
    # Initially, history is empty
    assert calc.count() == 0
    assert calc.get_last() is None
    assert calc.get_all() == []
    # Add an entry using the interface 'add' method
    result = calc.add("1+1", "2")
    assert result is True  # add returns True on success
    # Now history should have one record
    assert calc.count() == 1
    assert calc.get_last() == ("1+1", "2")
    assert calc.get_all() == [("1+1", "2")]
    # Search for existing and non-existing keywords in history
    assert calc.search("1+1") == [("1+1", "2")]
    assert calc.search("2") == [("1+1", "2")]    # keyword matches the result
    assert calc.search("3") == []               # no matching entry
    # Remove the last entry and verify history is empty
    removed = calc.remove_last()
    assert removed == ("1+1", "2")
    assert calc.count() == 0
    assert calc.get_last() is None
    assert calc.get_all() == []
    # Add a couple of entries and test clear()
    calc.add_history("temp1")
    calc.add_history("temp2")
    assert calc.count() == 2
    assert calc.clear() is True
    assert calc.count() == 0
