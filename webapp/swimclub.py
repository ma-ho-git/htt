import statistics
import hfpy_utils

FOLDER = "swimdata/"
CHARTS = "charts/"

def read_swim_data(filename):
    
    # data from filename
    swimmer, age, distance, stroke =filename.split(".")[0].split("-")

    # data from file
    with open (FOLDER+filename) as file:
        lines = file.readlines()
        times = lines[0].strip().split(",")

    # text to int
    converts = []
    for t in times:
        if ":" in t:
            minutes, tail = t.split(":")
            seconds , hundredth = tail.split(".")
        else:
            minutes = 0
            seconds , hundredth = t.split(".")
        converts.append((int(minutes)*60*100 + (int(seconds)*100)) + int(hundredth))


    average = statistics.mean(converts)
    # seconds and hundredth
    # sah = round(average/ 100, 2)
    # as string list
    mins_secs, hundredths = f"{(average/100):.2f}".split(".") # str(sah).split(".")
    mins_secs = int(mins_secs) 
    minutes = mins_secs // 60
    seconds = mins_secs - minutes *60

    average = f"{minutes}:{seconds:0>2}.{hundredths}" 
    #str(minutes)+":"+str(seconds)+"."+str(hundredths)
    return swimmer, age, distance, stroke, times, average, converts



def produce_bar_chart(filename, location=CHARTS):
    (swimmer, age, distance, stroke, times, avarage, converts) = read_swim_data(filename)

    title = f"{swimmer} (Under {age} ) {distance} {stroke}"

    # start html file
    html = f"""<!DOCTYPE html> 
    <html>
        <head>
            <title> {title} </title>
            <link rel="stylesheet" href="/static/webapp.css"/> 
        </head>
        <body> 
            <h2>  {title} </h2>"""
    
    # svg-bild
    from_max = max(converts)
    svgs = ""
    times.reverse()
    converts.reverse()

    for n, t in enumerate(times):
        bar_width = hfpy_utils.convert2range(converts[n],0,from_max,0,350)
        svgs = svgs + f"""
        
            <svg height="30" width="400">
                <rect height="30" width="{bar_width}" style="fill:rgb(0,0,255);"  > 
            </svg>{t} <br />
            """
    # eof    
    footer = f"""
                    <p> Average time: {avarage}</p>
            </body>
    </html>
    """
    page = f"{html}{svgs}{footer}"
    save_to =f"{location}{filename.removesuffix(".txt")}.html"

    # generierte seite in html-datei schreiben
    with open(save_to, "w") as tf: # mit parameter w wird neu geschrieben mit a angehängt
        print(page, file=tf)
    
    return save_to