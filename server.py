from flask import Flask, render_template, request, Response, send_file, jsonify
from text_preprocess import normalize


# Server & Handling Setting
app = Flask(__name__)


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

    try:
        text=request.args.get('text')
        result = run_model(text)
        return result
    except Exception:
        print("Empty Text")
        return Response("fail", status=400)

# Health Check

@app.route('/healthz')
def health():
    return "ok", 200

@app.route('/')
def main():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)

