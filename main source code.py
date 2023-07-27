import os
import time
import random
import PySimpleGUI as sg
import threading
import pygame

refresh_rate = 0.5

# Dictionary to store song names and checkbox keys
songs = {
    'Clark': 'clark',
    'Danny': 'danny',
    'Dry Hands': 'dry_hands',
    'Equinoxe': 'equinoxe',
    'Haggstrom': 'haggstrom',
    'Key': 'key',
    'Living Mice': 'living_mice',
    'Mice On Venus': 'mice_venus',
    'Minecraft': 'minecraft',
    'Oxygene': 'oxygene',
    'Subwoofer Lullaby': 'subwoofer_lullaby',
    'Sweden': 'sweden',
    'Wet Hands': 'wet_hands',
}


def play_sound(mp3_file):
    pygame.mixer.init()
    pygame.mixer.music.load(mp3_file)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        continue


def main(window):
    while True:
        sound_directories = []

        for song_name, checkbox_key in songs.items():
            if window[checkbox_key].get():
                sound_directory = f'sounds/{checkbox_key}.mp3'
                if os.path.exists(sound_directory):
                    sound_directories.append(sound_directory)

        play_sound_bool = window['play'].get()
        if play_sound_bool:
            if sound_directories:
                playing_sound = random.choice(sound_directories)
                print(f"Playing Sound: {playing_sound}")
                play_sound(playing_sound)

                with open('wait.txt', 'r') as file:
                    pause = file.read()

                if pause == "True":
                    wait_time = random.randint(60, 120)
                    print(f"Waiting in seconds: {wait_time}")
                    time.sleep(wait_time)

        time.sleep(refresh_rate)


def gui():
    layout = [
        [sg.Text("McPlayer 1.0")],
    ]

    row = []
    count = 0
    for song_name, checkbox_key in songs.items():
        row.append(sg.Checkbox(song_name, key=checkbox_key))
        count += 1
        if count % 5 == 0:
            layout.append(row)
            row = []

    if row:  # Add the last row if there are remaining items
        layout.append(row)

    layout.extend([
        [sg.Text("               ")],
        [sg.Checkbox("Play", key='play')],
        [sg.Text("               ")],
        [sg.Text("               ")],
        [sg.Button("Exit")]
    ])

    window = sg.Window("McPlayer 1.0", layout, finalize=True)

    # Start the checkbox monitoring thread
    main_thread = threading.Thread(target=main, args=(window,), daemon=True)
    main_thread.start()

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED or event == 'Exit':
            break

    window.close()


if __name__ == '__main__':
    gui()
