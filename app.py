import sqlite3
from datetime import date as day
from datetime import datetime, timedelta
import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
import hashlib

#Konfiguracja strony
st.set_page_config(page_title="Statki", page_icon=":ship:", layout="wide")

#Style
title_style = "color: White; background-color: #262730; text-align: Center; border-radius: 10px;"
info_style = "color: White; background-color: #85C1C1; text-align: Center; border-radius: 10px; font-weight: bold;"

#Tablice/zmienne wykorzystywane dla całej aplikacji
current_time = datetime.now().strftime("%H:%M")
today = day.today()
albatros = []
biala_mewa = []
kormoran = []
ckt_vip = []
tablicaDanych = []
tablicaDanych2 = []

#Klasa danych o statkach
class Ship:
    def __init__(self, id, customer, dc, nb, date, hour, cruise, ship, people, fee, fee_cost, catering, note):
        self.id = id
        self.customer = customer
        self.dc = dc
        self.nb = nb
        self.date = date
        self.hour = hour
        self.cruise = cruise
        self.ship = ship
        self.people = people
        self.fee = fee
        self.fee_cost = fee_cost
        self.catering = catering
        self.note = note
        
    def printData(self):
        data = [f"Imię i nazwisko: {self.customer}", f"Numer telefonu: {self.dc}", f"{self.nb}", f"{self.date}", f"{self.hour}", self.cruise, f"{self.people}", f"Zaliczka: {self.fee}", f"Kwota zaliczki: {self.fee_cost} PLN", f"Katering: {self.catering}", f"Notatki: {self.note}", f"ID: {self.id}"]
        return data

#Klasa rejsów do strony głównej
class Cruise:
    def __init__(self, hour, people, ship, cruise):
        self.hour = hour
        self.people = people
        self.ship = ship
        self.cruise = cruise

    def cruise_id(self):
        hashlib.md5((str(self.cruise) + str(self.hour) + str(self.ship)).encode()).hexdigest()

    def __str__(self):
        return f"hour={self.hour}, people={self.people}"

#Klasa rejsów do strony głównej na wszystkie dni
class Cruise_all:
    def __init__(self, date, hour, people, cruise, ship):
        self.date = date
        self.hour = hour
        self.people = people
        self.cruise = cruise
        self.ship = ship
        
    def cruise_id_all(self):
        hashlib.md5((str(self.date) + str(self.cruise) + str(self.hour) + str(self.ship)).encode()).hexdigest()

#Łączenia się z bazą danych
conn = sqlite3.connect('statki_database.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS rejs (id INTEGER PRIMARY KEY, customer TEXT, date DATE, hour TIME, ship TEXT, fee BOOLEAN, people INTEGER, nb DECIMAL, cruise TEXT, fee_cost INTEGER, catering TEXT, note TEXT, dc TEXT)''')
c.execute('''CREATE TABLE IF NOT EXISTS rejs_new (id INTEGER PRIMARY KEY, customer TEXT, date DATE, hour TIME, ship TEXT, fee BOOLEAN, people INTEGER, nb DECIMAL, cruise TEXT, fee_cost INTEGER, catering TEXT, note TEXT, dc TEXT)''')

#Funkcja dodająca przewidywany czas powrotu
def timeCruise(elem):
    global new_time
    time = datetime.strptime(elem.hour, '%H:%M')
    if elem.cruise == "Po rzekach i jeziorach - 1h":
        new_time = time + timedelta(hours=1)
        return new_time
    elif elem.cruise == "Fotel Papieski - 1h":
        new_time = time + timedelta(hours=1)
        return new_time
    elif elem.cruise == "Kanał Augustowski - 1h":
        new_time = time + timedelta(hours=1)
        return new_time
    elif elem.cruise == "Dolina Rospudy - 1,5h":
        new_time = time + timedelta(hours=1, minutes=30)
        return new_time
    elif elem.cruise == "Szlakiem Papieskim - 3h":
        new_time = time + timedelta(hours=3)
        return new_time
    elif elem.cruise == "Staw Swoboda - 4h":
        new_time = time + timedelta(hours=4)
        return new_time
    elif elem.cruise == "Gorczyca - „Pełen Szlak Papieski” - 6h":
        new_time = time + timedelta(hours=6)
        return new_time
    else:
        return None

#Ustawienia SideBar (DODAĆ DO LOGOWANIA IKONE "box-arrow-in-right")
with st.sidebar:
    selected = option_menu(
        menu_title = "Menu",
        options = ["Strona główna", "Szczegóły", "Panel zarządzania", "Historia"],
        icons = ["house", "book", "pencil-square", "clock-history"],
        menu_icon = "list-task",
        default_index = 0,
    )

#Wybierz dzień
def choiceTheDay():
    columns = st.columns([1,1,1,1])
    with columns[0]:
        theDay = st.date_input("Wybierz dzień")
    return theDay

#Funkcja do dodawania liczby ludzi
def checkCruise(theDay):
    c.execute(f"SELECT hour, people, cruise, ship FROM rejs_new WHERE date='{theDay}' ORDER BY hour")
    for elem in c.fetchall():
        object = Cruise(elem[0], elem[1], elem[2], elem[3])
        for cruise in tablicaDanych:
            if cruise.cruise_id() == object.cruise_id():
                cruise.people += object.people
                break
        else:
            tablicaDanych.append(object)

#Wyświetl skrócone dane o rejsie na dany dzień
def printData(): 
    ct = st.columns([1,1,1,1])
    with ct[0]:
        st.header("Godzina")
    with ct[1]:
        st.header("Ilość osób")
    with ct[2]:
        st.header("Rejs")
    with ct[3]:
        st.header("Statek")
    for elem in tablicaDanych:
        with ct[0]:
            st.write(elem.hour)
        with ct[1]:
            st.write(str(elem.people))
        with ct[2]:
            st.write(elem.cruise)
        with ct[3]:
            st.write(elem.ship)

#Funkcja do dodawania liczby ludzi dla wszystkich rejsów
def checkCruiseForAll():
    c.execute(f"SELECT date, hour, people, cruise, ship FROM rejs_new ORDER BY date")
    for elem in c.fetchall():
        cruise_info = Cruise_all(elem[0], elem[1], elem[2], elem[3], elem[4])
        for cruise2 in tablicaDanych2:
            if cruise2.cruise_id_all() == cruise_info.cruise_id_all():
                cruise2.people += cruise_info.people
                break
        else:
            tablicaDanych2.append(cruise_info)

#Funkcja do wyświetlania skróconych danych o rejsach dla wszystkich dni
def printDataForAll():
    ct_all = st.columns([1,1,1,1,1])
    with ct_all[0]:
        st.header("Data")
    with ct_all[1]:
        st.header("Godzina")
    with ct_all[2]:
        st.header("Ilość osób")
    with ct_all[3]:
        st.header("Rejs")
    with ct_all[4]:
        st.header("Statek")
    for elem in tablicaDanych2:
        with ct_all[0]:
            st.write(elem.date)
        with ct_all[1]:
            st.write(elem.hour)
        with ct_all[2]:
            st.write(str(elem.people))
        with ct_all[3]:
            st.write(elem.cruise)
        with ct_all[4]:
            st.write(elem.ship)

#Zapisywanie danych do poszczególnych tablic
def saveDataToArray():
    for row in c.fetchall():
        cruiseInfo = Ship(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12])
        if cruiseInfo.ship == "Albatros":
            albatros.append(cruiseInfo)
        if cruiseInfo.ship == "Biała Mewa":
            biala_mewa.append(cruiseInfo)
        if cruiseInfo.ship == "Kormoran":
            kormoran.append(cruiseInfo)
        if cruiseInfo.ship == "CKT VIP":
            ckt_vip.append(cruiseInfo)
    
#Wyświetlanie szczegółowych informacji o rejsach
def showDataFromArray(shipTable):
    for object in shipTable:
        timeCruise(object)
        time_str = new_time.strftime('%H:%M')
        st.markdown(f"<p style=\"{info_style}\">{object.hour} - {time_str}<br>{object.cruise}<br>Ilość osób: {object.people}<p>", unsafe_allow_html=True)
        with st.expander("Szczegóły"):
            for info in object.printData():
                st.write(info)

#Całe ustawienia do panelu dodawania informacji
def addCruiseInfo():
    with st.container(border=True):
        columns = st.columns([1,1])
        with columns[0]:
            customer = st.text_input("Podaj imię i nazwisko")
            date = st.date_input("Podaj dzień", value="today", format="DD.MM.YYYY", label_visibility="visible")
            ship = st.selectbox("Wybierz statek", ["Albatros", "Biała Mewa", "Kormoran", "CKT VIP"])
            fee = st.selectbox("Zaliczka", ["Nie", "Tak"])
            people = st.number_input("Ilość osób", step=1, max_value=60, min_value=0)
        with columns[1]:
            phone_column = st.columns([1,3])
            with phone_column[0]:
                dc = st.selectbox("Kierunkowy", ["🇵🇱 +48", "🇷🇺 +7", "🇩🇪 +49", "🇱🇹 +370", "🇱🇻 +371", "🇪🇪 +372", "🇺🇦 +380", "🇨🇿 +420", "🇸🇰 +421"])
            with phone_column[1]:
                nb = st.text_input("Podaj numer telefonu")
            hour = st.time_input("Podaj godzinę")
            cruise = st.selectbox("Wybierz rejs", ["Po rzekach i jeziorach - 1h", "Fotel Papieski - 1h", "Kanał Augustowski - 1h", "Dolina Rospudy - 1,5h", "Szlakiem Papieskim - 3h", "Staw Swoboda - 4h", "Gorczyca - „Pełen Szlak Papieski” – 6h", "Paniewo"])
            fee_cost = st.number_input("Kwota zaliczki")
            catering = st.selectbox("Katering", ["Tak", "Nie"])
        note = st.text_area("Notatki")
        add_button = st.button("Dodaj rezerwację")
    if add_button:
        if customer != "" and nb != "":
            hour_str = hour.strftime("%H:%M")
            c.execute("INSERT INTO rejs (customer, date, hour, ship, fee, people, nb, cruise, fee_cost, catering, note, dc) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (customer, date, hour_str, ship, fee, people, nb, cruise, fee_cost, catering, note, dc))
            c.execute("INSERT INTO rejs_new (customer, date, hour, ship, fee, people, nb, cruise, fee_cost, catering, note, dc) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (customer, date, hour_str, ship, fee, people, nb, cruise, fee_cost, catering, note, dc))
            conn.commit()
            st.warning("Dane zostały dodane pomyślnie", icon="🆗")
        else:
            st.warning("Wprowadź dane", icon="🚨")

#Zapisz do DataFrame wszystkie dane z tabeli
def showAllData():
    c.execute("SELECT customer, dc, nb, ship, date, hour, cruise, people, fee, fee_cost, catering, note, id FROM rejs ORDER BY date, hour")
    df = pd.DataFrame([row for row in c.fetchall()], columns=("Imię i nazwisko", "Kierunkowy", "Nr tel", "Statek", "Data", "Godzina", "Rejs", "Ilość ludzi", "Zaliczka", "Kwota zaliczki", "Katering", "Notatki", "ID"))
    return df

# #Strona do logowania
# if selected == "Zaloguj":
#     st.title("Zaloguj :closed_lock_with_key:")
#     with st.container(border=True):
#         log2 = st.text_input("Podaj login", key="login")
#         pass1 = st.text_input("Podaj hasło", key="password", type="password")
#         log_button = st.button("Zaloguj")
    
#     if (log2 == "admin"):                    
#         st.divider()
#         with st.expander("Dodaj nowego użytkownika :male-technologist:"):
#             im = st.text_input("Podaj imię i nazwisko")
#             lg = st.text_input("Podaj login")
#             ps = st.text_input("Podaj hasło", type="password")
#             ps2 = st.text_input("Powtórz hasło", type="password")
#             user_add_button = st.button("Dodaj użytkowanika")
#             if user_add_button:
#                 if (ps == ps2):
#                     st.info("OK", icon="ℹ️")
#                 else:
#                     st.warning("Hasła nie są identyczne", icon="⚠️")

#Strona główna
if (selected == "Strona główna"):
    tab_1, tab_2 = st.tabs(["Wybrany dzień", "Wszystko"])
    with tab_1:
        theDay = choiceTheDay()
        checkCruise(theDay)
        printData()
                
    with tab_2:
        checkCruiseForAll()
        printDataForAll()

#Szczegóły rejsów
if (selected == "Szczegóły"):
    st.title("Szczegóły rejsów :ship:")
    
    #Wybierz dzień
    theDay2 = choiceTheDay()
    st.divider()
    
    #Kolumny dla danych statków
    scr = st.columns([1,1,1,1])
    with scr[0]:
        st.markdown(f"<h3 style=\"{title_style}\">Albatros<p>Limit osób: 60</p></h3>", unsafe_allow_html=True)
        st.divider()
    with scr[1]:
        st.markdown(f"<h3 style=\"{title_style}\">Biała Mewa<p>Limit osób: 12</p></h3>", unsafe_allow_html=True)
        st.divider()
    with scr[2]:
        st.markdown(f"<h3 style=\"{title_style}\">Kormoran<p>Limit osób: 12</p></h3>", unsafe_allow_html=True)
        st.divider()
    with scr[3]:
        st.markdown(f"<h3 style=\"{title_style}\">CKT VIP<p>Limit osób: 12</p></h3>", unsafe_allow_html=True)
        st.divider()
    
    #Zapis wybranych danych
    c.execute(f"SELECT id, customer, dc, nb, date, hour, cruise, ship, people, fee, fee_cost, catering, note FROM rejs WHERE date='{theDay2}' ORDER BY hour")
    saveDataToArray()
    
    #Wyświetlanie danych
    with scr[0]:
        showDataFromArray(albatros)
    with scr[1]:          
        showDataFromArray(biala_mewa)
    with scr[2]:
        showDataFromArray(kormoran)
    with scr[3]:
        showDataFromArray(ckt_vip)

#Panel zarządzania danymi
if selected == "Panel zarządzania":
    tab1, tab2 = st.tabs(["Dodaj rejs", "Edytuj"])
    with tab1:
        st.header("Dodaj rejs :anchor:")
        addCruiseInfo()
        
    with tab2:
        st.header("Edytuj rejs :pencil:")
        toEdit = showAllData()
        edited_df = st.data_editor(toEdit)
        edit_button = st.button("Zapisz zmiany")
        # if edit_button:
        #     for elem in df:
        #         for columns in elem:
        #             c.execute("UPDATE")
        
if (selected == "Historia"):
    st.markdown("<h1 style=\"background-color: #85C1C1; color: #FFFFFF; border-radius: 10px; font-weight: bold; padding-left: 1rem;\">Historia rejsów<h1>", unsafe_allow_html=True)
    history = showAllData()
    st.dataframe(history)

conn.close()
