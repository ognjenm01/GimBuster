from examterm import ExamTerm
import requests
from bs4 import BeautifulSoup
from util import timestamp
import time as t
import os

terms = []
term_dates = []

def get_term_dates(session, term_dates):
    get_dates_req = session.get("http://gim.ftn.uns.ac.rs/IzmenaZakazanogTermina")
    soup = BeautifulSoup(get_dates_req.content, 'html.parser')
    for tag in soup.find_all("option"):
        data_url = tag['data-url']
        if "nastavnik=1" in data_url and "&" in data_url:
            term_dates.append(tag['value'])

def attach_time_to_term_date(terms, session, term_dates):
    for term_date in term_dates:
        get_times_for_term = session.get("http://gim.ftn.uns.ac.rs/IzmenaZakazanogTermina?nastavnik=1&datum=" + str(term_date))
        soup = BeautifulSoup(get_times_for_term.content, 'html.parser')
        for tag in soup.find_all("option"):
            try:
                if "RG usmeni" in tag['data-napomena']:
                    new_term = ExamTerm(term_date, tag.text, True, timestamp())
                    terms.append(new_term)
                    print(new_term)
            except KeyError:
                continue

        t.sleep(0.3)

def get_terms():
    with requests.Session() as session:
        session.headers = {
            "Accept": "*/*",
            "Host": "gim.ftn.uns.ac.rs",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Content-Type": "application/x-www-form-urlencoded",
            "Content-Length": "75"
        }
        login_req = session.post("http://gim.ftn.uns.ac.rs/Prijava", data="povratniUrl=%3F&korisnickoIme=" + os.getenv('GIM_USERNAME') + "&lozinka=" + os.getenv('GIM_SIFRA'))

        session.headers.pop("Content-Length")
        session.headers['Content-Type'] = 'text/html;charset=UTF-8'

        get_term_dates(session, term_dates)
        attach_time_to_term_date(terms, session, term_dates)

        return terms
