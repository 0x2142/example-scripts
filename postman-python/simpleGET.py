import requests
import json

URL = "https://jsonplaceholder.typicode.com/users"

print("Search by Username:")
user = input("> ")
queryURL = URL + f"?username={user}"
response = requests.get(queryURL)

userdata = json.loads(response.text)[0]

name = userdata["name"]
email = userdata["email"]
phone = userdata["phone"]

print(f"{name} can be reached via the following methods:")
print(f"Email: {email}")
print(f"Phone: {phone}")
