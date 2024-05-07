import sys

def is_virtualenv_active():
    return hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)

if is_virtualenv_active():
    print("Virtual environment is active.")
else:
    print("Virtual environment is not active.")
