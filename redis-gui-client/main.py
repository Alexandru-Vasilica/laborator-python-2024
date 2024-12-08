

from resp.client import Client

client = Client()
client.connect()
print(client.ping())
