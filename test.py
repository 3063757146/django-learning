from flask import Flask,render_template
app=Flask(__name__)

@app.route("/users/list")  #route注入
def list():
    return render_template("users_list.html")
app.run()