from flask import Flask, request
from secrets import TARGET_CHAT_ID
from datetime import datetime, timedelta, timezone
import json

app = Flask(__name__)


@app.route('/bot', methods=['GET', 'POST'])
def get_update():
    # print(request)
    js = request.json
    if js:
        print(json.dumps(js, ensure_ascii=False, indent=2))
    return {"ok": True}


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')