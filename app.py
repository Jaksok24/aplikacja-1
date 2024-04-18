import streamlit as st
import pandas as pd
import numpy as np
import streamlit_option_menu
from streamlit_option_menu import option_menu
import sqlite3
from datetime import datetime, date, timedelta

#Konfiguracja strony
st.set_page_config(page_title="Statki", page_icon=":ship:", layout="wide")

#Funkcja zliczająca osoby
def countPeopleOnCruise(ship_data, cruise_name, cruise_time):
    total_people = 0
    for cruise_data in ship_data:
        if cruise_data[2] == cruise_time and cruise_data[4] == cruise_name:
            total_people = total_people + cruise_data[5]
    return total_people

#Funkcja dodająca przewidywany czas powrotu
def timeCruise(elem):
    time = datetime.strptime(elem[2], "%H:%M")
    if elem[4] == "Po rzekach i jeziorach - 1h":
        return time + timedelta(hours=1)
    elif elem[4] == "Fotel Papieski - 1h":
        return time + timedelta(hours=1)
    elif elem[4] == "Kanał Augustowski - 1h":
        return time + timedelta(hours=1)
    elif elem[4] == "Dolina Rospudy - 1,5h":
        return time + timedelta(hours=1, minutes=30)
    elif elem[4] == "Szlakiem Papieskim - 3h":
        return time + timedelta(hours=3)
    elif elem[4] == "Staw Swoboda - 4h":
        return time + timedelta(hours=4)
    elif elem[4] == "Gorczyca - „Pełen Szlak Papieski” - 6h":
        return time + timedelta(hours=6)
    else:
        return None

current_time = datetime.now().strftime("%H:%M")

#Funkcja do usuwania "przeterminowanych" rejsów
def removeExpiredCruises(ship_data):
    current_time = datetime.now().strftime("%H:%M")
    updated_ship_data = []
    for cruise_data in ship_data:
        cruise_time = cruise_data[2]  # Godzina rejsu znajduje się pod indeksem 2 w danych o rejsie
        if cruise_time >= current_time:
            updated_ship_data.append(cruise_data)
    return updated_ship_data

#Ustawienia SideBar (ikona do logowania: "box-arrow-in-right") (DODAĆ PÓŹNIEJ STRONE DO LOGOWANIA!!!)
with st.sidebar:
    selected = option_menu(
        menu_title = "Menu",
        options = ["Strona główna", "Rezerwacje"],
        icons = ["house", "book"],
        menu_icon = "list-task",
        default_index = 0,
    )

#Style
title_style = "color: White; background-color: #333333; text-align: Center; border-radius: 10px;"
info_style = "color: White; background-color: #85C1C1; text-align: Center; border-radius: 10px; font-weight: bold;"

log1 = []
log2 = ""

#Funkcja do logowania
def logowanie():
    log1.append(log2)
    st.write(log1)

# #Strona do logowania
# if selected == "Zaloguj":
#     st.title("Zaloguj :closed_lock_with_key:")
#     with st.container(border=True):
#         log2 = st.text_input("Podaj login", key="login")
#         pass1 = st.text_input("Podaj hasło", key="password", type="password")
#         log_button = st.button("Zaloguj")
#         if log_button:
#             logowanie()
#     st.divider()
#     with st.expander("Dodaj nowego użytkownika :male-technologist:"):
#         im = st.text_input("Podaj imię i nazwisko")
#         lg = st.text_input("Podaj login")
#         ps = st.text_input("Podaj hasło", type="password")
#         ps2 = st.text_input("Powtórz hasło", type="password")
#         user_add_button = st.button("Dodaj użytkowanika")
#         if user_add_button:
#             if (ps == ps2):
#                 st.info("OK", icon="ℹ️")
#             else:
#                 st.warning("Hasła nie są identyczne", icon="⚠️")

#Rejsy na dany dzień
if (selected == "Strona główna"):
    
    #Tablice do statków
    albatros = []
    biala_mewa = []
    kormoran = []
    ckt_vip = []

    #Łączenie z bazą danych
    conn = sqlite3.connect('statki.db')
    c = conn.cursor()

    #Tworzrenie bazy danych jeśli nie istnieje
    c.execute('''CREATE TABLE IF NOT EXISTS rejs (id INTEGER PRIMARY KEY, customer TEXT, hour TIME, ship TEXT, fee INTEGER, ticket TEXT, nb DECIMAL, people INTEGER, cruise TEXT, fee_cost FLOAT, note TEXT, today DATE)''')

    st.title("Dodaj rejs :anchor:")

    #Dodaj rejs
    with st.expander("Dodaj nowy rejs"):
        columns_add = st.columns([1,1])
        with columns_add[0]:
            customer = st.text_input("Podaj imię i nazwisko")
            hour = st.time_input("Podaj godzinę", value="now")
            ship = st.selectbox("Wybierz statek", ["Albatros", "Biała Mewa", "Kormoran", "CKT VIP"])
            fee = st.selectbox("Zaliczka", ["Tak", "Nie"])
            ticket = st.selectbox("Bilet opłacony", ["Tak", "Nie"])

        with columns_add[1]:
            nb = st.text_input("Podaj numer telefonu")
            people = st.number_input("Ilość osób", step=1, max_value=60, min_value=0)
            cruise = st.selectbox("Wybierz rejs: ", ["Po rzekach i jeziorach - 1h", "Fotel Papieski - 1h", "Kanał Augustowski - 1h", "Dolina Rospudy - 1,5h", "Szlakiem Papieskim - 3h", "Staw Swoboda - 4h", "Gorczyca - „Pełen Szlak Papieski” – 6h", "Paniewo"])
            fee_cost = st.number_input("Kwotwa zaliczki")

        note = st.text_area("Notatki")
        add_button = st.button("Dodaj rejs")

        #Jeśli przycisk zostanie naciśnięty dane o rejsie dodadzą się do bazy danych statki.db
        if add_button:
            if not customer:
                st.warning("Wprowadź imię i nazwisko", icon="🚨")
            elif not nb:
                st.warning("Wprowadź numer telefonu", icon="🚨")
            elif people == 0:
                st.warning("Wprowadź liczbę osób", icon="🚨")
            else:
                hour_str = hour.strftime("%H:%M")
                if hour_str >= current_time:
                    c.execute("INSERT INTO rejs (customer, hour, ship, fee, ticket, nb, people, cruise, fee_cost, note, today) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (customer, hour_str, ship, fee, ticket, nb, people, cruise, fee_cost, note, today))
                    conn.commit()
                    st.warning("Dane zostały dodane pomyślnie", icon="🆗")
                else:
                    st.warning("Podana godzina już minęła", icon="🚨")

    st.divider()
    
    #Ustawienia etykiet statków
    ship_column = st.columns([1,1,1,1])
    with ship_column[0]:
        st.markdown(f"<h2 style=\"{title_style}\">Albatros<p>Limit osób: 60</p></h2>", unsafe_allow_html=True)
        st.divider()
    with ship_column[1]:
        st.markdown(f"<h2 style=\"{title_style}\">Biała Mewa<p>Limit osób: 12</p></h2>", unsafe_allow_html=True)
        st.divider()
    with ship_column[2]:
        st.markdown(f"<h2 style=\"{title_style}\">Kormoran<p>Limit osób: 12</p></h2>", unsafe_allow_html=True)
        st.divider()
    with ship_column[3]:
        st.markdown(f"<h2 style=\"{title_style}\">CKT VIP<p>Limit osób: 12</p></h2>", unsafe_allow_html=True)
        st.divider()

    c.execute("SELECT * FROM rejs ORDER BY hour")

    #Dodawanie dancych do poszczególnych tablic
    for new_row in c.fetchall():
        dane = [f"Imię i nazwisko: {new_row[1]}", f"Numer telefonu: {new_row[6]}", f"{new_row[2]}", f"Statek: {new_row[3]}", f"{new_row[8]}" , new_row[7], f"osób\nZaliczka: {new_row[4]}", f"Kwota zaliczki: {new_row[9]} zł", f"Bilet opłacony: {new_row[5]}", f"Notatki: {new_row[10]}", new_row[0]]
        if new_row[3] == "Albatros":
            albatros.append(dane)
        if new_row[3] == "Biała Mewa":
            biala_mewa.append(dane)
        if new_row[3] == "Kormoran":
            kormoran.append(dane)
        if new_row[3] == "CKT VIP":
            ckt_vip.append(dane)

    #Wywołanie funkcji do usuwania "przterminowanych" rejsów
    albatros = removeExpiredCruises(albatros)
    biala_mewa = removeExpiredCruises(biala_mewa)
    kormoran = removeExpiredCruises(kormoran)
    ckt_vip = removeExpiredCruises(ckt_vip)

    #Wyświetlanie danych
    with ship_column[0]:
        for i, elem in enumerate(albatros):
            cruise_time = elem[2]
            cruise_name = elem[4]
            total_people = countPeopleOnCruise(albatros, cruise_name, cruise_time)
            total_people_markdown = st.markdown(f"<p style=\"{info_style}\">{elem[2]} - {timeCruise(elem).strftime('%H:%M')}<br>{elem[4]}<br>{total_people}<p>", unsafe_allow_html=True)
            if total_people > 60:
                st.warning("Przekroczono limit osób", icon="🚨")
            with st.expander("Szczegóły"):
                for a in elem:
                    st.write(a)
    with ship_column[1]:          
            for i, elem in enumerate(biala_mewa):
                cruise_time = elem[2]
                cruise_name = elem[4]
                total_people = countPeopleOnCruise(biala_mewa, cruise_name, cruise_time)
                total_people_markdown = st.markdown(f"<p style=\"{info_style}\">{elem[2]} - {timeCruise(elem).strftime('%H:%M')}<br>{elem[4]}<br>{total_people}<p>", unsafe_allow_html=True)
                if total_people > 12:
                    st.warning("Przekroczono limit osób", icon="🚨")
                with st.expander("Szczegóły"):
                    for a in elem:
                        st.write(a)
    with ship_column[2]:
        for i, elem in enumerate(kormoran):
                cruise_time = elem[2]
                cruise_name = elem[4]
                total_people = countPeopleOnCruise(kormoran, cruise_name, cruise_time)
                total_people_markdown = st.markdown(f"<p style=\"{info_style}\">{elem[2]} - {timeCruise(elem).strftime('%H:%M')}<br>{elem[4]}<br>{total_people}<p>", unsafe_allow_html=True)
                if total_people > 12:
                    st.warning("Przekroczono limit osób", icon="🚨")
                with st.expander("Szczegóły"):
                    for a in elem:
                        st.write(a)
    with ship_column[3]:
        for i, elem in enumerate(ckt_vip):
                cruise_time = elem[2]
                cruise_name = elem[4]
                total_people = countPeopleOnCruise(ckt_vip, cruise_name, cruise_time)
                total_people_markdown = st.markdown(f"<p style=\"{info_style}\">{elem[2]} - {timeCruise(elem).strftime('%H:%M')}<br>{elem[4]}<br>{total_people}<p>", unsafe_allow_html=True)
                if total_people > 12:
                    st.warning("Przekroczono limit osób", icon="🚨")
                with st.expander("Szczegóły"):
                    for a in elem:
                        st.write(a)

    conn.close()

#Rezerwacje
if (selected == "Rezerwacje"):
    albatros_rez = []
    biala_mewa_rez = []
    kormoran_rez = []
    ckt_vip_rez = []
    
    conn_rez = sqlite3.connect('statki.db')
    cr = conn_rez.cursor()

    cr.execute('''CREATE TABLE IF NOT EXISTS rezerwacje (id INTEGER PRIMARY KEY, customer_rez TEXT, date DATE, hour_rez TIME, ship_rez TEXT, fee_rez INTEGER, people_rez INTEGER, nb_rez DECIMAL, cruise_rez TEXT, fee_cost_rez INTEGER, catering TEXT, note_rez TEXT)''')

    st.title("Dodaj rezerwację :anchor:")
    
    def countPeopleOnCruise_rez(ship_data, cruise_name, cruise_time, cruise_date):
        total_people_rez = 0
        for cruise_data in ship_data:
            if cruise_data[2] == cruise_time and cruise_data[4] == cruise_name and cruise_data[2] == cruise_date:
                total_people_rez = total_people_rez + cruise_data[5]
        return total_people_rez
    
    #Dodaj rezerwację
    with st.expander("Dodaj nową rezerwację"):
        columns_rez = st.columns([1,1])
        with columns_rez[0]:
            customer_rez = st.text_input("Podaj imię i nazwisko")
            date = st.date_input("Podaj dzień", value="today", format="DD.MM.YYYY", label_visibility="visible")
            ship_rez = st.selectbox("Wybierz statek", ["Albatros", "Biała Mewa", "Kormoran", "CKT VIP"])
            fee_rez = st.selectbox("Zaliczka", ["Tak", "Nie"])
            people_rez = st.number_input("Ilość osób", step=1, max_value=60, min_value=0)
        
        with columns_rez[1]:
            nb_rez = st.text_input("Podaj numer telefonu")
            hour_rez = st.time_input("Podaj godzinę")
            cruise_rez = st.selectbox("Wybierz rejs", ["Po rzekach i jeziorach - 1h", "Fotel Papieski - 1h", "Kanał Augustowski - 1h", "Dolina Rospudy - 1,5h", "Szlakiem Papieskim - 3h", "Staw Swoboda - 4h", "Gorczyca - „Pełen Szlak Papieski” – 6h", "Paniewo"])
            fee_cost_rez = st.number_input("Kwotwa zaliczki")
            catering = st.selectbox("Katering", ["Tak", "Nie"])
            
        note_rez = st.text_area("Notatki")
        add_button_rez = st.button("Dodaj rezerwację")
        
        if add_button_rez:
            if (customer_rez != "" and nb_rez != ""):
                hour_str_rez = hour_rez.strftime("%H:%M")
                
                #Zapis w bazie danych
                cr.execute("INSERT INTO rezerwacje (customer_rez, date, hour_rez, ship_rez, fee_rez, people_rez, nb_rez, cruise_rez, fee_cost_rez, catering, note_rez) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                        (customer_rez, date, hour_str_rez, ship_rez, fee_rez, people_rez, nb_rez, cruise_rez, fee_cost_rez, catering, note_rez))
                conn_rez.commit()
                st.warning("Dane zostały dodane pomyślnie", icon="🆗")
            else:
                st.warning("Wprowadź dane", icon="🚨")

    st.divider()
    
    #Kolumny dla danych statków
    scr = st.columns([1,1,1,1])
    with scr[0]:
        st.markdown(f"<h2 style=\"{title_style}\">Albatros<p>Limit osób: 60</p></h2>", unsafe_allow_html=True)
        st.divider()
    with scr[1]:
        st.markdown(f"<h2 style=\"{title_style}\">Biała Mewa<p>Limit osób: 12</p></h2>", unsafe_allow_html=True)
        st.divider()
    with scr[2]:
        st.markdown(f"<h2 style=\"{title_style}\">Kormoran<p>Limit osób: 12</p></h2>", unsafe_allow_html=True)
        st.divider()
    with scr[3]:
        st.markdown(f"<h2 style=\"{title_style}\">CKT VIP<p>Limit osób: 12</p></h2>", unsafe_allow_html=True)
        st.divider()
    
    cr.execute("SELECT * FROM rezerwacje ORDER BY hour_rez")

    #Przypisanie danych do odpowiednich tablic
    for rowrez in cr.fetchall():
        dane_rez = [f"Imię i nazwisko: {rowrez[1]}", f"Numer telefonu: {rowrez[7]}", f"Data: {rowrez[2]}", {rowrez[3]}, f"Rejs: {rowrez[8]}", {rowrez[6]}, f"Zaliczka: {rowrez[5]}", f"Kwota zaliczki: {rowrez[9]}", f"Katering: {rowrez[10]}", f"Notatki: {rowrez[11]}"]
        if rowrez[4] == "Albatros":
            albatros_rez.append(dane)
        if rowrez[4] == "Biała Mewa":
            biala_mewa_rez.append(dane)
        if rowrez[4] == "Kormoran":
            kormoran_rez.append(dane)
        if rowrez[4] == "CKT VIP":
            ckt_vip_rez.append(dane)
    
    #Wyświetlanie danych    
    with scr[0]:
        for i, elem in enumerate(albatros_rez):
            cruise_time_rez = elem[2]
            cruise_name_rez = elem[4]
            cruise_date = elem[2]
            total_people_rez = countPeopleOnCruise_rez(albatros_rez, cruise_name_rez, cruise_time_rez)
            st.markdown(f"<p style=\"{info_style}\">{elem[2]} - {timeCruise(elem).strftime('%H:%M')}<br>{elem[4]}<br>{total_people_rez}<p>", unsafe_allow_html=True)
            with st.expander("Szczegóły"):
                for a in elem:
                    st.write(a)
    with scr[1]:          
            for i, elem in enumerate(biala_mewa_rez):
                cruise_time_rez = elem[2]
                cruise_name_rez = elem[4]
                cruise_date = elem[2]
                total_people_rez = countPeopleOnCruise_rez(albatros_rez, cruise_name_rez, cruise_time_rez)
                st.markdown(f"<p style=\"{info_style}\">{elem[2]} - {timeCruise(elem).strftime('%H:%M')}<br>{elem[4]}<br>{total_people_rez}<p>", unsafe_allow_html=True)
                with st.expander("Szczegóły"):
                    for a in elem:
                        st.write(a)
    with scr[2]:
        for i, elem in enumerate(kormoran_rez):
                cruise_time_rez = elem[2]
                cruise_name_rez = elem[4]
                cruise_date = elem[2]
                total_people_rez = countPeopleOnCruise_rez(albatros_rez, cruise_name_rez, cruise_time_rez)
                st.markdown(f"<p style=\"{info_style}\">{elem[2]} - {timeCruise(elem).strftime('%H:%M')}<br>{elem[4]}<br>{total_people_rez}<p>", unsafe_allow_html=True)
                with st.expander("Szczegóły"):
                    for a in elem:
                        st.write(a)
    with scr[3]:
        for i, elem in enumerate(ckt_vip_rez):
                cruise_time_rez = elem[2]
                cruise_name_rez = elem[4]
                cruise_date = elem[2]
                total_people_rez = countPeopleOnCruise_rez(albatros_rez, cruise_name_rez, cruise_time_rez)
                st.markdown(f"<p style=\"{info_style}\">{elem[2]} - {timeCruise(elem).strftime('%H:%M')}<br>{elem[4]}<br>{total_people_rez}<p>", unsafe_allow_html=True)
                with st.expander("Szczegóły"):
                    for a in elem:
                        st.write(a)
        
    conn_rez.close()   
