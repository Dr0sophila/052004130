from flask import Flask, render_template
app = Flask(__name__, static_folder="templates")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/confirm_page.html")
def confirm_page():
    return render_template("confirm_page.html")


@app.route("/Asymptomatic_page.html")
def asymptomatic_page():
    return render_template("asymptomatic_page.html")


@app.route("/confirm.png",methods = ['POST','GET'])
def p1():
    return render_template("confirm.png", mimetype='image/gif')


@app.route("/asymptomatic.png",methods = ['POST','GET'])
def p2():
    return render_template("asymptomatic.png", mimetype='image/gif')


if __name__ == "__main__":
    app.run()
