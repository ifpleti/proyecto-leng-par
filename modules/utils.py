def time_format(time):

    if type(time) is not float:
        raise Exception("time no es float")

    minutes, seconds = divmod(time, 60)

    if int(minutes) > 1 or int(minutes) == 0:
        return str(int(minutes))+" minutos, "+str(round(float(seconds), 2))+" segundos"
    else:
        return str(int(minutes))+" minuto, "+str(round(float(seconds), 2))+" segundos"

def save_object_list(object_list):

    with open("generated.txt", "w", encoding="utf-8") as f:
        for i in range(len(object_list)):
            if i < 10:
                f.write("################# "+str(i)+" #################\n\n")
            elif i < 100:
                f.write("################# "+str(i)+" ################\n\n")
            else:
                f.write("################ "+str(i)+" ################\n\n")
            f.write(str(object_list[i])+"\n\n")