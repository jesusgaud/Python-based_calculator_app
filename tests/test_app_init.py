import builtins
import logging
import sys
import pytest
import app

def test_configure_logging(monkeypatch):
    # Ensure idempotent logging configuration: fileConfig should be called only once
    calls = []
    def fake_fileConfig(cfg_path):
        calls.append(cfg_path)
    monkeypatch.setattr(logging.config, "fileConfig", fake_fileConfig)
    app._logging_configured = False
    app.configure_logging("dummy.conf")
    # Second call (with logging already configured) should not call fileConfig again
    app.configure_logging("dummy.conf")
    assert calls == ["dummy.conf"]
    # Simulate fileConfig failure to test fallback to basicConfig
    app._logging_configured = False
    monkeypatch.setattr(logging.config, "fileConfig", lambda cfg: (_ for _ in ()).throw(Exception("fail")))
    basic_called = []
    monkeypatch.setattr(logging, "basicConfig", lambda **kwargs: basic_called.append(True))
    error_msgs = []
    monkeypatch.setattr(logging, "error", lambda msg, *args: error_msgs.append(msg % args))
    app.configure_logging("missing.conf")
    # basicConfig should have been called once, and an error message logged
    assert basic_called == [True]
    assert any("Failed to load logging config from missing.conf" in m for m in error_msgs)
    # _logging_configured should be set to True after fallback
    assert app._logging_configured is True

def test_start_exit(monkeypatch):
    # Simulate interactive mode with 'exit' command
    monkeypatch.setattr(sys, "argv", ["app"])
    monkeypatch.setattr(builtins, "input", lambda prompt=None: "exit")
    with pytest.raises(SystemExit) as exc:
        app.start()
    assert exc.value.code == 0
    # Also test 'quit' as an alias for 'exit'
    monkeypatch.setattr(builtins, "input", lambda prompt=None: "quit")
    with pytest.raises(SystemExit) as exc2:
        app.start()
    assert exc2.value.code == 0

def test_start(monkeypatch):
    # Ensure configure_logging is called, and an interactive loop iteration runs then exits
    configured_flag = {"called": False}
    monkeypatch.setattr(app, "configure_logging", lambda: configured_flag.update(called=True) or None)
    monkeypatch.setattr(sys, "argv", ["app"])
    # Simulate a blank input (just Enter) followed by 'exit'
    inputs_iter = iter(["", "exit"])
    monkeypatch.setattr(builtins, "input", lambda prompt=None: next(inputs_iter))
    with pytest.raises(SystemExit) as exc:
        app.start()
    assert exc.value.code == 0
    # configure_logging was called once at start
    assert configured_flag["called"] is True

def test_start_unknown_command(monkeypatch, capsys):
    # Unknown command in CLI mode should exit with code 1 and message
    monkeypatch.setattr(sys, "argv", ["app", "unknowncmd"])
    with pytest.raises(SystemExit) as exc:
        app.start()
    assert exc.value.code == 1
    output = capsys.readouterr().out
    assert "Unknown command: unknowncmd" in output

    # Unknown command in interactive mode should not exit immediately
    monkeypatch.setattr(sys, "argv", ["app"])
    inputs = iter(["foobar", "exit"])  # 'foobar' is unknown, then exit
    monkeypatch.setattr(builtins, "input", lambda prompt=None: next(inputs))
    with pytest.raises(SystemExit) as exc2:
        app.start()
    assert exc2.value.code == 0
    output2 = capsys.readouterr().out
    # It should report the unknown command and then allow exit
    assert "Unknown command: foobar" in output2

def test_start_add_command(monkeypatch, capsys):
    # Interactive 'add' command without name on the same line (should prompt for name)
    monkeypatch.setattr(sys, "argv", ["app"])
    inputs1 = iter(["add", "TestItem", "exit"])
    monkeypatch.setattr(builtins, "input", lambda prompt=None: next(inputs1))
    with pytest.raises(SystemExit) as exc:
        app.start()
    assert exc.value.code == 0
    out = capsys.readouterr().out
    assert "Added TestItem" in out

    # Interactive 'add' command with name on the same line
    inputs2 = iter(["add AnotherItem", "exit"])
    monkeypatch.setattr(builtins, "input", lambda prompt=None: next(inputs2))
    with pytest.raises(SystemExit) as exc2:
        app.start()
    assert exc2.value.code == 0
    out2 = capsys.readouterr().out
    assert "Added AnotherItem" in out2

    # CLI 'add' command with a name argument
    monkeypatch.setattr(sys, "argv", ["app", "add", "CLIItem"])
    with pytest.raises(SystemExit) as exc3:
        app.start()
    assert exc3.value.code == 0
    out3 = capsys.readouterr().out
    assert "Added CLIItem" in out3

    # CLI 'add' command without providing a name (error case)
    monkeypatch.setattr(sys, "argv", ["app", "add"])
    with pytest.raises(SystemExit) as exc4:
        app.start()
    assert exc4.value.code == 1
    out4 = capsys.readouterr().out
    assert "requires a name" in out4

def test_start_add_empty_name(monkeypatch, capsys):
    # User enters 'add' then provides an empty name (just Enter)
    monkeypatch.setattr(sys, "argv", ["app"])
    inputs = iter(["add", "", "exit"])
    monkeypatch.setattr(builtins, "input", lambda prompt=None: next(inputs))
    with pytest.raises(SystemExit) as exc:
        app.start()
    assert exc.value.code == 0
    out = capsys.readouterr().out
    # Expect an error about empty name and no successful "Added ..." message
    assert "name cannot be empty" in out
    assert "Added" not in out

def test_start_add_no_name_provided(monkeypatch, capsys):
    # User enters 'add' and then does not provide any name (simulates EOF or no further input)
    monkeypatch.setattr(sys, "argv", ["app"])
    inputs = iter(["add"])  # no second input for name
    monkeypatch.setattr(builtins, "input", lambda prompt=None: next(inputs))
    # start() should handle the missing name and break out without exception
    app.start()
    out = capsys.readouterr().out
    assert "no name provided for 'add'" in out
    assert "Added" not in out

def test_start_unknown_command_exitcall(monkeypatch, capsys):
    # Monkeypatch sys.exit to capture calls for an unknown CLI command (no interactive loop after)
    calls = []
    monkeypatch.setattr(sys, "exit", lambda code=0: calls.append(code))
    monkeypatch.setattr(sys, "argv", ["app", "badcmd"])
    app.start()  # with sys.exit patched, this will return instead of raising
    # Verify a single exit call with code 1 (unknown command)
    assert calls == [1]
    out = capsys.readouterr().out
    assert "Unknown command: badcmd" in out

def test_start_help(monkeypatch, capsys):
    # The help flag (-h/--help) should display usage and exit with code 0
    monkeypatch.setattr(sys, "argv", ["app", "--help"])
    with pytest.raises(SystemExit) as exc:
        app.start()
    assert exc.value.code == 0
    out = capsys.readouterr().out
    assert "Usage:" in out and "Commands:" in out
