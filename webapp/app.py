from flask import Flask, session, render_template, request

import os
import swimclub

app = Flask(__name__)
app.secret_key = "test_only"

def poupulate_data():
    if "swimmers" not in session:
            files = os.listdir(swimclub.FOLDER)
            files.remove(".DS_Store")
            session["swimmers"] = {}
            for file in files:
                name, *_ = swimclub.read_swim_data(file)
                if name not in session["swimmers"]:
                    session["swimmers"][name] = []
                session["swimmers"][name].append(file)


@app.get("/")
def index():
    return render_template("index.html",
                           title = "Welcome to the Swimclub")

@app.get("/swimmers")
def display_swimmers():
    poupulate_data()
    return render_template(
         "select.html",
         title = "Select a swimmer",
         url = "/showfiles",
         select_id = "swimmer",
         data = sorted(session["swimmers"])
    )

@app.post("/showfiles")
def display_swimmers_files():
     poupulate_data()
     name = request.form["swimmer"]
     return render_template(
          "select.html",
          title = "Select an event",
          url = "/showbarchart",
          select_id = "file",
          data = sorted(session["swimmers"][name]),
     )

@app.post("/showbarchart")
def show_bar_chart():
     file_id = request.form["file"]
     location = swimclub.produce_bar_chart(file_id, "templates/")
     return render_template(location.split("/")[-1])

@app.get("/files/<swimmer>")
def get_swimmer_files(swimmer):
    poupulate_data()
    return str(session["swimmers"][swimmer])


if __name__ == "__main__":
    app.run(debug=True)
