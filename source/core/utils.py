from .constants import ERRORS, VERSION_FILE
def error_message(error):
    """Echo an error message.
    
    Includes a master dictionary of all supported errors. These are accessible
    by key.
    """
    command = 'printf "ERROR {0}: {1}\n"'.format(error, ERRORS[error])
    
    print(command)
    #exit(0)

def load_version_info():
    """Load version information found at VERSION_FILE."""
    try:
        with open(str(VERSION_FILE), 'r') as f:
            return f.readlines()
    except FileNotFoundError:
        return None
        #error_message("NoVersion")
