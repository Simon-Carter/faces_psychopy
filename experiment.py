from psychopy import core, visual, gui, data, event
from psychopy.hardware import keyboard
from psychopy.tools.filetools import fromFile, toFile
import numpy as np
import os
import csv

file = open("answers.csv", "r")
answers = list(csv.reader(file, delimiter=","))[0]
file.close()

def finish_task():
    global is_finished
    is_finished = True
    is_finished = True

def set_positive_feedback(feedback, gain=None):
    if not gain:
        correct_fdbk = f'Correct!'
        feedback.setText(correct_fdbk)
    else:
        correct_fdbk = f'Correct! +${gain}'
        feedback.setText(correct_fdbk)

def set_negative_feedback(feedback, loss=None):
    if not loss:
        wrong_fdbk = "Wrong!"
        feedback.setText(wrong_fdbk)
    else:
        wrong_fdbk = f'Wrong! -${abs(loss)}'
        feedback.setText(wrong_fdbk)

def set_timeout_feedback(feedback, loss=None):
    if not loss:
        timeout_fdbk = f'Too slow!'
        feedback.setText(timeout_fdbk)
    else:
        timeout_fdbk = f'Too slow! -${abs(loss)}'
        feedback.setText(timeout_fdbk)
        
def run_test_face(
        exp, 
        stimuli, 
        win, 
        kb,
        answer,
        dollar_sign,
        x_sign,
        simuli_location
):    
    global epi_clock

    trial_index = 0
    face = visual.ImageStim(win, 'faces/img1.png')
    
    for trial in stimuli:
        trial_clock = core.Clock()
        
        correct_flag = False
        response = []

        if is_finished:
            break

        # load the image and collect data
        
        event.clearEvents()
        trial_epi_time = []
        for image_index, image in enumerate(trial):
            last_press = event.getKeys(keyList=['left', 'right'], timeStamped=trial_clock)
            if last_press:
                #print(last_press)
                response, response_time = last_press[-1]
                #print(response)
                exp.addData('response', response)
                exp.addData('response_time', response_time)
                exp.addData('image_response', image_index)
                break
            event.clearEvents()
            face.draw()
            win.flip()
            trial_epi_time.append(epi_clock.getTime())
            core.wait(face_length/35.0)
        
        exp.addData('trial_epi', trial_epi_time)
        
        
        #small delay after choice
        score['text'].draw()
        #print(last_press)
        if not response:
            pass
        elif response == answer[trial_index]:
            correct_flag = True
            
        #if correct_flag == True:
            #dollar_sign.draw()
        #else:
            #x_sign.draw()
        
            
        #print(correct_flag, response, answer[trial_index])
        exp.addData('correct', correct_flag)
        win.flip()
        delay_time = epi_clock.getTime()
        exp.addData('delay_presentation_time', delay_time)

        ISI = core.StaticPeriod()
        ISI.start(T_wait)
        face.setImage = f'{stimuli_location}img{trial_index+1}.png'
        ISI.complete()

        exp.nextEntry()
        end_delay_time = epi_clock.getTime()
        exp.addData('delay_presentation_time', end_delay_time)
        trial_index += 1
            
#---------------------------
# Experimental settings
#---------------------------
stim_pack_name = "BB"
jitter_filename = "jitter_120_final_1.csv"

face_length = 3 # length of each face seconds
num_trials = 10
img_per_trial = 35
feedback = False
stimuli_location = './faces/'
T_wait = 1 # seconds

is_finished = False # Global flag
event.globalKeys.clear()
event.globalKeys.add(key='escape', func = finish_task)

dlg = gui.DlgFromDict({'Name': '', 'Age': ''}, title="Please provide your details :", sortKeys=False)

subject_ID = np.random.randint(1000, 9999)

info = {
    'name': dlg.dictionary['Name'],
    'subject_ID': subject_ID,
    'age': dlg.dictionary['Age'],
    'jitter_file': jitter_filename, 
    'date' : data.getDateStr()
}

#exp = data.ExperimentHandler(
#    name='DCL_implicit_' + stim_pack_name,
#    extraInfo = info,
#    dataFileName = 'res_test' + f'_{stim_pack_name}' + f'_{subject_ID}'
#)

exp = data.ExperimentHandler(
    name='faces',
    extraInfo = info,
    dataFileName = 'face_test' + f'_{subject_ID}'
)

core.checkPygletDuringWait = False
win = visual.Window(size=(800,600), fullscr=True, color=(-1,-1,-1), allowGUI=True, monitor='testMonitor', units='height')

boxsize = [None,None]
fontsize = 0.05
keylist = ['left','right','up','down']

msg_wait = visual.TextBox2(
    win, 
    pos=[0, 0], 
    letterHeight = fontsize,
    text="Waiting for scanner...",
    alignment='center'
)

msg_begin = visual.TextBox2(
    win, 
    size = boxsize,
    letterHeight = fontsize,
    pos=[0, 0.2], 
    text="Task beginning!",
    alignment='center'
)

msg_intro_1 = visual.ImageStim(
    win, 
    'stimuli/dollar_sign.png'
)

custom_intro = [visual.ImageStim(win, f'instructions/inst{i}.png', size=[1,0.5]) for i in range(1,10)]


face_all = [visual.ImageStim(win, f'faces/img{i+1}.png') for i in range(0,img_per_trial*num_trials)]
face_organized = [face_all[i:i + img_per_trial] for i in range(0, len(face_all), img_per_trial)]
#custom_image = [visual.ImageStim(win, f'faces/img{i}.png') for i in face_id_list]

msg_intro_2 = visual.TextBox2(
    win, 
    size = boxsize,
    letterHeight = fontsize,
    pos=[0, 0.3], 
    text="There are two types of dot-patterns:",
    alignment='center'
)

msg_intro_3 = visual.TextBox2(
    win, 
    size = boxsize,
    letterHeight = fontsize,
    pos=[0, 0.3], 
    text="You will see many dot-patterns. \n\n If more",
    alignment='center'
)

msg_press_1 = visual.TextBox2(
    win, 
    size = boxsize,
    letterHeight = fontsize,
    pos=[-0.32, -0.2], 
    text="Press left button",
    alignment='center'
)

msg_press_2 = visual.TextBox2(
    win, 
    size = boxsize,
    letterHeight = fontsize,
    pos=[0.32, -0.2], 
    text="Press right button",
    alignment='center'
)

msg_intro_4 = visual.TextBox2(
    win, 
    pos=[0, 0], 
    letterHeight = fontsize,
    text="""
        We will give you feedback : \n \n
        Yes, you're right! \n \n
        No, you're wrong. 
    """,
    alignment='center'
)

msg_intro_5 = visual.TextBox2(
    win, 
    pos=[0.1, 0], 
    letterHeight = fontsize,
    text="""
        We will give you feedback : \n \n
        +1$ for each correct answer. \n \n
        -1$ for each wrong answer.  
    """,
    alignment='center'
)

msg_intro_6 = visual.TextBox2(
    win, 
    pos=[0, 0], 
    letterHeight = fontsize,
    text="Use the feedback to figure out what makes a pattern \n\n more Type A \n\n or \n\n more Type B",
    alignment='center'
)

msg_self_paced = visual.TextBox2(
    win, 
    pos=[0, 0], 
    letterHeight = fontsize,
    text="Press when ready",
    alignment='center'
)

ITI = visual.TextBox2(
    win, 
    pos=[0, 0], 
    letterHeight = fontsize,
    text="Next dot-pattern incoming!",
    alignment='center'
)

fixation = visual.TextBox2(
    win, 
    pos=[0, 0], 
    letterHeight = 0.2,
    text="+",
    alignment='center'
)

feedback = visual.TextBox2(
    win, 
    pos=[0, 0.25], 
    text="",
    letterHeight = 0.05,
    alignment='center'
)

outro = visual.TextBox2(
    win, 
    text="",
    pos=[0, 0], 
    letterHeight = 0.05,
    alignment='center'
)

dollar_sign = visual.ImageStim(win, 'stimuli/dollar_sign.png',size=[0.5,0.5],pos=[0,-0.1])
check_sign = visual.ImageStim(win, 'stimuli/green_check.png',size=[0.5,0.5],pos=[0,-0.1])
x_sign = visual.ImageStim(win, 'stimuli/red_x.png',size=[0.5,0.5],pos=[0,-0.1])
hourglass = visual.ImageStim(win, 'stimuli/hourglass.png',size=[0.5,0.5],pos=[0,-0.1])

choice_A = visual.TextBox2(win, pos=[-0.3, 0], text="A", alignment='center', letterHeight=0.2)
choice_B = visual.TextBox2(win, pos=[0.3, 0], text="B", alignment='center', letterHeight=0.2)

debug_msg = visual.TextBox2(win, pos=[0.0, -0.1], text="", alignment='center')

score = {
    'current_score' : 0.0, # USD
    'correct_gain' : 1, # USD
    'incorrect_loss' : -1, # USD
    'text' : visual.TextBox2(
                            win, 
                            pos=[0, 0.4], 
                            text='Bonus : $0', 
                            letterHeight = 0.05,
                            alignment='center'
    )
}

kb = keyboard.Keyboard()

fixation.draw()
win.flip()
core.wait(13)

msg_begin.draw()
fixation.draw()
win.flip()
core.wait(3)


# custom test shit
for intro in custom_intro:
    intro.draw()
    win.flip()
    keys = kb.waitKeys(keyList=keylist)
    
#for intro in custom_image:
#    intro.draw()
#    win.flip()
#    core.wait(face_length/35.0)

#for i in face_organized:
#    for j in i:
#        j.draw()
#        win.flip()
#        core.wait(face_length/35.0)

msg_wait.draw()
win.flip()
epi_kb = keyboard.Keyboard()
keys = epi_kb.waitKeys(keyList=['equal'])

epi_clock = core.Clock() 

run_test_face(exp,face_organized,win,kb,answers, dollar_sign,x_sign, stimuli_location)

outro.setText(f'Congratulations!\nYou won ${int(score["current_score"])}!\nPress any button to complete the task.')
outro.draw()
win.flip()
keys = kb.waitKeys()

win.close()
core.quit()
