from flask import Flask, request, Response, stream_with_context
import requests
import asyncio
import websockets

app = Flask(__name__)

TARGET_URL = 'https://shellshock.io/'

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def proxy(path):
    if request.method in ['GET', 'POST', 'PUT', 'DELETE']:
        url = f"{TARGET_URL}{path}"
        headers = {key: value for key, value in request.headers if key != 'Host'}
        response = requests.request(
            method=request.method,
            url=url,
            headers=headers,
            data=request.get_data(),
            cookies=request.cookies,
            allow_redirects=False
        )

        excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
        headers = [(name, value) for name, value in response.raw.headers.items() if name.lower() not in excluded_headers]
        
        return Response(response.content, response.status_code, headers)

@app.route('/ws/<path:path>')
def ws_proxy(path):
    return Response(stream_with_context(forward_websocket(path)), content_type='text/event-stream')

async def forward_websocket(path):
    ws_url = f"wss://shellshock.io/{path}"
    async with websockets.connect(ws_url) as websocket:
        while True:
            message = await websocket.recv()
            yield message

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
