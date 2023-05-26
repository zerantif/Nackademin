from server import Server
import pytest

class FakeServerSocketStoreMessage():
    def __init__(self, client_name, sockname=("127.0.0.1",123)):
        self.client_name = client_name
        self.sockname = sockname
        self.last_message = None
        pass

    def send(self, message):
        self.last_message = message

def test_client_command_users():
    s = Server("localghost", "1234")
    ss = FakeServerSocketStoreMessage("kalle")
    ss2 = FakeServerSocketStoreMessage("nils")
    s.add_connection(ss)
    s.add_connection(ss2)

    s.handle_client_command(ss, "users")
    assert \
        "List of connected users" in ss.last_message \
        and "kalle" in ss.last_message \
        and "nils" in ss.last_message
    
    s.remove_connection(ss) # Remove kalle

    s.handle_client_command(ss2, "users") # Kalle must not show up in list of users
    assert \
        "List of connected users" in ss2.last_message \
        and "nils" in ss2.last_message \
        and not "kalle" in ss2.last_message

def test_client_command_sendpm():
    s = Server("localghost", "1234")
    ss = FakeServerSocketStoreMessage("kalle")
    s.add_connection(ss)

    s.handle_client_command(ss, "sendpm kalle snigel")
    assert ss.last_message == "Private message from kalle: snigel"

    s.handle_client_command(ss, "sendpm nils snigel")
    assert ss.last_message == "No such user!"

def test_client_command_sendimg():
    s = Server("localghost", "1234")
    ss = FakeServerSocketStoreMessage("kalle")
    s.add_connection(ss)

    s.handle_client_command(ss, "sendimg devops.png") # Test start sending to all
    assert ss.last_message == "!imgstart kalle devops.png"

    s.handle_client_command(ss, "imgdata firstbytes") # Test sending image data to all
    assert ss.last_message == "!imgdata kalle firstbytes"

    s.handle_client_command(ss, "imgdata kalle firstbytes") # Test sending image data to specific recipient
    assert ss.last_message == "!imgdata kalle firstbytes"

    s.handle_client_command(ss, "imgend") # Test image-end condition to all.
    assert ss.last_message == "!imgend kalle "

def test_client_command_broadcast():
    s = Server("localghost", "1234")
    ss_kalle = FakeServerSocketStoreMessage("kalle", ("127.0.0.1", 123)) # Two clients
    ss_nils = FakeServerSocketStoreMessage("nils", ("127.0.0.1", 124))
    s.add_connection(ss_kalle)
    s.add_connection(ss_nils)
    s.broadcast(ss_kalle.client_name, "sniglar", ss_kalle.sockname) # Broadcast from "kalle" should only be visible to nils

    assert ss_kalle.last_message == None
    assert ss_nils.last_message == 'kalle: sniglar'

def test_distribute_command():
    s = Server("localghost", "1234")
    ss = FakeServerSocketStoreMessage("recipient")
    ss2 = FakeServerSocketStoreMessage("recipient2")
    s.add_connection(ss)
    s.add_connection(ss2)
    s._distribute_command("sender", "recipient", "!command", "this-is-data") # Distributing command to specific to specific user

    assert ss.last_message == '!command sender this-is-data'
    assert ss2.last_message == None

    s._distribute_command("sender", None, "!command", "this-is-broadcast") # Distributing command to all users.

    assert ss.last_message == '!command sender this-is-broadcast'
    assert ss2.last_message == '!command sender this-is-broadcast'

def test_remove_connection():
    s = Server("localghost", "1234")
    ss = FakeServerSocketStoreMessage("client")
    ss2 = FakeServerSocketStoreMessage("client2")

    s.add_connection(ss)
    s.add_connection(ss2)

    s.remove_connection(ss)
    s._distribute_command("sender", None, "!command", "this-should-reach-ss2") # Now only "ss2" should get the command
    
    assert ss2.last_message == "!command sender this-should-reach-ss2"
    assert ss.last_message == None

    ss3 = FakeServerSocketStoreMessage("client3") # Attempting to remove a connection that doesn't exist
    with pytest.raises(ValueError, match=r'x not in list'): # should fail.
        s.remove_connection(ss3)

