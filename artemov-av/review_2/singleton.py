class Singleton(type):
    instance = None

    def __call__(cls):
        if cls.instance is None:
            cls.instance = super(Singleton, cls).__call__()
        return cls.instance
