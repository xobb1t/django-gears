from .processors import DirectivesProcessor


class Finders(list):

    def register(self, finder):
        if finder not in self:
            self.append(finder)

    def unregister(self, finder):
        if finder in self:
            self.remove(finder)


class MIMETypes(dict):

    def register_defaults(self):
        self.register('.css', 'text/css')
        self.register('.js', 'application/javascript')

    def register(self, extension, mimetype):
        self[extension] = mimetype

    def unregister(self, extension):
        if extension in self:
            del self[extension]


class Processors(dict):

    def register_defaults(self):
        self.register('text/css', DirectivesProcessor)
        self.register('application/javascript', DirectivesProcessor)

    def register(self, mimetype, processor_class):
        self.setdefault(mimetype, []).append(processor_class)

    def unregister(self, mimetype, processor_class):
        if mimetype in self and processor_class in self[mimetype]:
            self[mimetype].remove(processor_class)

    def get(self, mimetype):
        return super(Processors, self).get(mimetype, [])


class PublicAssets(list):

    def register_defaults(self):
        self.register('css/style.css')
        self.register('js/script.js')

    def register(self, path):
        if path not in self:
            self.append(path)

    def unregister(self, path):
        if path in self:
            self.remove(path)


class Environment(object):

    def __init__(self, root):
        self.root = root
        self.finders = Finders()
        self.mimetypes = MIMETypes()
        self.processors = Processors()
        self.public_assets = PublicAssets()

    def register_defaults(self):
        self.mimetypes.register_defaults()
        self.processors.register_defaults()
        self.public_assets.register_defaults()

    def find(self, path, all=False):
        matches = []
        for finder in self.finders:
            result = finder.find(path, all=all)
            if not all and result:
                return result
            if not isinstance(result, (list, tuple)):
                result = []
            matches.extend(result)
        if matches:
            return matches
        return [] if all else None