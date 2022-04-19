import re
import os

## Capturing all the coil files, path is a relative path from the project, so
## should be edited to fit your project
coils = os.listdir("../Metal_stuff/SignalExport")

for coil in coils:

    with open("../Metal_stuff/SignalExport/" + str(coil), "r") as read_file:

        string = read_file.read()

    ## This regex will extract the data from the files in 2 capture groups
    captures = re.search(r".*Lengthpoints:;(.*)Values;(.*)", string)

    ## If nothing gets captured, the file will be skipped
    if captures != None:
        lengthpoints = captures.group(1)
        values = captures.group(2)

        lengthpoints = lengthpoints.split(";")
        values = values.split(";")

        ## This both cleans the data and puts it in an iterable array
        clean_data = [
            (lengthpoint, value)
            for (lengthpoint, value) in zip(lengthpoints, values)
            if lengthpoint != "0" and lengthpoint != "" and value != "0" and value != ""
        ]

        ## This is once again a relative path and needs to be edited to point
        ## to the correct directory
        with open("../Metal_stuff/coil_data/" + str(coil), "w") as write_file:

            ## Now we write the data to new csv and delete the old file, this
            ## will lead to us having all cleaned and correct files in the
            ## directory and leave any faulty files in the old directory, we can
            ## now iterate over those files and try to remove them if necessary
            write_file.write("Lengthpoints,Values\n")
            write_file.writelines(
                lengthpoint + "," + value + "\n" for (lengthpoint, value) in clean_data
            )

            os.remove("../Metal_stuff/SignalExport/" + str(coil))

    else:

        print(coil)
