from flask import Flask, session, render_template, request

import os
import swimclub
import data_utils
import convert_utils

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
@app.get("/swims")
def display_swim_sessions():
     data = data_utils.get_swim_sessions()
     dates = [session[0].split(" ")[0] for session in data]
     return render_template(
          "select.html",
          title = "Select a swim session",
          url="/swimmers",
          select_id="chosen_date",
          data= dates,
     )


@app.post("/swimmers")
def display_swimmers():
    session["chosen_date"] = request.form["chosen_date"]
    data = data_utils.get_session_swimmers(session["chosen_date"])
    swimmers=[f"{swimmer[0]}-{swimmer[1]}" for swimmer in data]
    return render_template(
         "select.html",
         title = "Select a swimmer",
         url = "/showevents",
         select_id = "swimmer",
         data = sorted(swimmers),
         #[f"{d[0]}-{d[1]}" for d in data]
    )

@app.post("/showevents")
def display_swimmers_events():
     #poupulate_data()
     session["swimmer"],session["age"] = request.form["swimmer"].split("-")
     data = data_utils.get_swimmers_events(session["swimmer"], session["age"], session["chosen_date"])
     events = [f"{event[0]} {event[1]}" for event in data]
     return render_template(
          "select.html",
          title = "Select an event",
          url = "/showbarchart",
          select_id = "event",
          data = sorted(events),
          
            
     )

#deprecated not for db-use
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
     distance, stroke = request.form["event"].split(" ")
     data = data_utils.get_swimmers_times(
          session["swimmer"],
          session["age"],
          distance,
          stroke,
          session["chosen_date"],
     )
     times = [time[0] for time in data]
     average_str, times_reversed, scaled = convert_utils.perform_conversions(times)
     world_records = convert_utils.get_worlds(distance, stroke)
     header = f"{session['swimmer']} (Under {session['age']}) {distance} {stroke} - {session['chosen_date']} "
     #location = swimclub.produce_bar_chart(file_id, "templates/")
     return render_template(
          "charts.html",
          title = header,
          data=  list(zip(times_reversed,scaled)),
          average=average_str,
          worlds=world_records,
     )

@app.get("/files/<swimmer>")
def get_swimmer_files(swimmer):
    poupulate_data()
    return str(session["swimmers"][swimmer])


if __name__ == "__main__":
    app.run(debug=True)
