from flask import Flask, render_template, jsonify
import threading
import time

app = Flask(__name__)

# 全局变量来控制页面显示
page_selector = 0

def apprun():
    app.run(host="0.0.0.0",port=4000)

@app.route('/')
def index():
    #return 'Hello, this is a simple test!'
    return render_template('index.html')

@app.route('/get_page_selector')
def get_page_selector():
    return jsonify({'page_selector': page_selector})

def warn_start():
    threading.Thread(target=apprun, daemon=True).start()

def warn_change(input):
    global page_selector
    page_selector=input

if __name__ == "__main__" :
    warn_start()
    while True:
        warn_change(0)
        time.sleep(1)
        warn_change(1)
        time.sleep(1)
