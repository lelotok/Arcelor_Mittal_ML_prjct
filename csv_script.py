import re
import os

directory_list = os.listdir("SignalExport")
for directory in directory_list:
    print(directory)

    file = open("SignalExport/" + directory, "r")
    string = file.read()

    captures = re.search(r'.*Lengthpoints:;(.*)Values;(.*)', string)

    lengthpoints = captures.group(1)
    values = captures.group(2)

    lengthpoints = lengthpoints.split(";")
    values = values.split(";")

    file.close()

    file = open("SignalExport/" + directory, "w")

    file.write("Lengthpoints;Values\n")
    file.writelines(lengthpoint + ";" + value + "\n" for (lengthpoint, value) in zip(lengthpoints, values))
    file.close()
