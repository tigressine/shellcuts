from utilities import constants

def throw_error(error):
    """Echo an error message.
    
    Includes a master dictionary of all supported errors. These are accessible
    by key.
    """
    command = 'printf "ERROR {0}: {1}\n"'.format(error, constants.ERRORS[error])
    print(command)
    exit(0)


def throw_help():
    """"""
    script = (
        'Shellcuts usage: \$ sc [--flag] <shellcut>',
        '----------------------------------------------------------------',
        'Create a new shellcut for the current directory (named example):',
        '    \$ sc -n example',
        '',
        'Jump to that location from anywhere else on the system:',
        '    \$ sc example',
        '',
        'Remove that shellcut:',
        '    \$ sc -d example',
        '',
        'List all available shellcuts:',
        '    \$ sc -l',
        '',
        'See the manpage for lots more information and examples:',
        '    \$ man shellcuts')
    command = 'printf "'
    
    for line in script:
        command += line + '\n'
    print(command + '"')
    exit(0)
