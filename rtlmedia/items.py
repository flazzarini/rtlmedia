class Page(object):
    def __init__(self, title, path, date):
        self.title = title
        self.path = path
        self.date = date

    def as_dict(self):
        result = {
            'title': self.title,
            'path': self.path,
            'date': self.date}
        return result


class Item(object):
    def __init__(self, title, url, date):
        self.title = title
        self.url = url
        self.date = date

    def as_dict(self):
        result = {
            'title': self.title,
            'url': self.url,
            'date': self.date}
        return result
