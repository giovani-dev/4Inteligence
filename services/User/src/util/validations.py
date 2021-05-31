



class Validate(object):

    @staticmethod
    def conditional(exp: bool, action: object, _raise: bool) -> None:
        if exp and _raise:
            raise action
        elif exp and not _raise:
            return action
