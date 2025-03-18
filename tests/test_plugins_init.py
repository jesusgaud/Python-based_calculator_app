import pytest
import logging
import importlib
import pkgutil
from unittest.mock import patch, MagicMock
from app.plugins import load_plugins, register_plugin_commands
from app.commands import CommandHandler, Command

@pytest.fixture
def command_handler():
    """Fixture to create an instance of CommandHandler."""
    return CommandHandler()

@patch("app.plugins.pkgutil.iter_modules")
@patch("app.plugins.importlib.import_module")
@pytest.mark.skip_load_plugins  # This is now linked to pytest.ini
def test_load_plugins(mock_import_module, mock_iter_modules, command_handler):
    """Test dynamic plugin discovery and command registration with multiple plugins."""
    mock_iter_modules.return_value = [
        (None, "test_plugin1", False),
        (None, "test_plugin2", False),
        (None, "test_plugin3", False)
    ]

    mock_plugin1 = MagicMock()
    mock_plugin1.__name__ = "app.plugins.test_plugin1"

    mock_plugin2 = MagicMock()
    mock_plugin2.__name__ = "app.plugins.test_plugin2"

    mock_plugin3 = MagicMock()
    mock_plugin3.__name__ = "app.plugins.test_plugin3"

    mock_import_module.side_effect = [mock_plugin1, mock_plugin2, mock_plugin3]

    load_plugins(command_handler)

    assert mock_import_module.call_count == 3
    mock_import_module.assert_any_call("app.plugins.test_plugin1")
    mock_import_module.assert_any_call("app.plugins.test_plugin2")
    mock_import_module.assert_any_call("app.plugins.test_plugin3")

@patch("app.plugins.pkgutil.iter_modules")
@patch("app.plugins.importlib.import_module", side_effect=ImportError("Mock Import Error"))
@pytest.mark.skip_import_error  # Skipping known ImportError issue
def test_load_plugins_import_error(mock_import_module, mock_iter_modules, command_handler, caplog):
    """Test plugin loading when an ImportError occurs."""
    mock_iter_modules.return_value = [
        (None, "bad_plugin1", False),
        (None, "bad_plugin2", False)
    ]

    with caplog.at_level(logging.ERROR):
        load_plugins(command_handler)

    assert "Failed to load plugin bad_plugin1" in caplog.text
    assert "Failed to load plugin bad_plugin2" in caplog.text
    assert mock_import_module.call_count == 2
