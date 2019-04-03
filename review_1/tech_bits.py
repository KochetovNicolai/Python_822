# auxiliary implementations


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


def type_validation(func, message=None, check=None):
    class Exc(Exception):
        pass

    while True:
        try:
            temp = func()
            if check is not None and not check(temp):
                raise Exc
            return temp
        except ValueError:
            if check is None and message is not None:
                print(message)
            else:
                print(f"Wrong type - try again")
        except Exc:
            print(message)
