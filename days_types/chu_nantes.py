"""
Day types definition
To convert data to calendar events
"""
from datetime import time

from workdays.workdays import WorkDay

# TODO #7 get them from dedicated sheet
chu_days_types = {
    "M": WorkDay(time(6, 45), time(14, 15), "M-Matin", color=5),
    "Mc": WorkDay(time(6, 45), time(14, 15), "Mc-Matin changeable", color=5),
    "S": WorkDay(time(13, 45), time(21, 15), "S-Soir", color=5),
    "Sc": WorkDay(time(13, 45), time(21, 15), "Sc-Soir changeable", color=5),
    "J": WorkDay(time(8, 30), time(16, 30), "J-Jour", color=5),
    "Ji": WorkDay(time(8, 30), time(16, 30), "Ji-Jour EndoscopI", color=5),
    "Jca": WorkDay(time(8, 30), time(16, 30), "Jca-Jour modifiable", color=5),
    "Jrp": WorkDay(time(8, 30), time(16, 30), "Jrp-Jour modifiable", color=5),
    "N": WorkDay(time(21, 0), time(7, 0), "N-Nuit", color=11),
    "Nca": WorkDay(time(21, 0), time(7, 0), "Nca-Nuit sur Ca de N", color=11),
    "TP": WorkDay(None, None, "Temps Partiel", is_off=True, color=10),
    "TA": WorkDay(None, None, "TA-Repo rtt ?", is_off=True, color=10),
    "To": WorkDay(None, None, "To-Repo recup ?", is_off=True, color=10),
    "RF": WorkDay(None, None, "RF-Repo récupération férier", is_off=True, color=10),
    "CA": WorkDay(None, None, "CA-Congé Annuel", is_off=True, color=10),
    ".CA": WorkDay(None, None, ".CA-Congé Annuel ?", is_off=True, color=10),
    "Rc": WorkDay(None, None, "Rc-Récupération", is_off=True, color=10),
    "_": WorkDay(None, None, "_-Weekend", is_off=True, color=10),
    "": WorkDay(None, None, "Not specified", is_off=True, color=10),
    "OFF": WorkDay(None, None, "OFF-Multi day off", is_off=True, color=10),
    "EM": WorkDay(None, None, "OFF-Enfant Malade", is_off=True, color=10),
    "AM": WorkDay(21, None, "OFF-Arret Maladie", is_off=True, color=10),
}
