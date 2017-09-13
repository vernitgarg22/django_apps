from django.conf import settings


def block_client(request):
    """
    Returns False if caller is in white list of accepted clients.
    """

    REMOTE_ADDR = request.META.get('REMOTE_ADDR')
    REMOTE_HOST = request.META.get('REMOTE_HOST')

    client_ok = REMOTE_ADDR in settings.ALLOWED_HOSTS or REMOTE_HOST in settings.ALLOWED_HOSTS
    return not client_ok
