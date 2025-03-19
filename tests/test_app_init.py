import sys
import builtins
import pytest
import app

@pytest.fixture
def monkeypatch_input(monkeypatch):
    """Helper function to mock user input."""
    def _patch(inputs):
        iter_inputs = iter(inputs)

        def mock_input(prompt=None):
            try:
                return next(iter_inputs)
            except StopIteration:
                return "\n"  # Ensure input() doesn't hang

        monkeypatch.setattr(builtins, "input", mock_input)

    return _patch

def test_start_add_no_name_provided(monkeypatch, capsys, monkeypatch_input):
    """Test handling of missing name input without hanging."""
    monkeypatch.setattr(sys, "argv", ["app"])
    monkeypatch_input(["add", ""])  # Simulate 'add' command, then empty input

    try:
        app.start()
    except StopIteration:
        pass  # Prevent pytest from hanging

    captured = capsys.readouterr()
    assert "Enter your name:" in captured.out
