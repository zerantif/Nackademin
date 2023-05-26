import pytest
import base64
from client import Send, Receive

class FakeSocket():
    def __init__(self):
        self.last_messages = []

    def sendall(self, message):
        self.last_messages.append(message)

    def get_all_messages(self):
        lm = self.last_messages
        self.last_messages = []
        return lm

def test_send_quit():
    fs = FakeSocket()
    s = Send(fs, "zeran")
    s.send_to_server("!quit")   # !quit should send "...has left the chat" message to server.

    assert "has left the chat." in fs.get_all_messages()[1].decode()

def test_send_sendimg():
    fs = FakeSocket()
    s = Send(fs, "zeran")
    s.send_to_server("!sendimg devops.png")
    msgs_sent = fs.get_all_messages()

    assert len(msgs_sent) > 4   # Ensure we have at least one !imgdata
    assert "!sendimg devops.png" == msgs_sent[1].decode()

    for i in range(3, len(msgs_sent)-2, 2):
        assert "!imgdata" in msgs_sent[i].decode()

    assert "!imgend" in msgs_sent[len(msgs_sent)-1].decode()

def test_send_img_missing_file(capsys):
    fs = FakeSocket()
    s = Send(fs, "zeran")
    s.send_to_server("!sendimg missingfile.png zeran")
    captured = capsys.readouterr()

    assert "doesn't exist" in captured.out

def test_send_imguser():
    fs = FakeSocket()
    s = Send(fs, "zeran")
    s.send_to_server("!sendimg devops.png zeran")
    msgs_sent = fs.get_all_messages()

    assert len(msgs_sent) > 4   # Ensure we have at least one !imgdata
    assert "!sendimg devops.png zeran" == msgs_sent[1].decode()

    for i in range(3, len(msgs_sent)-2, 2):
        assert "!imgdata" in msgs_sent[i].decode()

    assert "!imgend" in msgs_sent[len(msgs_sent)-1].decode()

def test_say_send():
    fs = FakeSocket()
    s = Send(fs, "zeran")
    s.send_to_server("hej server")

    assert fs.get_all_messages()[1].decode() == "hej server"

def test_recv_imgstart():    # Test how the client reacts when the server sends a !imgstart command to the client
    r = Receive(None, "zeran")
    r.recv_from_server("!imgstart bert foobar.png")

    assert r.images_in_flight['bert']['filename'] == 'foobar.png'
    assert r.images_in_flight['bert']['data'] == b''

def test_recv_imgdata():     # Verify that the client handles !imgdata properly
    r = Receive(None, "zeran")
    r.recv_from_server("!imgstart bert foobar.png")
    r.recv_from_server(f"!imgdata bert " + base64.b64encode(b'foo').decode())
    r.recv_from_server(f"!imgdata bert " + base64.b64encode(b'bar').decode())

    assert r.images_in_flight['bert']['data'] == 'foobar'.encode()
