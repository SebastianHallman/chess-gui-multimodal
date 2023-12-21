import chess
from openai import OpenAI
from game.gui import ChessGUI
import PySimpleGUI as sg
import numpy as np
import sounddevice as sd
import soundfile as sf
from dotenv import load_dotenv
import os
from pydub import AudioSegment
import io



# Define these variables before they are used
recording_in_progress = False
duration = 10  # Duration of recording in seconds
fs = 44100  # Sample rate
myrecording = None  # Will hold the recording
load_dotenv()
# Load your OpenAI API key
client = OpenAI(api_key=os.getenv('OPEN_API_KEY'))


# Define a function to convert the audio data to the format expected by the Whisper API
def convert_audio_for_whisper(myrecording):
    # Convert the numpy array to a WAV file
    sf.write('myrecording.wav', myrecording, 44100)

    # Open the WAV file in binary mode
    with open('myrecording.wav', 'rb') as f:
        audio_data = f.read()

    return audio_data


def main():
    global recording_in_progress, duration, fs, myrecording

    sg.theme('Python')
    sg.set_options(font="Cambria 15")

    window = ChessGUI('Chess')

    print(window.board.legal_moves)

    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Exit'):
            break

        print(values)
        # Move from input
        if event == "Send move":
            try: 
                move = chess.Move.from_uci(values[0])
                if move in window.board.legal_moves:
                    print("Moving to: ")
                    print(move)
                    window.board.push(move)
                else:
                    print("Hell nah stop trying to cheat dude")

            except chess.InvalidMoveError:
                print("This is an invalid move")
            
            except ValueError:
                print("This is not a move")
        
        if event == "-RECORD-":
            if not recording_in_progress:
                # Start recording
                # two channel
                # myrecording = sd.rec(int(duration * fs), samplerate=fs, channels=2)
                # one channel
                print("start recording")
                myrecording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
                recording_in_progress = True
            else:
                # Stop recording
                
                sd.stop()
                np.save('myrecording.npy', myrecording)  # Save as a numpy array
                
                recording_in_progress = False
                # Convert the numpy array to a WAV file
                sf.write('myrecording.wav', myrecording, fs)
                
                # Load the WAV file with pydub
                audio = AudioSegment.from_wav('myrecording.wav')
                print("After from wav")
                # Export the audio as an MP3 file
                #audio.export('myrecording.mp3', format='mp3')
                

        if event == "Perform move":
            # Convert the audio data for Whisper
            file = open('myrecording.wav', 'rb')


            # Call the Whisper API
            response = client.audio.transcriptions.create(
                model="whisper-1", 
                file=file
            )

            # Extract the transcribed text from the response
            # text = response['choices'][0]['text']
            print("Transcribed text:",response.text)
            chat_response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "user",
                        "content": f"I have a chess move described in English: '{response.text}'. Please respond only with the standard chess notation for this move, in the format [Start: a1, End: a3]."


                    }
                ]
            )

            res = chat_response.choices[0].message.content
            # Remove the prefix and the brackets
            print("Chat response:", res)
            res = res.replace("[", "").replace("]", "")

            start, end = res.split(", ")
            # Remove the prefixes
            start = start.replace("Start: ", "")
            end = end.replace("End: ", "")
            print("Move:", start + end)

            move = chess.Move.from_uci((start+end).lower())
            if move in window.board.legal_moves:
                print("Moving to: ")
                print(move)
                window.board.push(move)
            else:
                print("Hell nah stop trying to cheat dude")
            


        window.update_board(event)
        window.update_status()
        window.refresh()

    window.close()


if __name__ == '__main__':
    main()
