from MainCode import parent_path
from pathlib import Path

from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext

from app.density.database.database import get_density


def read_float_number(data: str, text: str) -> float:
    import re
    re_value: list = re.findall(text + "\d+\.\d+", data)
    if len(re_value) == 0:
        return 0
    else:
        re_value: str = re_value[0]

    return float(re.findall("\d+\.\d+", re_value)[0])


def read_int_number(data: str, text: str) -> int:
    import re
    re_value: list = re.findall(text + "\d+", data)
    if len(re_value) == 0:
        return 0
    else:
        re_value: str = re_value[0]
    return int(re.findall("\d+", re_value)[0])


def gcode(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Please upload your G_code : ")


def readfile(update: Update, context: CallbackContext) -> None:
    density = get_density()
    dc = update.message.document
    ghazal = dc.get_file()
    path = parent_path.joinpath('app/gcode/junk/' + dc.file_name)
    f_gcode = ghazal.download(str(path))
    path = path.joinpath(f_gcode)

    # print(path)
    with open(path, 'r') as f_gcode:
        data = f_gcode.read()
    Path.unlink(path)
    time = read_int_number(data, "TIME:")
    minute = time // 60
    hour = minute // 60
    minute = minute % 60
    seconds = time % 60

    filament = read_float_number(data, "Filament used: ")
    x_min = read_float_number(data, "MINX:")
    y_min = read_float_number(data, "MINY:")
    z_min = read_float_number(data, "MINZ:")
    x_max = read_float_number(data, "MAXX:")
    y_max = read_float_number(data, "MAXY:")
    z_max = read_float_number(data, "MAXZ:")

    x = round(x_max - x_min, 1)
    y = round(y_max - y_min, 1)
    z = round(z_max - z_min, 1)
    d = round(density * filament)

    text = "time = "

    if hour != 0:
        text += str(hour) + " hour" + " and "

    if minute != 0:
        text += str(minute) + " minutes" + " and "

    text += str(seconds) + " seconds " + "\n"

    text += "filamnt used = " + str(filament) + " m" + "\n" + \
            "x_dimention = " + str(x) + "\n" + \
            "y_dimension = " + str(y) + "\n" + \
            "z_dimension = " + str(z) + "\n" + \
            "weight = " + str(d) + " gram"
    update.message.reply_text(text)

    # text_1 = "Density = " + str(d) + " gram"
    # update.message.reply_text(text_1)
