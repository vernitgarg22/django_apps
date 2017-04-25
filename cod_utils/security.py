

API_CLIENT_WHITELIST_SERVERS = [ "10.208.68.13", "10.208.37.49" ]
API_CLIENT_WHITELIST_DEVELOPERS = [ "127.0.0.1", "10.194.74.214" ]
API_CLIENT_WHITELIST = API_CLIENT_WHITELIST_SERVERS + API_CLIENT_WHITELIST_DEVELOPERS


def block_client(request):
    """
    Returns False if caller is in white list of accepted clients.
    """

    REMOTE_ADDR = request.META.get('REMOTE_ADDR')
    REMOTE_HOST = request.META.get('REMOTE_HOST')

    client_ok = REMOTE_ADDR in API_CLIENT_WHITELIST or REMOTE_HOST in API_CLIENT_WHITELIST
    return not client_ok
