from plugin import PluginProvider


class Joke(PluginProvider):
    title = 'Joke'

    def __init__(self):
        super(Joke, self).__init__()
