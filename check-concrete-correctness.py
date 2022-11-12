import json

inputFilename = 'sample_data_1.json'
outputFilename = 'outputFormat.json'

inputFile = open(inputFilename)
outputFile = open(outputFilename)
input = json.load(inputFile)
output = json.load(outputFile)


inputElements = {}
for e in input['elements']:
  inputElements[e['id']] = e


ok = True
for bed in output['beds']:
    firstElement = bed['elements'][0]
    concrete = inputElements[firstElement['id']]['concrete']
    for bedEl in bed['elements']:
        ok = inputElements[bedEl['id']]['concrete'] == concrete
        if (ok != True):
            break
    if (ok != True):
        break

if (ok):
    print(outputFilename + ": is ok")
else:
    print(outputFilename + ": is not ok")


inputFile.close
outputFile.close