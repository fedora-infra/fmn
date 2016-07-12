import getpass

config = {
    'fas_credentials': {
        'username': raw_input('FAS username: '),
        'password': getpass.getpass('FAS password: '),
    }
}
