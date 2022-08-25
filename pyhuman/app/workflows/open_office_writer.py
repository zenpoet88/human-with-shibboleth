from ..utility.base_workflow import BaseWorkflow
import lorem
from lorem.text import TextLorem
import os
import pyautogui
from time import sleep
import random


WORKFLOW_NAME = 'OpenOfficeWriter'
WORKFLOW_DESCRIPTION = 'Create documents with Apache OpenOffice Writer (Windows)'


sleeptime = 2
openoffice_path = "C:\Program Files (x86)\OpenOffice 4\program\soffice"

def load():
    return DocumentManipulation()

class DocumentManipulation(BaseWorkflow):

    def __init__(self):
        super().__init__(name=WORKFLOW_NAME, description=WORKFLOW_DESCRIPTION)

    def action(self, extra=None):
        self._create_document()

    def _create_document(self):
        self.new_document()
        # Type random paragrahs and sentences
        for i in range(0, random.randint(2,10)):
            random.choice([pyautogui.typewrite(TextLorem().paragraph()), pyautogui.typewrite(TextLorem().sentence())])
            pyautogui.press('enter')
        sleep(sleeptime)
        # Randomly perform actions
        for i in range(0, random.randint(6,15)):
            random.choice([
                self.save_pdf,
                self.write_sentence,
                self.write_paragraph,
                self.copy_paste, 
                self.insert_comment,
                self.find,
                self.delete_text,
                self.format_text])()
            sleep(sleeptime)
        # Save and quit the document
        self.save_quit()


    def insert_comment(self):
        pyautogui.hotkey('ctrl', 'alt', 'c') # insert comment
        pyautogui.typewrite(TextLorem().sentence()) # type random sentence
        pyautogui.press('esc') # finish commenting
        sleep(sleeptime)

    def find(self):
        pyautogui.hotkey('ctrl', 'f') # open Find & Replace
        sleep(sleeptime)
        pyautogui.typewrite(TextLorem()._word()) # type random word
        sleep(sleeptime)
        pyautogui.press('enter') 
        sleep(sleeptime)
        pyautogui.hotkey('alt','y') # close pop up box that may appear
        sleep(sleeptime)
        pyautogui.hotkey('alt','c') # close Find & Replace
        sleep(sleeptime)

    def copy_paste(self):
        self.select_text()
        sleep(sleeptime)
        pyautogui.hotkey('ctrl', 'c') # copy to clipboard
        sleep(sleeptime)
        pyautogui.press('backspace') # delete text
        sleep(sleeptime)
        pyautogui.typewrite(TextLorem().paragraph()) # write text
        sleep(sleeptime)
        pyautogui.press('enter') # insert new line
        pyautogui.press('enter') # insert new line
        pyautogui.hotkey('ctrl', 'v') # paste from clipboard
        sleep(sleeptime)

    def select_text(self):
        selection_params = [
            ['ctrl'  , 'home'], # go to beginning of document
            ['shift' , 'left'], # move cursor & select to left
            ['shift' , 'up'] # move cursor & select up
        ]
        pyautogui.hotkey(*random.choice(selection_params)) 

    def format_text(self):
        self.select_text()
        sleep(sleeptime)
        formatting_params = [
        ['ctrl','1'], # Apply heading 1 style
        ['ctrl','2'], # Apply heading 2 style
        ['ctrl','3'], # Apply heading 3 style
        ['ctrl','d'], # Double underline
        ['ctrl','e'], # Center
        ['ctrl','5'] # Set 1.5 line spacing
        ]
        pyautogui.hotkey(*random.choice(formatting_params))
        sleep(sleeptime)

    def delete_text(self):
        pyautogui.hotkey('ctrl', 'shift', 'delete') # Delete text to beginning of line
        pyautogui.hotkey('ctrl', 'backspace') # Delete text to beginning of word 

    def save_pdf(self):
        # Export a pdf
        pyautogui.hotkey('alt','f') # select to File
        pyautogui.hotkey('alt','d') # select to Export as PDF
        pyautogui.press('enter') # choose Export as PDF
        pyautogui.hotkey('alt','x') # choose Export
        pyautogui.typewrite(TextLorem(wsep='-', srange=(1,3)).sentence()[:-1]) # type random file name
        sleep(sleeptime)
        pyautogui.press('enter') # press enter
        sleep(sleeptime)
        pyautogui.hotkey('alt','y') # choose "yes" if a popup asks if you'd like to overwrite another file


    def new_document(self):
        # Open new document in OpenOffice
        os.startfile(openoffice_path) # open OpenOffice
        sleep(sleeptime)
        pyautogui.press('d') # choose document editing
        sleep(sleeptime)
        # pyautogui.hotkey('ctrl','shift', 'j') # full screen mode


    def save_quit(self):
        pyautogui.hotkey('ctrl', 's') # save
        sleep(sleeptime)
        pyautogui.typewrite(TextLorem(wsep='-', srange=(1,3)).sentence()[:-1]) # type random file name
        sleep(sleeptime)
        pyautogui.press('enter') 
        pyautogui.hotkey('alt','y') # choose "yes" if a popup asks if you'd like to overwrite another file
        sleep(sleeptime)
        pyautogui.hotkey('ctrl','q') # quit OpenOffice

    def write_paragraph(self):
        pyautogui.typewrite(TextLorem().paragraph()), 
    def write_sentence(self):
        pyautogui.typewrite(TextLorem().sentence()), 







