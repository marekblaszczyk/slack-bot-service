
class PluginMount(type):

    def __init__(cls, name, bases, attrs):
        super(PluginMount, cls).__init__(name, bases, attrs)
        cls.test = 1

        if not hasattr(cls, 'plugins'):
            cls.plugins = []
        else:
            cls.plugins.append(cls)

    def get_plugins(cls, *args, **kwargs):
        return [p(*args, **kwargs) for p in cls.plugins]


class PluginProvider(metaclass=PluginMount):
    pass


