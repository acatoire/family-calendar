"""
Day types definition
To convert data to calendar events
Colors are defined in
https://google-calendar-simple-api.readthedocs.io/en/latest/colors.html?utm_source=chatgpt.com#list-event-colors
"""
from datetime import time

from workdays.workdays import WorkDay

# TODO #7 get them from dedicated sheet
chu_days_types = {
    "": WorkDay(None, None, "Not specified", is_off=True, color=10),
    ".CA": WorkDay(None, None, "Congé Annuel ?", is_off=True, color=10),
    "AM": WorkDay(21, None, "Arret Maladie", is_off=True, color=10),
    "CA": WorkDay(None, None, "Congé Annuel", is_off=True, color=10),
    "EM": WorkDay(None, None, "Enfant Malade", is_off=True, color=10),
    "J": WorkDay(time(8, 30), time(16, 30), "Jour", color=5),
    "J?": WorkDay(time(7, 15), time(19, 15), "Jour 12 ?", color=5),
    "J1": WorkDay(time(7, 15), time(19, 15), "Jour 12h secteur 1", color=5),
    "J12CA": WorkDay(time(7, 15), time(19, 15), "Jour secteur ? sur CA", color=5),
    "J2": WorkDay(time(7, 15), time(19, 15), "Jour 12h secteur 2", color=5),
    "J3": WorkDay(time(7, 15), time(19, 15), "Jour 12h secteur 3", color=5),
    "Jca": WorkDay(time(8, 30), time(16, 30), "Jour Matin ou soir à confirmer", color=5),
    "Ji": WorkDay(time(8, 30), time(16, 30), "Jour EndoscopI", color=5),
    "Jrp": WorkDay(time(8, 30), time(16, 30), "Jour Matin ou soir à confirmer", color=5),
    "JU": WorkDay(time(7, 15), time(19, 15), "Jour Continue", color=5),
    "M": WorkDay(time(6, 45), time(14, 15), "Matin", color=5),
    "Mc": WorkDay(time(6, 45), time(14, 15), "Matin continue", color=5),
    "Mp": WorkDay(time(7, 15), time(15, 15), "Matin Pansement", color=5),
    "N": WorkDay(time(21, 0), time(7, 0), "Nuit", color=11),
    "N12": WorkDay(time(19, 15), time(7, 15), "Nuit 12h", color=11),
    "N12A": WorkDay(time(19, 15), time(7, 15), "Nuit 12h sur Abs", color=11),
    "N12CA": WorkDay(time(19, 15), time(7, 15), "Nuit 12h sur CA", color=11),
    "Nca": WorkDay(time(21, 0), time(7, 0), "Nuit sur Ca", color=11),
    "NU": WorkDay(time(19, 15), time(7, 15), "Nuit Continue", color=11),
    "OFF": WorkDay(None, None, "Multi day off", is_off=True, color=10),
    "RF": WorkDay(None, None, "Repos récupération férier", is_off=True, color=10),
    "Rc": WorkDay(None, None, "Repos Récupération", is_off=True, color=10),
    "S": WorkDay(time(13, 45), time(21, 15), "S-Soir", color=5),
    "Sc": WorkDay(time(13, 45), time(21, 15), "Soir continue", color=5),
    "TA": WorkDay(None, None, "Repos rtt", is_off=True, color=10),
    "TP": WorkDay(None, None, "Temps Partiel", is_off=True, color=10),
    "To": WorkDay(None, None, "Repos ?", is_off=True, color=10),
    "_": WorkDay(None, None, "_-Weekend", is_off=True, color=10),
}
