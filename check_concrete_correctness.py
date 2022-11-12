import json


def checkConcreteCorrectness(inputStr, outputStr):
    input = json.loads(inputStr)
    output = json.loads(outputStr)
    inputElements = {}
    for e in input["elements"]:
        inputElements[e["id"]] = e

    ok = True
    for bed in output["beds"]:
        firstElement = bed["elements"][0]
        concrete = inputElements[firstElement["id"]]["concrete"]
        for bedEl in bed["elements"]:
            ok = inputElements[bedEl["id"]]["concrete"] == concrete
            if ok != True:
                break
        if ok != True:
            break

    return ok


# inputFilename = 'sample_data_1.json'
# outputFilename = 'output1ConcreteOk.json'

# inputStr = ""
# with open(inputFilename, 'r') as f:
#     inputStr = f.read()

# outputStr = ""
# with open(outputFilename, 'r') as f:
#     outputStr = f.read()

# if (checkConcreteCorrectness(inputStr, outputStr)):
#     print(outputFilename + ": concrete is ok")
# else:
#     print(outputFilename + ": concrete is not ok")
