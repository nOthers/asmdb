import sys
from .wsclient import WsController, WsError


def new_default_controller():
    return WsController('ws://127.0.0.1:8519/ws', sys.argv[1])
