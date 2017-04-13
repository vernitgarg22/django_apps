import cod_utils.util

# monkey-patch our twilio validator so that it
# doesn't kill our tests
class TestMsgValidator():
    def validate(self, request):
        pass

cod_utils.util.MsgValidator = TestMsgValidator
