import time
import random
import sys
import os
import keyboard
import cursor
from termcolor import colored
from ctypes import *
import pygame

DEBUG = True
SKIP_INTRO = True
FAST_TEXT = True
AI_NAME = "VaultE"

pygame.init()
pygame.mixer.init()
sound_console = pygame.mixer.Sound("sound.wav")
sound_console.set_volume(0.3)
bgm = pygame.mixer.Sound("museum.mp3")
bgm.set_volume(0.1)
startup_sound = pygame.mixer.Sound("computer_startup.mp3")
startup_sound.set_volume(0.3)
hello_sound = pygame.mixer.Sound("computer_hello.mp3")
hello_sound.set_volume(0.3)
pick_sound = pygame.mixer.Sound("pick.wav")
pick_sound.set_volume(0.3)

if not DEBUG and not FAST_TEXT:
    shortPause = 0.05
    mediumPause = 0.1
    longPause = 0.5
else:
    shortPause = 0.01
    mediumPause = 0.02
    longPause = 0.1

failuresMessages = {
    "system" : ["Incorrect input. Try again."],
    "normal" : ["I don't understand. Say again?", "What do you mean? Can you repeat?"]
    }

def flush_input():
    import msvcrt
    while msvcrt.kbhit():
        msvcrt.getch()

def take_input():
    flush_input()
    cursor.show()
    write_line("> ", False)
    i = input()
    cursor.hide()
    return i

def write_line(text, e = True, color = "green", sound = True, speed = 1):
    for i in text:
        sys.stdout.write(colored(i, color))
        if i != " " and sound:
            sound_console.play()  
        sys.stdout.flush()
        if i == "." or i == "!" or i == "?":
            time.sleep(longPause / speed)
        elif i == ",":
            time.sleep(mediumPause / speed)
        else:
            time.sleep(shortPause / speed)
    if e:
        sys.stdout.write("\n")

def sim_write(text):
    time.sleep(0.1)
    write_line("> ", False)
    cursor.show()
    for i in text:
        while True:
            if keyboard.read_key():
                sys.stdout.write(i)
                sys.stdout.flush()
                break
    keyboard.wait("enter")
    cursor.hide()
    print("")

def show_loading(times, text = "Loading", color = "green", sound = True, speed = 1, done = True):
    write_line(text + " ", False, color = color, sound = sound, speed = speed)
    symbols = ["-", "\\", "|", "/"]
    for i in range(times):
        for j in symbols:
            sys.stdout.write(colored(j, color))
            sys.stdout.flush()
            sys.stdout.write('\b')
            time.sleep(mediumPause)
    sys.stdout.write('\b')
    sys.stdout.flush()
    if done:
        write_line(" done.", color = color, sound = sound, speed = speed)

def get_continue(text = "CONTINUE"):
    flush_input()
    write_line("")
    write_line(">[" + text + "]")
    pick_sound.play()
    keyboard.wait("enter")

def get_input(question):
    write_line(question)
    a = take_input()
    return a

def get_ans(question, options, failures = "system", write = True):
    global inpAssist
    if inpAssist or not write:
        p = 0
        write_line(question)
        for i in options:
                write_line(" [" + i + "]")
        flush_input()
        
        while True:
            for i in options:
                print("\033[1A", end='\x1b[2K')
                sys.stdout.flush()
            for i in options:
                if i == options[p]:
                    print(">[" + i + "]")
                else:
                    print(" [" + i + "]")
            pick_sound.play()
            time.sleep(0.1)
            while True:
                if keyboard.is_pressed("down"):
                    p += 1
                    p %= len(options)
                    break
                elif keyboard.is_pressed("up"):
                    p -= 1
                    p %= len(options)
                    break
                elif keyboard.is_pressed("enter"):
                    if write == True and options[p] != "BACK TO MENU":
                        for i in options:
                            print("\033[1A", end='\x1b[2K')
                            sys.stdout.flush()
                        sim_write(options[p])
                        print("\033[1A", end='\x1b[2K')
                    return options[p]
    else:
        if curDialoguePos != -1:
            write_line(AI_NAME + ": ", False, color = "cyan")
            write_line(question)
        while True:
            if curDialoguePos == -1:
                write_line(question)
            for i in options:
                write_line(" [" + i + "]")
            a = take_input()
            atc = a.upper()
            if atc == "BACK":
                return "BACK TO MENU"
            for i in range(len(options) + 1):
                print("\033[1A", end='\x1b[2K')
                sys.stdout.flush()
            for i in options:
                if atc == i.upper():
                    return i
            if curDialoguePos != -1:
                write_line(AI_NAME + ": ", False, color = "cyan")
            if curDialoguePos == -1:
                clear()
            write_line(random.choice(failuresMessages[failures]), color = "red")

def clear(indent = True):
    global current_screen
    os.system("cls")
    if current_screen != "":
        print(current_screen + "\n" * indent)

butterfly = """
  ____         ____
 /. . \       / . .\\
/ .-~-.\ \_/ /.-~-. \\
\ '._.'.\(_)/.'._.' /
 \. ..-. |=| .-.. ./
  \  `-' |=| `-'  /
   \____/|=|\____/
    /.-..|=|..-.\\
   /.`-'./^\.`-'.\\
   \____/   \____/
           
      Vault OS
"""
logo = """
|------------------------- SUDO presents ----------------------------|

███████╗██╗  ██╗██╗   ██╗████████╗██████╗  ██████╗ ██╗    ██╗███╗   ██╗
██╔════╝██║  ██║██║   ██║╚══██╔══╝██╔══██╗██╔═══██╗██║    ██║████╗  ██║
███████╗███████║██║   ██║   ██║   ██║  ██║██║   ██║██║ █╗ ██║██╔██╗ ██║
╚════██║██╔══██║██║   ██║   ██║   ██║  ██║██║   ██║██║███╗██║██║╚██╗██║
███████║██║  ██║╚██████╔╝   ██║   ██████╔╝╚██████╔╝╚███╔███╔╝██║ ╚████║
╚══════╝╚═╝  ╚═╝ ╚═════╝    ╚═╝   ╚═════╝  ╚═════╝  ╚══╝╚══╝ ╚═╝  ╚═══╝

|--------------------- an adventure text game ------------------------|

"""

def displayGameMenu():
    pygame.mixer.stop()
    cursor.hide()
    clear()
    flush_input()
    
    write_line(logo, speed = 10)
    while True:
        clear()
        print(logo)
        ans = get_ans("", ["Start Game", "Change Language"], write = False)
        if ans == "Change Language":
            clear()
            print(logo)
            ansl = get_ans("Choose language", ["Polski", "English"], write = False)
        else:
            break

def displayHelloWorld():
    global current_screen
    current_screen = "--- VaultOS 1.24 Maintenance System ---"
    clear(False)
    hello_sound.play()
    bgm.play()
    print(butterfly)
    time.sleep(1)
    get_continue("ENTER")

def displayMainMenu():
    global current_screen, wereDiagnosticsRun
    current_screen = "--- VaultOS 1.24 Maintenance System ---" 
    clear()
    write_line("Hello " + usr + ".")
    write_line("Welcome to the semi-automatic bunker maintenance system.")
    write_line("")
    if not wereDiagnosticsRun:
        write_line("Warning! ", False, "red")
        write_line("Last diagnostics has been ran ", False)
        write_line("#ERR", False, "cyan")
        write_line(" days ago.")
        write_line("Running diagnostics session is heavily recommended.")
        write_line("")
    bunkerMenu = get_ans("Main menu:", ["Show logs", "Run diagnostics", AI_NAME, "Restart"], write = False)
    return bunkerMenu

def runDiagnostics():
    global current_screen, wereDiagnosticsRun
    current_screen = "--- Maintenance Diagnostics ---"
    clear()
    if not wereDiagnosticsRun:
        waitTime = 0.3
        write_line("Beginning diagnostics.")
        show_loading(10, "Scanning bunker life support systems")
        write_line("")
        write_line("Report:")
        write_line("Registered bunker population: ", False)
        write_line("1", color = "cyan")
        time.sleep(waitTime)
        write_line("Working electricity generators: ", False)
        write_line("6/20", color = "cyan")
        time.sleep(waitTime)
        write_line("Security systems: ", False)
        write_line("UNKNOWN", color = "yellow")
        time.sleep(waitTime)
        write_line("Water filtration system: ", False)
        write_line("OK", color = "cyan")
        time.sleep(waitTime)
        write_line("Emergency water reserves: ", False)
        write_line("OK", color = "cyan")
        time.sleep(waitTime)
        write_line("Oxygen filtration system: ", False)
        write_line("FAILURE", color = "red")
        time.sleep(waitTime)
        write_line("Emergency oxygen reserves: ", False)
        write_line("CRITICAL", color = "red")
        time.sleep(waitTime)
        write_line("")
        write_line("WARNING! OXYGEN LEVELS CRITICAL!", color = "red")
        write_line("Maintenance system must be restarted in order to perform self-fix the faulty life support component.")
        get_continue("RESTART MAINTENANCE SYSTEM")
        clear()
        write_line("Restarting")
        write_line("")
        show_loading(7, "Saving logs")
        write_line("")
        show_loading(5, "Shutting down processes", done = False)
        write_line("")
        wereDiagnosticsRun = True
    write_line("ERROR! ", False, color = "red")
    write_line("Cannot restart maintenance system.")
    write_line("Ongoing processes authorized to block restart: ", False)
    write_line("prc:vaulteAI, prc:vaulteUI", color = "cyan")
    write_line("Developer documentation:")
    write_line("TG: As vaulte has authorization over many lss we're leaving restarting maintenance to them.", color = "cyan")
    write_line("Basically - want to restart, talk to vaulte.", color = "cyan")
    write_line("KK: Are you sure? Maybe we should leave a killswitch or sth.", color = "cyan")
    write_line("TG: Naah there shouldn't be any issues that need restarting so I'm gonna leave it here.", color = "cyan")
    get_continue("BACK TO MENU")

def displayLogs():
    global current_screen
    current_screen = "--- User Logs ---"
    while True:
        clear()
        logs = get_ans("View log:", [
            "Log #1 | 26/08/2025",
            "Log #2 | 13/10/2026",
            "Log #3 | 01/03/2029",
            "DATA CORRUPTED",
            "Log #5 | 25/12/2031",
            "Log #6 | 01/01/1970",
            "Log #7 | 01/01/1970",
            "BACK TO MENU"
        ], write = False)
        if logs == "BACK TO MENU":
            return
        elif logs == "Log #1 | 26/08/2025":
            clear()
            write_line("Log entry #1 | 26/08/2025")
            write_line("By: Overseer Anthony Shultz")
            write_line("")
            write_line("We made it. We managed to close the gates last minute.")
            write_line("Many people made in, tho not everyone had that much luck.")
            write_line("Now just to stick to the schedule. We have supplies to survive long past the predicted time.")
            write_line("")
            write_line("Did the first maintanence diagnostics. Everything's running smoothly. I just hope it'll stay that way.")
            write_line("I'm running mostly on hope to be honest, but one must have something to clinge to in my situation.")
            get_continue("BACK")

def restartGame():
    global current_screen
    current_screen = "--- RESTART GAME ---"
    clear()
    write_line("WARNING! ", False, "red")
    write_line("You're about to restart the game.")
    write_line("You'll loose all progress and come back to the main menu.")
    return get_ans("Are you sure want to restart the game?", ["Yes", "No"], write = False)

def displayVaulte():
    global curDialoguePos, current_screen, wereDiagnosticsRun
    current_screen = "--- " + AI_NAME + " UI ---"
    clear()
    if curDialoguePos == -1:
        show_loading(15, "Connecting to " + AI_NAME)
        if not wereDiagnosticsRun:
            write_line("Error! ", False, "red")
            write_line("Connection timed out.")
            get_continue("BACK TO MENU")
            return
        write_line("Connected.")
        curDialoguePos = 0
        clear()
    if not inpAssist:
        write_line("Write 'BACK' to go pack to the main menu.", color = "yellow")
        write_line("")
    while True:
        playerDialogueResponse = vaulteRespond()
        if playerDialogueResponse == "BACK TO MENU":
            break
        write_line(usr + ": ", False, "cyan")
        write_line(playerDialogueResponse)
        time.sleep(1)
           
def vaulteRespond():
    global curDialoguePos, aiMood

    if curDialoguePos == 0:
        aiMood = "normal"
        question = ({"msg" : "Hi " + usr + ".", "ops" : ["Hello", "There's an issue with the oxygen"]})
    elif curDialoguePos == 1:
        question = ({"msg" : "Good that you're up. I just received readings from the life support systems. There's an issue with the oxygen.", "ops" : ["Yes, that's why I contacted you", "I need you to shut down"]})
    elif curDialoguePos == 2:
        question = ({"msg" : "I know, just received the readings from life support. Fortunately it can be self-fixed.", "ops" : ["Option 1", "Option 2"]})

    if inpAssist:
        write_line(AI_NAME + ": ", False, color = "cyan")
    playerResponse = get_ans(question["msg"], question["ops"] + (["BACK TO MENU"] if inpAssist else []), aiMood)
    if playerResponse == "BACK TO MENU":
        return playerResponse

    if curDialoguePos == 0:
        if playerResponse == "Hello":
            curDialoguePos = 1
        elif playerResponse == "There's an issue with the oxygen":
            curDialoguePos = 2
    elif curDialoguePos == 1:
        if playerResponse == "Yes, that's why I contacted you":
            curDialoguePos = 0
        elif playerResponse == "I need you to shut down":
            curDialoguePos = 0
    
    return playerResponse

while True:
    current_screen = ""
    usr = ""
    pronouns = "They/Them"
    inpAssist = True
    curDialoguePos = -1
    aiMood = "system"
    curPlace = "main"
    if DEBUG:
        wereDiagnosticsRun = True
    else:
        wereDiagnosticsRun = False

    displayGameMenu()

    # intro
    curspeed = 5
    curpause = 0.2
    clear()
    if not DEBUG and not SKIP_INTRO:
        startup_sound.play()
        time.sleep(2)
        write_line("Booting up.\n", speed = curspeed, sound = False)
        time.sleep(2)
        show_loading(2, "Checking subsystems", speed = curspeed, sound = False)
        write_line("CPU: ", speed = curspeed, sound = False, e = False)
        write_line("OK", speed = curspeed, sound = False, color = "cyan")
        write_line("RAM: ", speed = curspeed, sound = False, e = False)
        write_line("OK", speed = curspeed, sound = False, color = "cyan")
        write_line("HDD: ", speed = curspeed, sound = False, e = False)
        write_line("OK", speed = curspeed, sound = False, color = "cyan")
        write_line("Kernel: ", speed = curspeed, sound = False, e = False)
        write_line("OK", speed = curspeed, sound = False, color = "cyan")
        time.sleep(curpause)
        show_loading(3, "Checking I/O devices", sound = False, speed = curspeed)
        write_line("Keyboard: ", speed = curspeed, sound = False, e = False)
        write_line("OK", speed = curspeed, sound = False, color = "cyan")
        write_line("Screen A: ", speed = curspeed, sound = False, e = False)
        write_line("OK", speed = curspeed, sound = False, color = "cyan")
        write_line("Screen B: ", speed = curspeed, sound = False, e = False)
        write_line("NOT FOUND", speed = curspeed, sound = False, color = "yellow")
        write_line("Speakers: ", speed = curspeed, sound = False, e = False)
        write_line("OK", speed = curspeed, sound = False, color = "cyan")
        write_line("Floppy Port A: ", speed = curspeed, sound = False, e = False)
        write_line("FAILURE", speed = curspeed, sound = False, color = "red")
        write_line("Floppy Port B: ", speed = curspeed, sound = False, e = False)
        write_line("FAILURE", speed = curspeed, sound = False, color = "red")
        write_line("USB Port: ", speed = curspeed, sound = False, e = False)
        write_line("OK\n", speed = curspeed, sound = False, color = "cyan")
        time.sleep(curpause)
        show_loading(4, "Loading Graphical User Interface", sound = False, speed = curspeed)
        write_line("Error! ", speed = curspeed, sound = False, e = False, color = "red")
        write_line("GUI cannot load properly. Booting up in performance mode.", speed = curspeed, sound = False)
        write_line("Shell: VSH 3.43 2025\n", speed = curspeed, sound = False)
        write_line("Last session: ", speed = curspeed, sound = False, e = False)
        write_line("25.04.2036", speed = curspeed, sound = False, color = "cyan")
        show_loading(3, "Restoring last session", sound = False, speed = curspeed)
        write_line("Warning! ", speed = curspeed, sound = False, e = False, color = "yellow")
        write_line("Last session not ended properly. Additional user calibration may be needed.\n", speed = curspeed, sound = False)
        time.sleep(curpause)
        write_line("System booted up successfuly.", speed = curspeed, sound = False)
        show_loading(4, "", sound = False, speed = curspeed, done = False)


    if not DEBUG:
        displayHelloWorld()
        clear()
        write_line("Hello [USERNAME].")
        write_line("Welcome to the semi-automatic bunker maintanance system.")
        show_loading(8)
        get_continue()
        clear()
        write_line("Warning! ", False, "yellow")
        write_line("User not calibrated! ", False)
        ans = get_ans("Are you willing to perform calibration now?", ["Yes", "No"], write = False)
        if ans == "Yes":
            initCalibration = True
        else:
            initCalibration = False

    if not DEBUG and not initCalibration:
        clear()
        write_line("Warning! ", False, "yellow")
        write_line("Uncalibrated usage of the maintanance system may lead to certain user-machine issues.")
        write_line("If this is your first time performing maintanance, user calibration is highly advisable.")
        ans = get_ans("Are you still willing to skip the calibration?", ["Yes", "No"], write = False)
        if ans == "No":
            initCalibration = True
        else:
            clear()
            write_line("User calibration skipped.")
            get_continue()

    if not DEBUG and initCalibration:
        while True:
            current_screen = "--- User Calibration ---"
            clear()
            write_line("User calibration initiated.")
            show_loading(4, done = False)

            while True:
                clear()
                usr = get_input("Enter username.")
                write_line("System will now recognize you as " + usr + ".")
                ans = get_ans("Is that correct?", ["Yes", "No"], write = False)
                if ans == "Yes":
                    break
            
            while True:
                clear()
                pronouns = get_ans("Pick your preferred pronouns.", ["He/Him", "She/Her", "They/Them"], write = False)
                write_line("System will now refer to you as " + pronouns + ".")
                ans = get_ans("Is that correct?", ["Yes", "No"], write = False)
                if ans == "Yes":
                    break

            clear()
            write_line("Currently you're using assisted input option. System automatically picks correct input for you, regardless of what you type on keyboard.")
            write_line("You may want to turn it off. It will result in greater immersion, however you will have to be more accurate in your typing.")
            write_line("Capitalization is not taken into account.")
            ans = get_ans("Assisted input", ["On", "Off"], write = False)
            if ans == "Off":
                clear()
                write_line("Warning! ", False,"yellow")
                write_line("Performing maintanence without input assist is recommended for advanced keyboard users only.")
                ans = get_ans("Would you like to receive a short exercise on unassisted inputting?", ["Yes", "No"], write = False)
                if ans == "Yes":
                    clear()
                    write_line("Initializing simulation.")
                    show_loading(4, done = False)
                    current_screen = "--- Unassisted Input Exercise #" + str(random.randint(1001, 9999)) + " ---"
                    clear()
                    write_line("You will receive five prompts to which you will have to and write the answer correctly. System will react accordingly.")
                    get_continue()
                    clear()

                    inpAssist = False
                    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ 0123456789"
                    for i in range(1, 6):
                        calAns = get_ans("Input " + str(i) + ".", ["".join(random.choice(alphabet) for j in range(0, 5 + i))])
                        clear()
                        if calAns == "aezakmi":
                            break

                    write_line("Unassisted input exercise successfuly finished.")
                    write_line("")
                    get_continue()
                current_screen = "--- User Calibration ---"
                clear()
                inpAssist = True
                write_line("Are you still willing to turn the input assist off?")
                ans = get_ans("Assisted input", ["On", "Off"], write = False)
                if ans == "On":
                    inpAssist = True
                else:
                    inpAssist = False
            
            clear()
            write_line("USER CALIBRATION FINISHED")
            write_line("Username: ", False)
            write_line(usr, True, "cyan")
            write_line("Preferred pronouns: ", False)
            write_line(pronouns, True, "cyan")
            write_line("Input assist: ", False)
            if inpAssist:
                write_line("on", True, "cyan")
            else:
                write_line("off", True, "cyan")
            write_line("")
            ans = get_ans("Do you want to repeat calibration?", ["Yes", "No"], write = False)
            if ans == "No":
                clear()
                write_line("User fully calibrated")
                get_continue()
                break        

    # main game loop
    while True:
        if curPlace == "main":
            curPlace = displayMainMenu()
            continue
        elif curPlace == "Show logs":
            displayLogs()
        elif curPlace == "Run diagnostics":
            runDiagnostics()
        elif curPlace == AI_NAME:
            displayVaulte()
        elif curPlace == "Restart":
            doRestart = restartGame()
            if doRestart == "Yes":
                break
        curPlace = "main"

    flush_input()
