import os
from openai import OpenAI
import speech_recognition as sr
import PyPDF2
import pyttsx3

client = OpenAI(
    base_url="http://localhost:11434/v1",  
    api_key="ollama"  
)

recognizer = sr.Recognizer()

def get_absolute_path(filename):
    """
    Convert a filename to its absolute path and ensure the directory exists.
    """
    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Create full path
    full_path = os.path.join(script_dir, filename)
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    
    return full_path

def audiototext(audio_filename, text_filename):
    try:
        # Additional diagnostic information
        print(f"Attempting to transcribe: {audio_filename}")
        print(f"File exists: {os.path.exists(audio_filename)}")
        print(f"File size: {os.path.getsize(audio_filename)} bytes")

        with sr.AudioFile(audio_filename) as audf:
            # Adjust for ambient noise
            recognizer.adjust_for_ambient_noise(audf, duration=0.5)
            
            # Record the entire audio
            audio_data = recognizer.record(audf)
            
            try:
                # Try multiple recognition methods
                transcription_methods = [
                    recognizer.recognize_google,
                    recognizer.recognize_sphinx  # Offline fallback
                ]
                
                for method in transcription_methods:
                    try:
                        transcribed_text = method(audio_data)
                        if transcribed_text:
                            # Save transcribed text
                            text_path = get_absolute_path(text_filename)
                            with open(text_path, "w", encoding='utf-8') as transcribedtext:
                                transcribedtext.write(transcribed_text)
                            
                            print(f"Transcription successful using {method.__name__}")
                            print(f"Transcribed text saved to: {text_path}")
                            
                            return transcribed_text
                    except Exception as method_error:
                        print(f"Method {method.__name__} failed: {method_error}")
                
                raise ValueError("No transcription method succeeded")
            
            except sr.UnknownValueError:
                print("Speech Recognition could not understand the audio")
            except sr.RequestError as request_error:
                print(f"Could not request results from Speech Recognition service: {request_error}")
    
    except Exception as general_error:
        print(f"Unexpected error in audio transcription: {general_error}")
    
    return ""  # Return empty string instead of None

def pdftotext(pdf_filename, text_filename):
    with open(pdf_filename, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            text = text + page.extract_text()
        pdf_file.close()
        text_path = get_absolute_path(text_filename)
        with open(text_path, "w", encoding="utf-8") as transcribedtext:
            transcribedtext.write(text)
        print(f"PDF text extracted and saved to: {text_path}")
        return text

def summarize(ttext):
    print("Input is being summarized.....Please Wait")
    try:
        # List of models to try
        models_to_try = ["llama3", "mistral", "llama2", "llama3.2"]
        
        for model in models_to_try:
            try:
                output = client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": "You are a text summarization assistant. Provide a concise and accurate summary of the provided content, capturing main points and important details."},
                        {"role": "user", "content": ttext}
                    ],
                    temperature=0.7
                )
                summary = output.choices[0].message.content
                if summary:
                    return summary
            except Exception as model_error:
                print(f"Error with model {model}: {model_error}")
        
        # If no model works
        print("Failed to generate summary with any available model.")
        return "Unable to generate summary due to model errors."

    except Exception as e:
        print(f"Unexpected error generating response: {e}")
        return "Summary generation failed."

def texttospeech(text, audio_filename):
    engine = pyttsx3.init()
    audio_path = get_absolute_path(audio_filename)
    engine.save_to_file(text, audio_path)
    engine.runAndWait()
    print(f"Audio summary saved to: {audio_path}")

def main():
    # Always use consistent naming for output files in the same directory as the script
    text_filename = 'transcribed.txt'
    audio_filename = 'audiooutput.wav'
    summary_text_filename = 'summary.txt'
    
    inputformat = input("Enter 1 for Audio as input or 2 for PDF as input: ")
    outputformat = input("Enter 1 for Text as output or 2 for Audio as output or 3 for both: ")
    
    try:
        if inputformat == '1':
            audio_filename = input("Enter audio file name: ")
            transcriptiontext = audiototext(audio_filename, text_filename)
            
            # Added check to ensure transcription is not empty
            if not transcriptiontext:
                print("No text could be transcribed from the audio file.")
                return
            
            summarizedtext = summarize(transcriptiontext)
            
            if outputformat == '1':
                summary_path = get_absolute_path(summary_text_filename)
                with open(summary_path, 'w', encoding="utf-8") as finaloutput:
                    finaloutput.write(summarizedtext)
                print(f"\n🔍 Summary saved as text file:")
                print(f"Location: {summary_path}")
            
            elif outputformat == '2':
                texttospeech(summarizedtext, audio_filename)
                print(f"\n🔊 Audio summary created. Check the file in the same directory.")
            
            elif outputformat == '3':
                # Text output
                summary_path = get_absolute_path(summary_text_filename)
                with open(summary_path, 'w', encoding="utf-8") as finaloutput:
                    finaloutput.write(summarizedtext)
                
                # Audio output
                texttospeech(summarizedtext, audio_filename)
                
                print("\n📄 Outputs Generated:")
                print(f"Text Summary: {summary_path}")
                print(f"Audio Summary: {get_absolute_path(audio_filename)}")
            
            else:
                print('Enter valid input')
        
        elif inputformat == '2':
            pdf_filename = input("Enter pdf file name: ")
            transcriptiontext = pdftotext(pdf_filename, text_filename)
            summarizedtext = summarize(transcriptiontext)
            
            if outputformat == '1':
                summary_path = get_absolute_path(summary_text_filename)
                with open(summary_path, 'w', encoding="utf-8") as finaloutput:
                    finaloutput.write(summarizedtext)
                print(f"\n🔍 Summary saved as text file:")
                print(f"Location: {summary_path}")
            
            elif outputformat == '2':
                texttospeech(summarizedtext, audio_filename)
                print(f"\n🔊 Audio summary created. Check the file in the same directory.")
            
            elif outputformat == '3':
                # Text output
                summary_path = get_absolute_path(summary_text_filename)
                with open(summary_path, 'w', encoding="utf-8") as finaloutput:
                    finaloutput.write(summarizedtext)
                
                # Audio output
                texttospeech(summarizedtext, audio_filename)
                
                print("\n📄 Outputs Generated:")
                print(f"Text Summary: {summary_path}")
                print(f"Audio Summary: {get_absolute_path(audio_filename)}")
            
            else:
                print('Enter valid input')
        
        else:
            print('Enter valid input')
    
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    main()