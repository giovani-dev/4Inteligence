from typing import NamedTuple, List


class ToValidateMethods(NamedTuple):
    methods: List[str] = [
        "GET",
        "POST",
        "PUT",
        "HEAD",
        "DELETE",
        "PATCH",
        "OPTIONS"
    ]

    @staticmethod
    def exclude(values: List[str], class_methods=methods) -> List[str]:
        assert isinstance(values, list)
        for value in values:
            for n in range(0, len(class_methods)-1):
                if value.upper() == class_methods[n]:
                    del(class_methods[n])
        return ToValidateMethods(methods=class_methods)