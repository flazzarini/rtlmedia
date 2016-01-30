import logging
from bottle import route, response, run
from json import dumps

from manager import Manager
from exc import JournalException

manager = Manager()


def handle_error(exc):
    result = {
        'message': "Failed to get journals",
        'reason': str(exc),
    }
    response.content_type = "application/json"
    response.status = 409
    return dumps(result)


@route('/')
def index():
    try:
        results = manager.get_items()
        response.content_type = "application/json"
        return dumps(results)
    except JournalException as exc:
        handle_error(exc)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    run(host='localhost', port=8080, debug=True)
