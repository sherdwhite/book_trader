# Settings module marker
# Import all settings from the main settings.py file
from pathlib import Path

# Get the parent directory where settings.py is located
current_dir = Path(__file__).parent
settings_py_path = current_dir.parent / "settings.py"

# Read and execute the settings.py file in this module's namespace
if settings_py_path.exists():
    with open(settings_py_path, "r", encoding="utf-8") as f:
        settings_code = f.read()

    # Execute the settings code in this module's globals
    exec(settings_code, globals())  # noqa: S102
else:
    raise ImportError(f"Could not find settings.py at {settings_py_path}")
