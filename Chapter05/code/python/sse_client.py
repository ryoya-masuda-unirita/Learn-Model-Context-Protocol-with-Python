import requests

def consume_sse():
    response = requests.get('http://localhost:8000/sse', stream=True)
    for line in response.iter_lines():
        if line:
            print('SSE を受信:', line.decode('utf-8'))
consume_sse()
