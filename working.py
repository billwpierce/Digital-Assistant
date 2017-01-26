import speech_recognition as sr
import json
import os
import commands
from watson_developer_cloud import ConversationV1
with open('../keys.json', 'r') as file_pointer:
    json_object=json.load(open('../keys.json','r'))

from alchemyapi import AlchemyAPI
alchemyapi = AlchemyAPI()

def say(text):
    os.system("say '" + str(text) + "'")
def runOutputCommand(commandName, extractedAlchemy):
    return str(commands.call(commandName.encode('ascii','ignore'), extractedAlchemy))
from os import path
say("Initializing")

conversationUsername = json_object["CONVERSATION-USERNAME"]
conversationPassword = json_object["CONVERSATION-PASSWORD"]
speechUsername = str(json_object["STT_USERNAME"])
speechPassword = str(json_object["STT_PASSWORD"])
apiKey = str(json_object["API-KEY"])
workspaceID = str(json_object["WORKSPACE_ID"])

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source)

    print("finding audio file")
    AUDIO_FILE = path.join(path.dirname(
        path.realpath(__file__)), "microphone-results.wav")
    print("finding credentials")

    try:
        myText = r.recognize_ibm(audio, username=speechUsername, password=speechPassword)
    except Exception as e:
        myText = "error"
    return myText


conversation = ConversationV1(
    username=conversationUsername,
    password=conversationPassword,
    version='2016-09-20'
)

# Replace with the context obtained from the initial request

print("Start a conversation:")
myText = listen()
extractedAlchemy = alchemyapi.entities('text', myText, {'sentiment': 1})
print(myText)
response = conversation.message(
    workspace_id=workspaceID,
    message_input={'text': myText},
    # context=context
)
# i = 0
while True:
    # print(json.dumps(response, indent=2))
    # print(response['context'])
    textualResponse = response['output']['text']
    if textualResponse[0] == "Could you please repeat?":
        print("not changing context")
    else:
        currentContext = response['context']
    finalResponse = textualResponse[0]
    if finalResponse[0] == "/":
        finalResponse = runOutputCommand(finalResponse[1:], extractedAlchemy)
    print("Computer response: ")
    print(finalResponse)
    say(finalResponse)

    print("Your Response:")
    myText = listen()
    extractedAlchemy = alchemyapi.entities('text', myText, {'sentiment': 1})
    print(myText)
    try:
        print("Context:")
        print(currentContext)
    except NameError as e:
        pass
    try:
        response = conversation.message(
            workspace_id=workspaceID,
            message_input={'text': myText},
            context=currentContext
        )
    except Exception as e:
        try:
            response = conversation.message(
                workspace_id=workspaceID,
                message_input={'text': myText},
            )
        except Exception as e:
            response = conversation.message(
                workspace_id=workspaceID,
            )
    # i = i + 1
