
from resp.client import Client

client = Client()
client.connect()
client.send_command("PING")
client.send_command("SCAN" ,"0")
