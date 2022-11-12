import json

def checkStackCorrectness(inputStr, outputStr):

    input = json.loads(inputStr)
    output = json.loads(outputStr)

    inputElements = {}
    initialStacks = {}
    for e in input['elements']:
        inputElements[e['id']] = e
        if (not e['stack'] in initialStacks):
            initialStacks[e['stack']] = {}
        initialStacks[e['stack']][e['id']] = e
    

    maxStacks = input['maxStacks']
    stacks = {}
    for i in range(maxStacks):
        stacks[i] = None

    # {
    #     "id": 1,
    #     "elements": [1,3,4]
    # }

    def addToStackIfPossible(e):
        added = False
        for i in range(maxStacks):
            if (stacks[i] == None):
                # print("init new stack")
                stacks[i] = {'id': e['stack'], 'elements': [e]}
                print("New " + str(stacks[i]['id']) + "==" + str(e['stack']))
                added = True
            elif (stacks[i]['id'] == e['stack']):
                # print("add to existing stack")
                stacks[i]['elements'].append(e)
                print("Old " + str(stacks[i]['id']) + "==" + str(e['stack']))
                added = True
            if (added):
                break
        return added

    def popFromInitialStack(e):
        # print(initialStacks)
        prevLen = len(initialStacks[e['stack']])
        initialStacks[e['stack']].pop(e['id'])
        print(str(e['stack']) + " from " + str(prevLen) + " --> " + str(len(initialStacks[e['stack']])))

    def clearStackIfInitialStackFinished(e):
        if (len(initialStacks[e['stack']]) == 0):
            for i in range(int(maxStacks)):
                if stacks[i] is not None:
                    if (stacks[i]['id'] == e['id']):
                        stacks[i] = None
                        break

    def checkStackCorrectnessImpl(): 
        ok = True
        for bed in output['beds']:
            #maybe a stack is finished in this bed, so later we could add the elements to new stack
            outputElementsToCheckLater = []
            for outputElement in bed['elements']:
                inputElement = inputElements[outputElement['id']]
                print("InputElement: " + str(inputElement['id']) + " Stack: " + str(inputElement['stack']))
                # stack with same stack elements or stack with 0 elements
                addedToStack = addToStackIfPossible(inputElement)
                if (addedToStack):
                    popFromInitialStack(inputElement)
                    clearStackIfInitialStackFinished(inputElement)
                else:
                    print("not added to any stack")
                    outputElementsToCheckLater.append(outputElement)
                
            for outputElement in outputElementsToCheckLater:
                #still needs testing
                inputElement = inputElements[outputElement['id']]
                addedToStack = addToStackIfPossible(inputElement)
                if (addedToStack):
                    popFromInitialStack(outputElement)
                    clearStackIfInitialStackFinished(outputElement)
                else:
                    ok = False
                    break

            if (ok != True):
                break
        return ok

    return checkStackCorrectnessImpl()