from cod_utils.messaging import MsgHandler


def no_validate(self, request):
    pass

MsgHandler.validate = no_validate
