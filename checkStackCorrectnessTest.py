from checkStackCorrectness import checkStackCorrectness

inputFilename = 'sample_data_3.json'
outputFilename = 'output3StackNotOk.json'

inputStr = ""
with open(inputFilename, 'r') as f:
    inputStr = f.read()

outputStr = ""
with open(outputFilename, 'r') as f:
    outputStr = f.read()

if (checkStackCorrectness(inputStr, outputStr)):
    print(outputFilename + ": stack is ok")
else:
    print(outputFilename + ": stack is not ok")
