from werkzeug.routing import BaseConverter


class NotReserved(BaseConverter):
    regex = "(?!static|api|confirm).*"
