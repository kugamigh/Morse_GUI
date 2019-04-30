from tkinter import *
import tkinter.font
from gpiozero import LED
import RPi.GPIO
import time
RPi.GPIO.setmode(RPi.GPIO.BCM)

led = LED(14)

win = Tk()
win.title("Morse GUI")
myFont = tkinter.font.Font(family = 'Helvetica', size = 12, weight = "bold")

edit_label = Label(win, text="Message: ")
edit_label.grid(row=0, column=0)
edit = Entry(win)
edit.grid(row=0, column=1)

EXCLUDED_CHARS = [' ', '!', '@', '#', '$',
                  '%', '^', '&', '*', '(',
                  ')', '-', '_', '=', '+',
                  ';', "'", '"', '\\', '|',
                  '/', '?', ',', '.', '<',
                  '>', '[', ']', '{', '}']

MORSE_CODE_DICT = { 'A':'.-', 'B':'-...', 'C':'-.-.', 'D':'-..', 'E':'.',
                    'F':'..-.', 'G':'--.', 'H':'....', 'I':'..', 'J':'.---',
                    'K':'-.-', 'L':'.-..', 'M':'--', 'N':'-.', 'O':'---',
                    'P':'.--', 'Q':'--.-', 'R':'.-.', 'S':'...', 'T':'-',
                    'U':'..-', 'V':'...-', 'W':'.--', 'X':'-..-', 'Y':'-.--',
                    'Z':'--..', '1':'.----', '2':'..---', '3':'...--', '4':'....-',
                    '5':'.....', '6':'-....', '7':'--...', '8':'---..', '9':'----.',
                    '0':'-----'}

def encrypt(message):
    cipher = ''
    for letter in message:
        if letter not in EXCLUDED_CHARS:
            cipher += MORSE_CODE_DICT[letter] + ' '
        elif letter == ' ':
            cipher += ' '
    return cipher

def decrypt(message):
    message += ' '
    
    ciphertext = ''
    
    for letter in message:
        if ((letter == '.') or (letter == ' ')):
            led.on()
            time.sleep(0.25)
            led.off()
            time.sleep(0.25)
        elif letter == '-':
            led.on()
            time.sleep(0.75)
            led.off()
            time.sleep(0.25)


def readMessage():
    text = edit.get()
    text = text.upper()
    
    if (len(text) < 13):
        ciphertext = encrypt(text)
        
        print(ciphertext)
        decrypt(ciphertext)
    else:
        print("Message too long")


def close():
    RPi.GPIO.cleanup()
    win.destroy()
    
blinkButton = Button(win, text='Blink', font=myFont, command=readMessage, bg='yellow', height=1, width=6)
blinkButton.grid(row=2, column=1)

exitButton = Button(win, text='Exit', font=myFont, command=close, bg='red', height=1, width=6)
exitButton.grid(row=4, column=1)

win.protocol("WM_DELETE_WINDOW", close)

win.mainloop()
