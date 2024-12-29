import pyttsx3
import os
import sys
import argparse

def main():
    engine = pyttsx3.init()

    voices = engine.getProperty('voices')
    for i, voice in enumerate(voices):
        print(f"Voice {i}: {voice.name} ({voice.languages})")
        if "Chinese" in voice.name:
            chinese_voice_index = i
            break
        else:
            print("The voice you want is not available")
    print("The Chinese voice index is: ", chinese_voice_index)
    engine.setProperty('voice', voices[chinese_voice_index].id)

    parser = argparse.ArgumentParser(description="Text-to-Speech program with adjustable speech rate.")
    parser.add_argument(
        "rate", 
        type=int, 
        nargs="?",  # Makes the argument optional
        default=1,  # Sets the default value
        help="Set the speech rate multiplier (e.g., 1.5 for 1.5 time speed, 0.5 for 0.5 time speed). Default is 1."
    )
    args = parser.parse_args()

    speech_rate = 150 * args.rate
    # Set other properties like rate and volume (optional)
    engine.setProperty('rate', speech_rate)  # Adjust speaking speed
    engine.setProperty('volume', 1.0)  # Max volume
    print(f"Speech rate set to: {args.rate}")
    print(f"Speech volume set to: 1.0")

    # Determine the directory of the .exe or .py file
    if getattr(sys, 'frozen', False):  # Running as a bundled executable
        base_dir = os.path.dirname(sys.executable)
    else:  # Running as a script
        base_dir = os.path.dirname(os.path.abspath(__file__))

    # Specify the input file located in the same directory as the .exe
    in_file = os.path.join(base_dir, "wenben.txt")
    out_audio_file = os.path.join(base_dir, "output_audio.mp3")

    try:
        # Read the entire content of the file
        with open(in_file, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Split the content into paragraphs (separated by blank lines)
        paragraphs = content.split("\n\n")
        
        for paragraph in paragraphs:
            # Remove any extra whitespace
            paragraph = paragraph.strip()
            if paragraph:  # Check if the paragraph is not empty
                print(f"Reading paragraph:\n{paragraph}\n")
                #engine.say(paragraph)
                engine.save_to_file(content, out_audio_file)
                engine.runAndWait()

    except FileNotFoundError:
        print(f"Error: The file '{in_file}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

    return

if __name__ == "__main__":
    main()