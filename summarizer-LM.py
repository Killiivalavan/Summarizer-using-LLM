from openai import OpenAI
import speech_recognition as sr
import PyPDF2
import pyttsx3

client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")
recognizer = sr.Recognizer()

def audiototext(audio_filename, text_filename):
    with sr.AudioFile(audio_filename) as audf:
        audio_data = recognizer.record(audf, duration = None)
        try:
            transcribed_text =  recognizer.recognize_google(audio_data)
            with open(text_filename, "w") as transcribedtext:
                transcribedtext.write(transcribed_text)
            return transcribed_text
        except sr.UnknownValueError:
            print("Error during audio recognition. Make sure the audio file is not corrupted")
        except sr.RequestError as r:
            print(f"Error in SpeechRecognition Module:{r}")

def pdftotext(pdf_filename, text_filename):
    with open(pdf_filename, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            text = text + page.extract_text()
        pdf_file.close()
        with open(text_filename, "w", encoding="utf-8") as transcribedtext:
            transcribedtext.write(text)
        return text

def summarize(ttext):
    print("Input is being summarized.....Please Wait")
    try:
        output = client.chat.completions.create(
            model="lmstudio-ai/gemma-2b-it-GGUF",
            messages=[
                {"role": "system", "content": "You are a text summarization assistant. Your job is to provide concise and accurate summaries of the provided content, capturing the main points and important details without losing the original meaning. Focus on clarity and brevity."},
                {"role": "user", "content": ttext}
            ],
            temperature = 0.7
        )
        return output.choices[0].message.content
    except Exception as e:
        print(f"Error generating response: {e}")

def texttospeech(text, audio_filename):
    engine = pyttsx3.init()
    engine.save_to_file(text, audio_filename)
    engine.runAndWait()

def main():
    text_filename = 'transcribed.txt'
    audio_filename = 'audiooutput.wav'
    inputformat = input("Enter 1 for Audio as input or 2 for PDF as input: ")
    outputformat = input("Enter 1 for Text as output or 2 for Audio as output or 3 for both: ")
    if inputformat == '1':
        audio_filename = input("Enter audio file name: ")
        transcriptiontext = audiototext(audio_filename, text_filename)
        summarizedtext = summarize(transcriptiontext)
        if outputformat == '1':
            with open('summary.txt', 'w', encoding="utf-8") as finaloutput:
                finaloutput.write(summarizedtext)
        elif outputformat == '2':
            texttospeech(summarizedtext, audio_filename)
        elif outputformat == '3':
            with open('summary.txt', 'w', encoding="utf-8") as finaloutput:
                finaloutput.write(summarizedtext, audio_filename)
            texttospeech(summarizedtext)
        else:
            print('Enter valid input')
    elif inputformat == '2':
        pdf_filename = input("Enter pdf file name: ")
        transcriptiontext = pdftotext(pdf_filename, text_filename)
        summarizedtext = summarize(transcriptiontext)
        if outputformat == '1':
            with open('summary.txt', 'w', encoding="utf-8") as finaloutput:
                finaloutput.write(summarizedtext)
        elif outputformat == '2':
            texttospeech(summarizedtext, audio_filename)
        elif outputformat == '3':
            with open('summary.txt', 'w', encoding="utf-8") as finaloutput:
                finaloutput.write(summarizedtext)
            texttospeech(summarizedtext, audio_filename)
        else:
            print('Enter valid input')
    else:
        print('Enter valid input')

if __name__ == '__main__':
    main()


     