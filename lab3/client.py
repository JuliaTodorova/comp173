import socket, sys, os

# Utilities functions
###################################################################################################

def getRequestInfo():
    url = sys.argv[1]
    urlSplits = url.split("/")

    host = urlSplits[2]

    if len(urlSplits) == 3:
    	resource = "/"
    else:
    	resource = "/" + urlSplits[3]

    return { "host": host, "resource": resource }

def getSocket(host, port):
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soc.connect((host, port))
    return soc

def getIndexCaseInSensitive(source, target):
    sourceUpper = source.upper()
    targetUpper = target.upper()
    if (targetUpper in sourceUpper):
        return sourceUpper.index(targetUpper)
    else:
        return -1

# State machine functions
###################################################################################################

def startStateMachine(initialState):
    currentState = 0

    while (True):
        if (not currentState): currentState = initialState
        currentState = invokeState(currentState)
        if (not currentState): break

def invokeState(state):
    stateName = state["name"]
    if (stateName == "seekStart"):
        return stateSeekStart(state)
    elif (stateName == "seekEnd"):
        return stateSeekEnd(state)
    elif (stateName == "sendToRtvm"):
        return stateSendToRtvm(state)
    elif (stateName == "receiveFromRtvm"):
        return stateReceiveFromRtvm(state)

def stateSeekStart(state):
    resourceResponse = resourceSocket.recv(1024).decode("UTF-8")
    startIndex = getIndexCaseInSensitive(resourceResponse, "<HTML>")

    if (startIndex < 0):
        return { "name": "seekStart" }
    else:
        resourceFragment = resourceResponse[startIndex:]
        endIndex = getIndexCaseInSensitive(resourceFragment, "</HTML>")
        if (endIndex >= 0):
            return { "name": "sendToRtvm", "resourceContent": resourceFragment[:endIndex + 7] }
        else:
            return { "name": "seekEnd", "resourceFragment": resourceFragment }

def stateSeekEnd(state):
    resourceFragment = state["resourceFragment"]
    resourceResponse = resourceSocket.recv(1024).decode("UTF-8")
    resourceFragment = resourceFragment + resourceResponse

    endIndex = getIndexCaseInSensitive(resourceFragment, "</HTML>")
    if (endIndex >= 0):
        return { "name": "sendToRtvm", "resourceContent": resourceFragment[:endIndex + 7] }
    else:
        return { "name": "seekEnd", "resourceFragment": resourceFragment }

def stateSendToRtvm(state):
    resourceContent = state["resourceContent"]
    rtvmSocket.send(resourceContent.encode("UTF-8"))
    return { "name": "receiveFromRtvm" }

def stateReceiveFromRtvm(state):
    rtvmResponse = rtvmSocket.recv(1024).decode("ASCII")
    responseEndedIndex = getIndexCaseInSensitive(rtvmResponse, "COMP173")

    if (responseEndedIndex >= 0):
        print(rtvmResponse[:responseEndedIndex], end='')
        return 0 # We're done; Exit from the state machine.
    else:
        print(rtvmResponse, end='')
        return state

# Main program
###################################################################################################

# Create RTVM socker
rtvmSocket = getSocket("rtvm.cs.camosun.bc.ca", 10010)
rtvmResponse = rtvmSocket.recv(1024)

# Exit if RTVM is not READY
if (rtvmResponse != b'READY'):
    print("RTVM NOT READY!!!")
    print(rtvmResponse)
    sys.exit(0)

# Parse command arguments for request info
requestInfo = getRequestInfo()

# Open resource socket from request info
resourceSocket = getSocket(requestInfo["host"], 80)
resourceSocket.send(("GET " + requestInfo["resource"] + " HTTP/1.1\n" + "Host: " + requestInfo["host"] + "\n\n").encode("UTF-8"))

# Process resource with RTVM via a state machine
startStateMachine({ "name": "seekStart" })

# CLeanup
resourceSocket.close()
rtvmSocket.close()
sys.exit(0)
