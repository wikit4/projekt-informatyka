#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math

from typing import List, Dict, Tuple
from psychopy import visual, core, event, logging, gui
from os.path import join
import random
import csv
import yaml
import codecs

RESULTS = [["ID", "Typ Sekwencji", "Numer próby", "Wyświetlony tekst", "Typ bodźca", "Kolor tekstu", "Oczekiwany przycisk", "Otrzymany przycisk", "Czas reakcji [ms]", "Poprawność reakcji"]]

def read_text_from_file(file_name: str, insert: str = '') -> str:
    if not isinstance(file_name, str):
        logging.error('Problem with file reading, filename must be a string')
        raise TypeError('file_name must be a string')
    msg = list()
    with codecs.open(file_name, encoding='utf-8', mode='r') as data_file:
        for line in data_file:
            if not line.startswith('#'):  # if not commented line
                if line.startswith('<--insert-->'):
                    if insert:
                        msg.append(insert)
                else:
                    msg.append(line)
    return ''.join(msg)
    
def show_info(win: visual.Window, file_name: str, insert: str = '') -> None:
    msg = read_text_from_file(file_name, insert=insert)
    msg = visual.TextStim(win, color='black', text=msg, height=20) #, wrapWidth=SCREEN_RES['width']
    msg.draw()
    win.flip()
    key = event.waitKeys(keyList=['f7', 'return', 'space', 'left', 'right'])
    if key == ['f7']:
        abort_with_error('Experiment finished by user on info screen! F7 pressed.')
    win.flip()

def feedback(acc):
    if acc:
        feedbk = visual.TextStim(win=win, text="Poprawnie", height=30)

    elif not acc:
        feedbk = visual.TextStim(win=win, text="Niepoprawnie", color="black", height=30)

    else:  # acc is None
        feedbk = visual.TextStim(win=win, text="Proszę, reaguj szybciej", color="black", height=30)
    
    feedbk.draw()
    win.flip()
    core.wait(1)


def training(n_trials=25):
    for trial_num in range(n_trials):
        tabelka.draw()
        fix_cross = visual.TextStim(win=win, text="+", color="black", height=80)
        fix_cross.draw()
        win.flip()
        core.wait(0.7)

        # Choose stimuli type, color, text and key press required
        all_texts = ["FIOLETOWY", "ZIELONY", "ŻÓŁTY", "POMARAŃCZOWY"]
        all_colors = {
            "FIOLETOWY": '#7030A0',
            "ZIELONY": '#00FF1E',
            "ŻÓŁTY": '#FFFF00',
            "POMARAŃCZOWY": '#FF5E00'
        }
        all_keys = ["3", "4", "8", "9"]

        stim_type = random.choice(["Zgodne", "Zgodne", "Niezgodne", "Niezgodne", "Neutralne"])

        if stim_type == "Zgodne":
            idx = random.randint(0, 3)

            text = all_texts[idx]
            color = all_texts[idx]
            key = all_keys[idx]
            stim = visual.TextStim(win=win, text=text, color=all_colors[color], height=80)

        elif stim_type == "Niezgodne":
            idx1 = random.randint(0, 3)
            idx2 = random.randint(0, 3)
            while idx2 == idx1:
                idx2 = random.randint(0, 3)

            text = all_texts[idx1]
            color = all_texts[idx2]
            key = all_keys[idx2]
            stim = visual.TextStim(win=win, text=text, color=all_colors[color], height=80)

        else:  #stim_type == "Neutralne"
            idx = random.randint(0, 3)

            text = '######'
            color = all_texts[idx]
            key = all_keys[idx]
            stim = visual.TextStim(win=win, text=text, color=all_colors[color], height=80)

        tabelka.draw()
        stim.draw()
        win.callOnFlip(clock.reset)
        win.flip()

        key_pressed = event.waitKeys(maxWait=4.0, keyList=["3", "4", "8", "9"])[0]
        time = math.floor(clock.getLastResetTime() / 1000)
        
        # Show result and add to log
        if key is None:
            result = None
        else:
            result = (key_pressed == key)

        feedback(result)

        RESULTS.append(["Trening", trial_num, text, stim_type, color, key, key_pressed, time, result])
        win.flip()
        core.wait(random.uniform(0.7, 1.2))


def experiment(n_trials=50, n_parts=10):
    for part_num in range(n_parts):
        for trial_num in range(n_trials):
            # Draw fixation point and wait 700ms
            tabelka.draw()
            fix_cross = visual.TextStim(win=win, text="+", color="black", height=80)
            fix_cross.draw()
            win.flip()
            core.wait(0.7)

            # Choose stimuli type, color, text and key press required
            all_texts = ["FIOLETOWY", "ZIELONY", "ŻÓŁTY", "POMARAŃCZOWY"]
            all_colors = {
                "FIOLETOWY": '#7030A0',
                "ZIELONY": '#00FF1E',
                "ŻÓŁTY": '#FFFF00',
                "POMARAŃCZOWY": '#FF5E00'
            }
            all_keys = ["3", "4", "8", "9"]

            stim_type = random.choice(["Zgodne", "Zgodne", "Niezgodne", "Niezgodne", "Neutralne"])

            if stim_type == "Zgodne":
                idx = random.randint(0, 3)

                text = all_texts[idx]
                color = all_texts[idx]
                key = all_keys[idx]
                stim = visual.TextStim(win=win, text=text, color=all_colors[color], height=80)

            elif stim_type == "Niezgodne":
                idx1 = random.randint(0, 3)
                idx2 = random.randint(0, 3)
                while idx2 == idx1:
                    idx2 = random.randint(0, 3)

                text = all_texts[idx1]
                color = all_texts[idx2]
                key = all_keys[idx2]
                stim = visual.TextStim(win=win, text=text, color=all_colors[color], height=80)

            else:  # stim_type == "Neutralne"
                idx = random.randint(0, 3)

                text = "######"
                color = all_texts[idx]
                key = all_keys[idx]
                stim = visual.TextStim(win=win, text=text, color=all_colors[color], height=80)

            # Draw stim and get key press
            tabelka.draw()
            stim.draw()
            win.callOnFlip(clock.reset)
            win.flip()

            key_pressed = event.waitKeys(maxWait=4.0, keyList=["3", "4", "8", "9"])[0]
            time = math.floor(clock.getLastResetTime() / 1000)

            # Add result to log
            if key is None:
                result = None
            else:
                result = (key_pressed == key)

            RESULTS.append(["Eksperyment " + str(part_num + 1), trial_num, text, stim_type, color, key, key_pressed, time, result])
            win.flip()
            core.wait(random.uniform(0.7, 1.2))

        # If not final part, show break screen
        if part_num != n_parts - 1:
            show_info(win, join('.', 'messages', 'przerwa.txt'))

def abort_with_error(err: str) -> None:
    logging.critical(err)
    raise Exception(err)

conf = yaml.safe_load(open('config.yaml', encoding='utf-8'))
win = visual.Window(size=conf['SCREEN_RES'], fullscr=False, units='pix', color=conf['BACKGROUND_COLOR'])
win.setMouseVisible(True)
clock = core.Clock()
tabela = read_text_from_file('tabelka.txt') # pos=(350, +350))
tabelka = visual.TextStim(win, color='black', text=tabela, height=35,pos=(-500, +300)) #alignText='left', anchorVert='top')

info: Dict = {'ID': '', 'Płeć': ['M', "K","Inna"], 'Wiek': ''}
dict_dlg = gui.DlgFromDict(dictionary=info, title='Wpisz proszę swoje dane :)')
if not dict_dlg.OK:
    abort_with_error('Info dialog terminated.')
    
PART_ID = info['ID'] + info['Płeć'] + info['Wiek']
    
RESULTS.append(['PART_ID'])

win.setMouseVisible(False)

# Instrukcja
show_info(win, join('.', 'messages', 'hello.txt'))
show_info(win, join('.', 'messages', 'before_training.txt'))
show_info(win, join('.', 'messages', 'trening.txt'))

# Trening
training(conf['N_TRIALS_TRAINING'])

# Przerwa
show_info(win, join('.', 'messages', 'break.txt'))

# Eksperyment
show_info(win, join('.', 'messages', 'sesja_eksperymentalna.txt'))
experiment(conf['N_TRIALS_EXPERIMENT'], conf['EXPNUM'])
show_info(win, join('.', 'messages', 'end.txt'))

with open("result.csv", "w", newline="") as f:
    write = csv.writer(f)
    write.writerows(RESULTS)
