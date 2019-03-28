from django.conf import settings


def block_client(request):
    """
    Returns False if caller is in white list of accepted clients.
    """

    # REVIEW Disable this because the addresses of all incoming requests
    # are NAT-ed to the address of the firewall.

    return False

    REMOTE_ADDR = request.META.get('REMOTE_ADDR')
    REMOTE_HOST = request.META.get('REMOTE_HOST')

    client_ok = REMOTE_ADDR in settings.ALLOWED_HOSTS or REMOTE_HOST in settings.ALLOWED_HOSTS
    return not client_ok
