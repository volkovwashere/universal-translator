import requests
import json

text = "hello there sir how are you"
target_lang = "DE"
api_key = "5fa7a2fe-6d96-6926-e15b-f829e2be23ae:fx"

payload = {
    "text": text,
    "target_lang": target_lang,
}
headers = {
    "Authorization": f"DeepL-Auth-Key {api_key}"
}
res = requests.post(
    url="https://api-free.deepl.com/v2/translate",
    data=payload,
    headers=headers,
)
print(res.status_code)
print(res.json())
