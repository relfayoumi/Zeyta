# integrations/pc_control.py
# Placeholder for PC control functions.

import os

def open_application(app_name: str):
    """
    Opens an application on the PC.
    (Implementation is basic and OS-dependent)
    """
    print(f"Placeholder: Attempting to open '{app_name}'.")
    try:
        os.startfile(app_name) # For Windows
    except AttributeError:
        print("Note: 'os.startfile' is for Windows. Implement alternatives for other OS.")
    except Exception as e:
        print(f"Could not open {app_name}: {e}")

def shutdown_pc(force: bool = False):
    """
    Shuts down the PC.
    (Implementation not included for safety)
    """
    print(f"Placeholder: Would shut down PC now (Forced: {force}).")