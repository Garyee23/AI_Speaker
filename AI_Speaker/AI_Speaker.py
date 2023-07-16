#!/usr/bin/env python3
# Requires PyAudio and PySpeech.
import speech_recognition as sr
import os
import openai
from gtts import gTTS
import playsound
import serial
from Arduino import Arduino

ser = serial.Serial(
    port='COM3',
    baudrate=9600,
    parity=serial.PARITY_NONE,\
    stopbits=serial.STOPBITS_ONE,\
    bytesize=serial.EIGHTBITS,\
) #아두이노 보드와 통신 설정

openai.api_key = "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" #GPT-3.5-turbo를 사용하기 위한 API Key 


def AI_speaker():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("무엇을 도와드릴까요?") 
        tts = gTTS(text='무엇을 도와드릴까요?', lang='ko') #한국어로 '무엇을 도와드릴까요?'라고 말하는 TTS작업
        Hello_file = "Hello.mp3"
        tts.save(Hello_file) #생성된 TTS파일을 mp3형태로 저장
        playsound.playsound(Hello_file) #저장한 mp3 출력하기
        os.remove(Hello_file) 
        audio = r.listen(source)

    try:
        command = r.recognize_google(audio, language='ko-KR') #사용자의 말을 한국어로 인식하여 Command라는 변수에 저장
        
        print("You said: " + command) #내가 한 말이 인식된 결과를 출력
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio") #제대로 인식이 되지 않았을 경우 오류가 발생했다고 출력
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e)) #그 밖의 오류 출력

    messages = [
        {"role": "system", "content": str(command)},
    ]

    message = str(command)
    if message: #사용자가 한 말을 저장
        messages.append(
            {"role": "user", "content": message},
        )
        chat = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=messages #gpt-3.5-turbo 모델 불러오기
        ) #gpt가 대답을 생성

    reply = chat.choices[0].message.content #생성한 대답을 reply에 저장
    print(f"ChatGPT: {reply}") #생성된 대답 출력하기
    messages.append({"role": "assistant", "content": reply}) 
    reply_tts = gTTS(text=reply, lang='ko') #생성된 대답을 TTS작업
    reply_file = "reply.mp3"
    reply_tts.save(reply_file) #작업된 것 mp3파일로 저장
    playsound.playsound(reply_file) #생성된 mp3파일 출력
    os.remove(reply_file)



while True:
    if ser.readable():
        res = ser.readline()   
        print(res)              
        ready = res.decode()[:len(res)-2] # bytes를 decode 해서 str로 변환, 자동으로 포함되어있는 개행을 제거하기 위해 [:len(res)-2] 를 추가함 : 즉, \r\n 을 제거함.

        print(ready) # 아두이노(PLC)에서 날라온 프로토콜.

        if ready == 'ready': #아두이노에서 준비완료 신호가 오면 AI_speaker라는 위의 함수 실행
            AI_speaker()
        else:
            pass


