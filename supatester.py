import os;
import re;
import requests
import sys


print("TESTING _____ BEGIN READ FILE ______");
with open('tkl.txt', 'r', encoding='utf-8') as file:
    content = file.read()
    #content = content.match(/^.+$[\n\r]*/gm);
    response = requests.post("http://localhost:8000/process-text", json={"text": content, "table":"test_bin", "docid": "1x0002olklffdd"})
    
print(response.json())