import statistics

FOLDER = "swimdata/"

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
    sah = round(average/ 100, 2)
    # as string list
    mins_secs, hundredths = str(sah).split(".")
    mins_secs = int(mins_secs) 
    minutes = mins_secs // 60
    seconds = mins_secs - minutes *60

    average_str = str(minutes)+":"+str(seconds)+"."+str(hundredths)

    return swimmer, age, distance, stroke, times, average 