from resp.client import Client

client = Client()
client.connect()
client.send_command("PING")
client.Hashes.hset("myhash", ("field1", "value1"), ("field2", "value2"))
print(client.Hashes.hget_all("myhash"))
client.Hashes.hdel("myhash", "field1")
print(client.Hashes.hscan_all("myhash"))




