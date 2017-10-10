import logging

from django.conf import settings


class CODLogger():
    """
    Handles logging information
    """

    # the one and only singlton instance
    __instance = None

    def __init__(self):
        # Make sure only 1 instance is created
        if self.__instance:
            raise Exception("call static instance() to get access to " + __class__.__name__)    # pragma: no cover (note: should never get called)
        self.loggers = {}

    @staticmethod
    def instance():
        """
        Should return one-and-only instance of this class.
        """
        if __class__.__instance is None:
            __class__.__instance = CODLogger()
        return __class__.__instance

    def get_logger(self, name):
        """
        Get an instance of a logger
        """

        if not self.loggers.get(name):
            self.loggers[name] = logging.getLogger(name)
        return self.loggers[name]

    def log_api_call(self, name, msg):
        """
        Log information about an api call
        """

        logger = self.get_logger(name)

        # TODO should configure log level better ...
        if not settings.RUNNING_UNITTESTS:
            logger.error("api call: " + msg)    # pragma: no cover

    def log_error(self, name, area, msg):
        """
        Log information about a runtime error.
        """

        logger = self.get_logger(name)

        # TODO should configure log level better ...
        if not settings.RUNNING_UNITTESTS:
            logger.error("ERROR in " + area + ": " + msg)    # pragma: no cover
