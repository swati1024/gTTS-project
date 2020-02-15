import speech_recognition as sr  

# get audio from the microphone                                                                       
r = sr.Recognizer()
r.operation_timeout=5                                                                                
with sr.Microphone(chunk_size=4096) as source:                                                                       
    print("Speak:")               
    r.adjust_for_ambient_noise(source,1)                                                                    
    audio = r.listen(source)   
    print('Done')

try:
    print("You said " + r.recognize_google(audio,language='en-GB'))
except sr.UnknownValueError:
    print("Could not understand audio")
except sr.RequestError as e:
    print("Could not request results; {0}".format(e))