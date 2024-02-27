from gimadapter import get_terms
import dbadapter
from examterm import ExamTerm
from datetime import datetime
from telegram_notifier import set_config_options
from telegram_notifier import send_message
import os
from dotenv import load_dotenv

incoming_terms = []
current_terms = []
load_dotenv()
set_config_options(chat_id=os.getenv('SINGLE_CHAT_ID'), token=os.getenv('BOT_API'))

def notify(msg):
    send_message(msg, no_escape=True)


incoming_terms = get_terms()
current_terms = dbadapter.get_all()

#Scenario - potpuno nov termin
for iterm in incoming_terms:
    found = False
    for cterm in current_terms:
        if iterm.date == cterm.date and iterm.time == cterm.time:
            found = True

    if found is False:
        dbadapter.insert(iterm)
        notify("""Obavestenje!
Izbacen je novi termin za grafiku: {0}""".format(iterm.date + " - " + iterm.time))

#Scenario - termin se zauzeo (nema ga u incoming a ima u current)
for cterm in current_terms:
    found = False
    for iterm in incoming_terms:
        if iterm.date == cterm.date and iterm.time == cterm.time:
            found = True

    if found is False and cterm.is_available:
        cterm.is_available = False
        cterm.timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        dbadapter.update(cterm, False)  
        notify("""Obavestenje!
Termin u {0} je postao zauzet!""".format(cterm.date + " - " + cterm.time))    
    
#Scenario - termin se vratio - ima ga u oba
for cterm in current_terms:
    found = False
    for iterm in incoming_terms:
        if iterm.date == cterm.date and iterm.time == cterm.time and iterm.is_available != cterm.is_available:
            found = True

    if found is True:
        cterm.is_available = True
        cterm.timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        dbadapter.update(cterm, True)
        notify("""Obavestenje!
Termin u {0} je postao slobodan!""".format(cterm.date + " - " + cterm.time))         



