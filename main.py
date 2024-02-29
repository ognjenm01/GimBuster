from gimadapter import get_terms
import dbadapter
from telegram_notifier import set_config_options
from telegram_notifier import send_message
import os
from dotenv import load_dotenv

load_dotenv()
incoming_terms = get_terms()
current_terms = dbadapter.get_all()
set_config_options(chat_id=os.getenv('SINGLE_CHAT_ID'), token=os.getenv('BOT_API'))

def notify(msg):
    send_message(msg, no_escape=True)

def equal_by_datetime(term1, list_of_terms):
    for term2 in list_of_terms:
        if term1.date == term2.date and term1.time == term2.time:
            return True
    return False

def equal_by_availability(term1, list_of_terms):
    for term2 in list_of_terms:
        if term1.date == term2.date and term1.time == term2.time and term1.is_available != term2.is_available:
            return True
    return False

#Scenario - potpuno nov termin
for iterm in incoming_terms:
    if equal_by_datetime(iterm, current_terms) is False:
        dbadapter.insert(iterm)
        notify("""Obavestenje!
Izbacen je novi termin za grafiku: {0}""".format(iterm.date + " - " + iterm.time))

#Scenario - termin se zauzeo (nema ga u incoming a ima u current)
for cterm in current_terms:
    if equal_by_datetime(cterm, incoming_terms) is False and cterm.is_available:
        cterm.reserve()
        dbadapter.update(cterm, False)  
        notify("""Obavestenje!
Termin u {0} je postao zauzet!""".format(cterm.date + " - " + cterm.time))    
    
#Scenario - termin se vratio - ima ga u oba
for cterm in current_terms:
    if equal_by_availability(cterm, incoming_terms) is True:
        cterm.free()
        dbadapter.update(cterm, True)
        notify("""Obavestenje!
Termin u {0} je postao slobodan!""".format(cterm.date + " - " + cterm.time))         



