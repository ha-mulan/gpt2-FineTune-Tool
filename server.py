
from flask import Flask, request, Response, jsonify
from flask import Flask, render_template, request, Response, send_file, jsonify

from queue import Queue, Empty
import time
import threading
from text_preprocess import normalize

# Server & Handling Setting
app = Flask(__name__)

requests_queue = Queue()
BATCH_SIZE = 1
CHECK_INTERVAL = 0.1


# Queue 핸들링
def handle_requests_by_batch():
    while True:
        requests_batch = []
        while not (len(requests_batch) >= BATCH_SIZE):
            try:
                requests_batch.append(requests_queue.get(timeout=CHECK_INTERVAL))
            except Empty:
                continue

            for requests in requests_batch:
                requests['output'] = run_model(requests['input'])

threading.Thread(target=handle_requests_by_batch).start()

def run_model(prompt, num=1, length=30):
    try:
        result=''
        for i in prompt:
            result+=i
        return normalize(result)

    except Exception as e:
        print(e)
        return 500

@app.route("/api/", methods=['GET'])
def generate():

    if requests_queue.qsize() > BATCH_SIZE:
        return jsonify({'error': 'Too Many Requests'}), 429

    try:
        args = []

        text=request.args.get('text')

        args.append(text)

    except Exception:
        print("Empty Text")
        return Response("fail", status=400)

    req = {
        'input': args
    }
    requests_queue.put(req)

    while 'output' not in req:
        time.sleep(CHECK_INTERVAL)

    return req['output']


# Health Check

@app.route('/healthz')
def health():
    return "ok", 200

@app.route('/')
def main():
    return render_template('index.html')

if __name__ == "__main__":
    from waitress import serve
    serve(app, host='0.0.0.0', port=80)

