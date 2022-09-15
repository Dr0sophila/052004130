from flask import Flask

app = Flask(__name__)


@app.route('/')  # 装饰器
def hello_world():
    return "Hello World!"


@app.route('/abc')
def hello_world1():
    return """
    <form>
        账号:<input><br>
        密码:<input>
    </form>
    """


if __name__ == "__main__":
    app.run()