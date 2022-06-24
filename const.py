SHIFR = 0
DOPSHIFR = 1
RAIONOBSHII = 2
RAION = 3
AVTOR = 4
MARSHRUT = 5
GOD = 6
MESYAC = 7
KATEGORIYA = 8
TIP = 9
TIPSYDNA = 10
GOROD = 11
KOMMENTARII = 12
SSYLKA = 13
KOLVOSTRANIC = 14
RAZMERARHIVA = 15

set_months = ["", "январь", "февраль", "март", "апрель", "май", "июнь",
              "июль", "август", "сентябрь", "октябрь", "ноябрь", "декабрь"]

set_months_patterns = ["", r"12", r"11", r"10", r"9", r"8", r"7",
                       r"6", r"5", r"4", r"3", r"[^1]2", r"1[^012]"]


def month_to_string(month):
    for m in range(12, 0, -1):
        month = month.replace(str(m), set_months[m])
    return month
