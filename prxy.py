from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/proxy', methods=['GET', 'POST'])
def proxy():
    url = 'https://shellshock.io/' + request.full_path
    headers = {'User-Agent': request.headers.get('User-Agent')}
    response = requests.request(method=request.method, url=url, headers=headers, data=request.get_data(), cookies=request.cookies, allow_redirects=False)
    return (response.content, response.status_code, response.headers.items())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
