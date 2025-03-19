import os, sys, importlib, pkgutil
import app.plugins  # Ensure app.plugins is importable
import pytest
from app.plugins import load_plugins, register_plugin_commands, PLUGIN_COMMANDS

@pytest.fixture(autouse=True)
def plugin_env(tmp_path):
    """Setup a temporary app/plugins package for testing plugin loading."""
    app_dir = tmp_path / "app"
    plugins_dir = app_dir / "plugins"
    plugins_dir.mkdir(parents=True)

    # Create __init__.py files for package recognition
    (app_dir / "__init__.py").write_text("")
    (plugins_dir / "__init__.py").write_text("")

    # Add to sys.path so 'app' package is discoverable
    sys.path.insert(0, str(tmp_path))

    yield plugins_dir  # Provide plugins directory path

    # Teardown: remove temp path and clean imported modules
    sys.path.remove(str(tmp_path))
    for mod in list(sys.modules):
        if mod == "app" or mod.startswith("app."):
            sys.modules.pop(mod, None)

def test_no_plugins(plugin_env, monkeypatch):
    """No plugin files in app/plugins should result in no modules loaded or commands registered."""

    # ✅ Override app.plugins.__path__ to only look in the test's plugin_env directory
    monkeypatch.setattr(app.plugins, "__path__", [str(plugin_env)])

    modules = load_plugins()
    assert modules == []  # No plugins found

    register_plugin_commands()
    assert PLUGIN_COMMANDS == {}  # No commands should be registered

def test_valid_plugin(plugin_env):
    """A well-formed plugin with a commands dict should be discovered and its command registered."""
    plugin_code = '''
executed = False
def sample():
    global executed
    executed = True
    return "ok"
commands = {"sample": sample}
'''
    (plugin_env / "plugin1.py").write_text(plugin_code)

    modules = load_plugins()
    assert len(modules) == 1
    assert modules[0].__name__ == "app.plugins.plugin1"

    register_plugin_commands()
    assert "sample" in PLUGIN_COMMANDS
    assert PLUGIN_COMMANDS["sample"]() == "ok"
    assert modules[0].executed is True

def test_plugin_missing_commands(plugin_env):
    """A plugin that does not define a commands attribute should load but not register commands."""
    (plugin_env / "plugin_no_cmd.py").write_text("def hello(): return 'hello'")

    modules = load_plugins()
    assert len(modules) == 1
    assert modules[0].__name__ == "app.plugins.plugin_no_cmd"

    register_plugin_commands()
    assert PLUGIN_COMMANDS == {}  # No commands registered

def test_multiple_plugins(plugin_env):
    """Multiple plugins should be discovered and their commands registered."""
    code1 = '''
executed = False
def foo():
    global executed
    executed = True
    return "foo"
commands = {"foo": foo}
'''
    code2 = '''
executed = False
def bar():
    global executed
    executed = True
    return "bar"
commands = {"bar": bar}
'''
    (plugin_env / "plugin_alpha.py").write_text(code1)
    (plugin_env / "plugin_beta.py").write_text(code2)

    modules = load_plugins()
    assert len(modules) == 2
    module_names = {m.__name__ for m in modules}
    assert "app.plugins.plugin_alpha" in module_names
    assert "app.plugins.plugin_beta" in module_names

    register_plugin_commands()
    assert "foo" in PLUGIN_COMMANDS
    assert "bar" in PLUGIN_COMMANDS
    assert PLUGIN_COMMANDS["foo"]() == "foo"
    assert PLUGIN_COMMANDS["bar"]() == "bar"

def test_import_error_plugin(plugin_env):
    """A plugin that fails on import should be skipped."""
    bad_code = 'raise ImportError("fail to import")'
    good_code = '''
executed = False
def do():
    global executed
    executed = True
    return "done"
commands = {"do": do}
'''
    (plugin_env / "bad_plugin.py").write_text(bad_code)
    (plugin_env / "good_plugin.py").write_text(good_code)

    modules = load_plugins()
    assert len(modules) == 1
    assert modules[0].__name__ == "app.plugins.good_plugin"

    register_plugin_commands()
    assert "do" in PLUGIN_COMMANDS
    assert PLUGIN_COMMANDS["do"]() == "done"
