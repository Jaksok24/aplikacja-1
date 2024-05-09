import streamlit as st
import pandas as pd
import numpy as np
import streamlit_option_menu
from streamlit_option_menu import option_menu
import sqlite3
from datetime import datetime, timedelta
from datetime import date as day

#Konfiguracja strony
st.set_page_config(page_title="Statki", page_icon=":ship:", layout="wide")

#Style
title_style = "color: White; background-color: #333333; text-align: Center; border-radius: 10px;"
info_style = "color: White; background-color: #85C1C1; text-align: Center; border-radius: 10px; font-weight: bold;"

#Tablice/zmienne wykorzystywane dla całej aplikacji
log1 = []
log2 = ""
current_time = datetime.now().strftime("%H:%M")
today = day.today()
albatros = []
biala_mewa = []
kormoran = []
ckt_vip = []

#Łączenie z bazą danych
conn = sqlite3.connect('statki_database.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS rejs (id INTEGER PRIMARY KEY, customer TEXT, date DATE, hour TIME, ship TEXT, fee INTEGER, people INTEGER, nb DECIMAL, cruise TEXT, fee_cost INTEGER, catering TEXT, note TEXT, dc TEXT)''')

#Funkcja zliczająca osoby
def countPeopleOnCruise(ship_data, cruise_data, cruise_name, cruise_time):
    total_people = int(cruise_data[1])
    for cruise_data in ship_data:
        if cruise_data[0] == cruise_time and cruise_data[2] == cruise_name:
            total_people = total_people + int(cruise_data[1])
    return total_people

#Funkcja dodająca przewidywany czas powrotu
def timeCruise(element):
    global new_time
    time = datetime.strptime(element[3], '%H:%M')
    if element[4] == "Po rzekach i jeziorach - 1h":
        new_time = time + timedelta(hours=1)
        return new_time
    elif element[4] == "Fotel Papieski - 1h":
        new_time = time + timedelta(hours=1)
        return new_time
    elif element[4] == "Kanał Augustowski - 1h":
        new_time = time + timedelta(hours=1)
        return new_time
    elif element[4] == "Dolina Rospudy - 1,5h":
        new_time = time + timedelta(hours=1, minutes=30)
        return new_time
    elif element[4] == "Szlakiem Papieskim - 3h":
        new_time = time + timedelta(hours=3)
        return new_time
    elif element[4] == "Staw Swoboda - 4h":
        new_time = time + timedelta(hours=4)
        return new_time
    elif element[4] == "Gorczyca - „Pełen Szlak Papieski” - 6h":
        new_time = time + timedelta(hours=6)
        return new_time
    else:
        return None

#Funkcja do usuwania "przeterminowanych" rejsów

#Ustawienia SideBar
with st.sidebar:
    selected = option_menu(
        menu_title = "Menu",
        options = ["Zaloguj", "Strona główna", "Szczegóły", "Panel zarządzania", "Historia"],
        icons = ["box-arrow-in-right", "house", "book", "pencil-square", "clock-history"],
        menu_icon = "list-task",
        default_index = 0,
    )

#Funkcja do logowania
def logowanie():
    log1.append(log2)
    st.write(log1)

#Strona do logowania
if selected == "Zaloguj":
    st.title("Zaloguj :closed_lock_with_key:")
    with st.container(border=True):
        log2 = st.text_input("Podaj login", key="login")
        pass1 = st.text_input("Podaj hasło", key="password", type="password")
        log_button = st.button("Zaloguj")
        if log_button:
            logowanie()
                        
    st.divider()
    with st.expander("Dodaj nowego użytkownika :male-technologist:"):
        im = st.text_input("Podaj imię i nazwisko")
        lg = st.text_input("Podaj login")
        ps = st.text_input("Podaj hasło", type="password")
        ps2 = st.text_input("Powtórz hasło", type="password")
        user_add_button = st.button("Dodaj użytkowanika")
        if user_add_button:
            if (ps == ps2):
                st.info("OK", icon="ℹ️")
            else:
                st.warning("Hasła nie są identyczne", icon="⚠️")

#Strona główna
if (selected == "Strona główna"):
    coltd1 = st.columns([1,1,1,1])
    with coltd1[0]:
        theDay = st.date_input("Wybierz dzień")
    
    #Tablice
    tablicaDanych = []
    
    #Łączenie z bazą danych
    c.execute(f"SELECT * FROM rejs WHERE date='{theDay}' ORDER BY hour")
    
    #Dodawanie danych do poszczególnych tablic
    for new_row in c.fetchall():
        dane_td = [f"{new_row[3]}", f"{new_row[6]}", f"{new_row[8]}", f"{new_row[4]}"]
        tablicaDanych.append(dane_td)
    
    with st.container(border=True):
        for elem in tablicaDanych:
            cruise_time = elem[0]
            cruise_name = elem[2]
            total_people = countPeopleOnCruise(albatros, elem, cruise_name, cruise_time)
            st.markdown(f"<h5 style='background-color: #85C1C1; color: #FFFFFF; text-align: Center; border-radius: 10px'>{elem[0]} | {total_people} osób | {elem[2]} | {elem[3]}</h5><br>", unsafe_allow_html=True)

#Szczegóły rejsów
if (selected == "Szczegóły"):
    st.title("Szczegóły rejsów :ship:")
    
    #Przypisanie danych do odpowiednich tablic
    c.execute("SELECT * FROM rejs ORDER BY hour")
    for row in c.fetchall():
        dane = [f"Imię i nazwisko: {row[1]}", f"Numer telefonu: {row[7]}", f"{row[2]}", f"{row[3]}", f"{row[8]}", row[6], f"Zaliczka: {row[5]}", f"Kwota zaliczki: {row[9]} PLN", f"Katering: {row[10]}", f"Notatki: {row[11]}"]
        if row[4] == "Albatros":
            albatros.append(dane)
        if row[4] == "Biała Mewa":
            biala_mewa.append(dane)
        if row[4] == "Kormoran":
            kormoran.append(dane)
        if row[4] == "CKT VIP":
            ckt_vip.append(dane)  

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
    
    #Wyświetlanie danych    
    with scr[0]:
        for elem in albatros:
            timeCruise(elem)
            time_str = new_time.strftime('%H:%M')
            st.markdown(f"<p style=\"{info_style}\">{elem[3]} - {time_str}<br>{elem[4]}<br>Ilość osób: {elem[5]}<p>", unsafe_allow_html=True)
            with st.expander("Szczegóły"):
                for a in elem:
                    st.write(a)
    with scr[1]:          
            for elem in biala_mewa:
                timeCruise(elem)
                time_str = new_time.strftime('%H:%M')
                st.markdown(f"<p style=\"{info_style}\">{elem[3]} - {time_str}<br>{elem[4]}<br>Ilość osób: {elem[5]}<p>", unsafe_allow_html=True)
                with st.expander("Szczegóły"):
                    for a in elem:
                        st.write(a)
    with scr[2]:
        for elem in kormoran:
                timeCruise(elem)
                time_str = new_time.strftime('%H:%M')
                st.markdown(f"<p style=\"{info_style}\">{elem[3]} - {time_str}<br>{elem[4]}<br>Ilość osób: {elem[5]}<p>", unsafe_allow_html=True)
                with st.expander("Szczegóły"):
                    for a in elem:
                        st.write(a)
    with scr[3]:
        for elem in ckt_vip:
                timeCruise(elem)
                time_str = new_time.strftime('%H:%M')
                st.markdown(f"<p style=\"{info_style}\">{elem[2]} - {time_str}<br>{elem[4]}<br>Ilość osób: {elem[5]}<p>", unsafe_allow_html=True)
                with st.expander("Szczegóły"):
                    for a in elem:
                        st.write(a)

#Panel zarządzania danymi
if (selected == "Panel zarządzania"):
    tab1, tab2 = st.tabs(["Dodaj rejs", "Edytuj"])
    with tab1:
        st.header("Dodaj rejs :anchor:")
        with st.container(border=True):
            columns = st.columns([1,1])
            with columns[0]:
                customer = st.text_input("Podaj imię i nazwisko")
                date = st.date_input("Podaj dzień", value="today", format="DD.MM.YYYY", label_visibility="visible")
                ship = st.selectbox("Wybierz statek", ["Albatros", "Biała Mewa", "Kormoran", "CKT VIP"])
                fee = st.selectbox("Zaliczka", ["Tak", "Nie"])
                people = st.number_input("Ilość osób", step=1, max_value=60, min_value=0)
            
            with columns[1]:
                phone_column = st.columns([1,3])
                with phone_column[0]:
                    dc = st.selectbox("Kierunkowy", ["🇵🇱 +48", "🇷🇺 +7", "🇩🇪 +49", "🇱🇹 +370", "🇱🇻 +371", "🇪🇪 +372", "🇺🇦 +380", "🇨🇿 +420", "🇸🇰 +421" ])
                with phone_column[1]:
                    nb = st.text_input("Podaj numer telefonu")
                hour = st.time_input("Podaj godzinę")
                cruise = st.selectbox("Wybierz rejs", ["Po rzekach i jeziorach - 1h", "Fotel Papieski - 1h", "Kanał Augustowski - 1h", "Dolina Rospudy - 1,5h", "Szlakiem Papieskim - 3h", "Staw Swoboda - 4h", "Gorczyca - „Pełen Szlak Papieski” – 6h", "Paniewo"])
                fee_cost = st.number_input("Kwota zaliczki")
                catering = st.selectbox("Katering", ["Tak", "Nie"])
            note = st.text_area("Notatki")
                
            add_button = st.button("Dodaj rezerwację")
            
            if add_button:
                if (customer != "" and nb != ""):
                    hour_str = hour.strftime("%H:%M")
                    
                    #Zapis w bazie danych
                    c.execute("INSERT INTO rejs (customer, date, hour, ship, fee, people, nb, cruise, fee_cost, catering, note, dc) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                            (customer, date, hour_str, ship, fee, people, nb, cruise, fee_cost, catering, note, dc))
                    conn.commit()
                    st.warning("Dane zostały dodane pomyślnie", icon="🆗")
                else:
                    st.warning("Wprowadź dane", icon="🚨")
        
    with tab2:
        st.header("Edytuj rejs :pencil:")

#Historia
if (selected == "Historia"):
    rejsy_his = []
    
    st.markdown("<h2 style=\"background-color: #85C1C1; color: White; padding-left: 1rem; border-radius: 10px;\">Historia resjów</h2><br>", unsafe_allow_html=True)
    c.execute("SELECT customer, dc, nb, ship, date, hour, cruise, people, fee, fee_cost, catering, note FROM rejs GROUP BY date ORDER BY hour")
    df_rez = pd.DataFrame([row for row in c.fetchall()], columns=("Imię i nazwisko", "Kierunkowy", "Nr tel", "Statek", "Data", "Godzina", "Rejs", "Ilość ludzi", "Zaliczka", "Kwota zaliczki", "Katering", "Notatki"))
    st.dataframe(df_rez)
    
conn.close()
