"""This module implements the Singleton pattern."""


class SingletonMeta(type):
    """The Singleton class can be implemented in different ways in Python.

    Some possible methods include: base class, decorator, metaclass. We will use the metaclass because it is best suited
    for this purpose. To define a singleton class use this format:
    class SingletonClass(metaclass=SingletonMeta):
        pass
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonMeta, cls).__call__(*args, **kwargs)
            cls._instances[cls].__init__(*args, **kwargs)

        return cls._instances[cls]
