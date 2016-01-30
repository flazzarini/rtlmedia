from spider import Spider


class Manager(object):
    def __init__(self, spider=Spider()):
        self.spider = spider

    def get_items(self, query="Journal"):
        result = {
            'items': []}

        for item in self.spider.get_items(query=query):
            result['items'].append(item.as_dict())

        return result
