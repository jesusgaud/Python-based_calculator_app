import sys
import logging
import logging.config

_logging_configured = False

def configure_logging(config_path="logging.conf"):
    """
    Set up logging configuration from the given file. If the configuration has already been loaded,
    subsequent calls have no effect to prevent duplicate configurations.
    If the config file cannot be loaded, falls back to basicConfig with INFO level and logs an error.
    """
    global _logging_configured
    if _logging_configured:
        # Logging is already configured; skip reconfiguration
        return
    try:
        logging.config.fileConfig(config_path)
        _logging_configured = True
    except Exception as e:
        # Fallback to basic configuration if fileConfig fails (e.g., missing or invalid file)
        logging.basicConfig(level=logging.INFO)
        logging.error("Failed to load logging config from %s: %s", config_path, e)
        _logging_configured = True  # Prevent repeated attempts in the future

def start(commands=None):
    """
    Start the application by configuring logging and then entering the main command loop or processing CLI arguments.
    If `commands` is provided (a list of inputs), the function will simulate interactive input using that list.
    This is used for testing to automate inputs and exits.
    """
    configure_logging()
    args = sys.argv[1:]
    # Handle command-line arguments (non-interactive mode)
    if args:
        cmd = args[0]
        if cmd in ("-h", "--help"):
            # Display usage/help message
            print("Usage: app [command] [<args>]\nCommands:\n  add <name>  Add an item with the given name\n  exit        Exit the application")
            sys.exit(0)
        if cmd == "add":
            if len(args) < 2:
                print("Error: 'add' command requires a name argument")
                sys.exit(1)
            name = " ".join(args[1:]).strip()
            if not name:
                print("Error: 'add' command requires a non-empty name")
                sys.exit(1)
            # Execute the add command (e.g., add the item – here we just acknowledge it)
            print(f"Added {name}")
            sys.exit(0)
        else:
            # Unknown command provided as an argument
            print(f"Unknown command: {cmd}")
            sys.exit(1)
        return  # Ensure we don't enter interactive mode after handling a CLI command

    # Interactive mode: loop reading commands from input (or from the provided list in tests)
    input_iter = iter(commands) if commands is not None else None
    while True:
        try:
            cmd = next(input_iter) if input_iter is not None else input(">>> ")
        except StopIteration:
            # No more test commands; end the interactive session
            break
        except EOFError:
            # End-of-file (Ctrl+D) ends the session gracefully
            print("")  # Move to a new line before exiting
            break

        # Normalize and handle the command
        if cmd is None:
            continue  # Skip if somehow None is fetched (should not happen in normal usage)
        cmd = str(cmd).strip()
        if cmd == "":
            # Ignore empty input (just an Enter with no command)
            continue
        if cmd in ("exit", "quit"):
            sys.exit(0)
        elif cmd.startswith("add"):
            # Handle 'add' command in interactive mode
            parts = cmd.split(maxsplit=1)
            if len(parts) < 2 or parts[1] == "":
                # No name provided on the same line; prompt (or get next test input)
                try:
                    name = next(input_iter) if input_iter is not None else input("Enter name: ")
                except StopIteration:
                    print("Error: no name provided for 'add'")
                    break
                except EOFError:
                    print("\nError: no name provided for 'add'")
                    break
                name = str(name).strip()
                if not name:
                    print("Error: name cannot be empty")
                    continue  # Loop back to prompt again for a name or new command
            else:
                # Name is provided in the same command after 'add'
                name = parts[1].strip()
                if not name:
                    print("Error: name cannot be empty")
                    continue
            # Execute the add command (here we simply print confirmation)
            print(f"Added {name}")
        else:
            # Unknown command in interactive mode – notify and continue
            print(f"Unknown command: {cmd}")
            continue

if __name__ == "__main__":
    start()  # pragma: no cover
