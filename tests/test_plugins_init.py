import pytest
from app.plugins import load_plugins

@pytest.fixture
def plugin_env(tmp_path, monkeypatch):
    """Creates a temporary plugin environment for testing."""
    plugins_dir = tmp_path / "app" / "plugins"
    plugins_dir.mkdir(parents=True, exist_ok=True)
    monkeypatch.setattr("app.plugins.PLUGIN_DIR", plugins_dir)
    return plugins_dir

def test_valid_plugin(plugin_env):
    """Test that a well-formed plugin loads successfully."""
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
    assert len(modules) == 1, f"Expected 1 plugin, got {len(modules)}"

def test_plugin_missing_commands(plugin_env):
    """Ensure plugins without a 'commands' dict do not break loading."""
    (plugin_env / "plugin_no_cmd.py").write_text("def hello(): return 'hello'")

    modules = load_plugins()
    assert len(modules) == 0, f"Expected no plugins to load, got {len(modules)}"

def test_multiple_plugins(plugin_env):
    """Ensure multiple plugins load correctly."""
    code1 = '''
def foo():
    return "foo"
commands = {"foo": foo}
'''
    code2 = '''
def bar():
    return "bar"
commands = {"bar": bar}
'''
    (plugin_env / "plugin_alpha.py").write_text(code1)
    (plugin_env / "plugin_beta.py").write_text(code2)

    modules = load_plugins()
    assert len(modules) == 2, f"Expected 2 plugins, got {len(modules)}"

def test_import_error_plugin(plugin_env):
    """Ensure plugins that fail to import do not break loading."""
    bad_code = 'raise ImportError("fail to import")'
    good_code = '''
def do():
    return "done"
commands = {"do": do}
'''
    (plugin_env / "bad_plugin.py").write_text(bad_code)
    (plugin_env / "good_plugin.py").write_text(good_code)

    modules = load_plugins()
    assert len(modules) == 1, f"Expected 1 valid plugin, got {len(modules)}"
