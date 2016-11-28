import speech_recognition as sr
import json
import os
from watson_developer_cloud import ConversationV1
with open('../keys.json', 'r') as file_pointer:
    json_object=json.load(open('../keys.json','r'))

def say(text):
    os.system("say " + text)
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

    myText = r.recognize_ibm(audio, username=speechUsername, password=speechPassword)
    return myText


conversation = ConversationV1(
    username=conversationUsername,
    password=conversationPassword,
    version='2016-09-20'
)

# Replace with the context obtained from the initial request
context = {}

print("Start a conversation:")
myText = listen()

response = conversation.message(
    workspace_id=workspaceID,
    message_input={'text': myText},
    context=context
)
i = 0
while(i < 10):
    # print(json.dumps(response, indent=2))
    # print(response['context'])
    context = response['context']
    textualResponse = response['output']['text']
    say(textualResponse[0])
    print("Computer response: ")
    print(textualResponse[0])

    print("Response:")
    myText = listen()
    print(myText)

    response = conversation.message(
        workspace_id=workspaceID,
        message_input={'text': myText},
        context=context
    )
    i = i + 1
