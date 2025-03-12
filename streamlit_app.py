import streamlit as st
import pandas as pd
from PIL import Image
import json
import numpy as np
import hmac
import base64
import matplotlib.pyplot as plt

def check_password():
    """Returns True if the user had the correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if hmac.compare_digest(st.session_state["password"], st.secrets["password"]):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Don't store the password.
        else:
            st.session_state["password_correct"] = False

    # Return True if the password is validated.
    if st.session_state.get("password_correct", False):
        return True

    # Show input for password.
    st.text_input(
        "Passwort", type="password", on_change=password_entered, key="password"
    )
    if "password_correct" in st.session_state:
        st.error("Passwort falsch test")
    return False

if not check_password():
    st.stop()  # Do not continue if check_password is not True.

st.set_page_config(layout='wide', initial_sidebar_state='expanded')

st.markdown(
    """
    <style>
    /* Set the background color of the main content area */
    div[data-testid="stAppViewContainer"] {
        background-color: #d6e8ee;
        background-image: none;
    }
    /* Set the background color of the sidebar */
    div[data-testid="stSidebar"] > div:first-child {
        background-color: #f0f2f6;
    }
    /* Set the background color of the header */
    header[data-testid="stHeader"] {
        background-color: #d6e8ee;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <style>
    /* Change the background of the header and the surrounding area */
    header, .css-18ni7ap {
        background-color: #d6e8ee !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

custom_metric_html = """
    <div style="background-color: #F0F8FF;
                border: 1px solid #CCCCCC;
                padding: 20px;
                border-radius: 15px;
                border-left: 0.5rem solid yellow;  /* Added yellow line */
                margin-bottom: 10px;
                width: 100%;
                box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
                overflow-wrap: break-word;">
        <div style="padding-left: 10px;">
            <div style="font-weight: bold; color: #41528b; font-size: 16px;">
                {label}
            </div>
            <div style="font-size: 36px; font-weight: bold; color: #41528b;">
                {value}
            </div>
        </div>
    </div>
"""

# Functions
def format_german(value):
    v1 = f'{value:,.2f} €'
    v2 = v1.replace(',','#')
    v3 = v2.replace('.','%')
    v4 = v3.replace('#','.')
    v5 = v4.replace('%',',')
    return v5

# Formatter function for the y-axis
def euro_formatter(value):
    return f'€ {value:,.0f}'.replace(',', '.').replace('.', ',')

st.sidebar.header('Vergleichsrechner Einmaleinlage version 1')

uploaded_file = st.sidebar.file_uploader("Parameter Hochladen", type=["json"])
if uploaded_file:
    # Reading the uploaded JSON file
    uploaded_data = json.load(uploaded_file)
    # Load Umschichtungen into session_state
    st.session_state['umschichtungen'] = uploaded_data.get('umschichtungen', [])
else:
    if 'umschichtungen' not in st.session_state:
        st.session_state['umschichtungen'] = []

# Eingabe Fondspolice
st.sidebar.markdown('Fondspolice')
if uploaded_file:
    col1, col2 = st.sidebar.columns(2)
    with col1:
        einmalbeitrag_police = st.number_input('Einmalbeitrag',min_value=0,value=uploaded_data.get('einmalbeitrag_police'))
        rendite_mischfonds_police = (st.number_input('Rendite Mischfonds(%)',min_value=0.0,value=uploaded_data.get('rendite_mischfonds_police'))/100)
        rendite_rentenfonds_police = (st.number_input('Rendite Rentenfonds(%)',min_value=0.0,value=uploaded_data.get('rendite_rentenfonds_police'))/100)
        rendite_aktienfonds_police = (st.number_input('Rendite Aktienfonds(%)',min_value=0.0,value=uploaded_data.get('rendite_aktienfonds_police'))/100)
    with col2:
        teilfreistellung_police = (st.number_input('Teilfreistellung(%)',min_value=0.0,value=uploaded_data.get('teilfreistellung_police'))/100)
        effektivkosten_police = (st.number_input('Effektivkosten pro Jahr(%)',min_value=0.0,value=uploaded_data.get('effektivkosten_police'))/100)
        steuersatz_police = (st.number_input('Persönl. Steuersatz bei Auszahlung(%)',min_value=0.0,value=uploaded_data.get('steuersatz_police'))/100)


else:
    col1, col2 = st.sidebar.columns(2)
    with col1:
        einmalbeitrag_police = st.number_input('Einmalbeitrag',min_value=0,value=10000)
        rendite_mischfonds_police = (st.number_input('Rendite Mischfonds(%)',min_value=0.0,value=8.0)/100)
        rendite_rentenfonds_police = (st.number_input('Rendite Rentenfonds(%)',min_value=0.0,value=8.0)/100)
        rendite_aktienfonds_police = (st.number_input('Rendite Aktienfonds(%)',min_value=0.0,value=8.0)/100)
    with col2:
        teilfreistellung_police = (st.number_input('Teilfreistellung(%)',min_value=0.0,value=15.00)/100)
        effektivkosten_police = (st.number_input('Effektivkosten pro Jahr(%)',min_value=0.0,value=1.00)/100)
        steuersatz_police = (st.number_input('Persönl. Steuersatz bei Auszahlung(%)',min_value=0.0,value=42.0)/100)


# Eingabe Fondssparplan
st.sidebar.markdown('Fondssparplan')
if uploaded_file:
    col1, col2 = st.sidebar.columns(2)
    with col1:
        einmalbeitrag_sparplan = st.number_input('Einmalbeitrag ',min_value=0,value=uploaded_data.get('einmalbeitrag_sparplan'))
        rendite_aktienfonds_sparplan = (st.number_input('Rendite Aktienfonds(%) ',min_value=0.0,value=uploaded_data.get('rendite_aktienfonds_sparplan'))/100)
        rendite_mischfonds_sparplan = (st.number_input('Rendite Mischfonds(%) ',min_value=0.0,value=uploaded_data.get('rendite_mischfonds_sparplan'))/100)
        rendite_rentenfonds_sparplan = (st.number_input('Rendite Rentenfonds(%) ',min_value=0.0,value=uploaded_data.get('rendite_rentenfonds_sparplan'))/100)
        freistellungsauftrag_sparplan = st.number_input('Freistellungsauftrag ',min_value=0,value=uploaded_data.get('freistellungsauftrag_sparplan'))
    with col2:
        teilfreistellung_aktienfonds_sparplan = (st.number_input('Teilfreistellung Aktienfonds(%) ',min_value=0.0,value=uploaded_data.get('teilfreistellung_aktienfonds_sparplan'))/100)
        teilfreistellung_mischfonds_sparplan = (st.number_input('Teilfreistellung Mischfonds(%)',min_value=0.0,value=uploaded_data.get('teilfreistellung_mischfonds_sparplan'))/100)
        teilfreistellung_rentenfonds_sparplan = (st.number_input('Teilfreistellung Rentenfonds(%) ',min_value=0.0,value=uploaded_data.get('teilfreistellung_rentenfonds_sparplan'))/100)
        basiszins_sparplan = (st.number_input('Basiszins(%) ',min_value=0.0,value=uploaded_data.get('basiszins_sparplan'))/100)

        effektivkosten_sparplan = (st.number_input('Effektivkosten pro Jahr(%) ',min_value=0.0,value=uploaded_data.get('effektivkosten_sparplan'))/100)
        ausgabeaufschlag_sparplan = (st.number_input('Ausgabeaufschlag auf Wiederanlage(%) ',min_value=0.0,value=uploaded_data.get('ausgabeaufschlag_sparplan'))/100)
        steuerlast_sparplan = (st.number_input('Steuerlast(%) ',min_value=0.0,value=uploaded_data.get('steuerlast_sparplan'))/100)
        steuerlast_auszahlung_sparplan = (st.number_input('Steuerlast bei Auszahlung(%) ',min_value=0.0,value=uploaded_data.get('steuerlast_auszahlung_sparplan'))/100)
else:
    col1, col2 = st.sidebar.columns(2)
    with col1:
        einmalbeitrag_sparplan = st.number_input('Einmalbeitrag ',min_value=0,value=10000)
        rendite_aktienfonds_sparplan = (st.number_input('Rendite Aktienfonds(%) ',min_value=0.0,value=0.0)/100)
        rendite_mischfonds_sparplan = (st.number_input('Rendite Mischfonds(%) ',min_value=0.0,value=0.0)/100)
        rendite_rentenfonds_sparplan = (st.number_input('Rendite Rentenfonds(%) ',min_value=0.0,value=0.0)/100)
        freistellungsauftrag_sparplan = st.number_input('Freistellungsauftrag ',min_value=0,value=0)
    with col2:
        teilfreistellung_aktienfonds_sparplan = (st.number_input('Teilfreistellung Aktienfonds(%) ',min_value=0.0,value=0.0)/100)
        teilfreistellung_mischfonds_sparplan = (st.number_input('Teilfreistellung Mischfonds(%) ',min_value=0.0,value=0.0)/100)
        teilfreistellung_rentenfonds_sparplan = (st.number_input('Teilfreistellung Rentenfonds(%) ',min_value=0.0,value=0.0)/100)
        basiszins_sparplan = (st.number_input('Basiszins(%) ',min_value=0.0,value=0.0)/100)

        effektivkosten_sparplan = (st.number_input('Effektivkosten pro Jahr(%) ',min_value=0.0,value=0.0)/100)
        ausgabeaufschlag_sparplan = (st.number_input('Ausgabeaufschlag auf Wiederanlage(%) ',min_value=0.0,value=0.0)/100)
        steuerlast_sparplan = (st.number_input('Steuerlast(%) ',min_value=0.0,value=0.0)/100)
        steuerlast_auszahlung_sparplan = (st.number_input('Steuerlast bei Auszahlung(%) ',min_value=0.0,value=0.0)/100)



st.sidebar.subheader('Weitere Parameter')
col1, col2 = st.sidebar.columns(2)
with col1:
    if uploaded_file:
        laufzeit = st.number_input('Laufzeit',min_value=0,value=uploaded_data.get('laufzeit'))-1
    else:
        laufzeit = st.number_input('Laufzeit',min_value=0,value=1)-1

# Umschichtungen Section

if 'umschichtungen' not in st.session_state:
    st.session_state['umschichtungen'] = []

st.sidebar.subheader('Umschichtungen')

options = list(range(1, laufzeit+2))
jahr_der_umschichtung = st.sidebar.selectbox('Jahr der Umschichtung', options=options, index=0)
anteil_umschichtung_input = st.sidebar.number_input('Anteil Umschichtung(%)', min_value=0.0, max_value=100.0, value=0.0)
anteil_umschichtung = anteil_umschichtung_input / 100

if st.sidebar.button('Speichern'):
    # Append the Umschichtung to the list
    st.session_state['umschichtungen'].append({'jahr': jahr_der_umschichtung - 1, 'anteil': anteil_umschichtung})
    # Optionally reset the input fields
    st.session_state['jahr_der_umschichtung'] = options[0]
    st.session_state['anteil_umschichtung_input'] = 0.0

if st.sidebar.button('Umschichtungen löschen'):
    st.session_state['umschichtungen'] = []


if st.sidebar.button('Alle Umschichtungen löschen'):
    st.session_state['umschichtungen'] = []

# Display the list of Umschichtungen
if st.session_state['umschichtungen']:
    st.sidebar.write('Umschichtungen:')
    for idx, ums in enumerate(st.session_state['umschichtungen']):
        st.sidebar.write(f"Umschichtung {idx+1}: Jahr {ums['jahr']+1}, Anteil {ums['anteil']*100}%")
        # Add a button to delete each Umschichtung
        if st.sidebar.button(f'Umschichtung löschen', key=f'delete_{idx}'):
            st.session_state['umschichtungen'].pop(idx)
            # Since the list has changed, we need to break to avoid issues
            break

#Umschichtungen police
def create_rollover_dataframe_police(laufzeit, ums_list):
    # Create a dataframe with "years" number of rows
    df_police = pd.DataFrame({'Jahr': range(0, laufzeit+1)})

    # Initialize the rollover columns
    df_police['UmschichtungJN'] = 0
    df_police['AnteilUmschichtung'] = 0.0

    # Set UmschichtungJN and AnteilUmschichtung based on ums_list
    for ums in ums_list:
        jahr = ums['jahr']
        anteil = ums['anteil']
        if 0 <= jahr <= laufzeit:
            df_police.loc[df_police['Jahr'] == jahr, 'UmschichtungJN'] = 1
            df_police.loc[df_police['Jahr'] == jahr, 'AnteilUmschichtung'] = anteil

    return df_police

def create_rollover_dataframe_depot(laufzeit, ums_list):
    # Create a dataframe with "years" number of rows
    df_depot = pd.DataFrame({'Jahr': range(0, laufzeit+1)})

    # Initialize the rollover columns
    df_depot['UmschichtungJN'] = 0
    df_depot['AnteilUmschichtung'] = 0.0

    # Set UmschichtungJN and AnteilUmschichtung based on ums_list
    for ums in ums_list:
        jahr = ums['jahr']
        anteil = ums['anteil']
        if 0 <= jahr <= laufzeit:
            df_depot.loc[df_depot['Jahr'] == jahr, 'UmschichtungJN'] = 1
            df_depot.loc[df_depot['Jahr'] == jahr, 'AnteilUmschichtung'] = anteil

    return df_depot


#POLICE TABELLE
df_police = create_rollover_dataframe_police(laufzeit, st.session_state['umschichtungen'])

df_police['Jahresbeginn'] = 0
df_police['Nach Beitragskosten und Abschlusskosten'] = 0
df_police['Rendite'] = 0
df_police['Wertsteigerung'] = 0
df_police['Jahresende'] = 0
df_police['Kosten Fondsguthaben'] = 0
df_police['Jahresende nach Kosten'] = 0
df_police['Einzahlung'] = 0
df_police['Umschichtung'] = 0
df_police['Umschichten oder Auszahlen'] = 0
df_police['Einzahlungen'] = 0
df_police['Erträge'] = 0
df_police['Teilfreistellung'] = 0
df_police['zu besteuern'] = 0
df_police['HEV'] = 0
df_police['Steuerlast'] = 0

for i in range (laufzeit+1):
    if i == 0:
        df_police.loc[i, 'Jahr'] = i+1 #A
        df_police.loc[i, 'Jahresbeginn'] = einmalbeitrag_police #B
        df_police.loc[i, 'Nach Beitragskosten und Abschlusskosten'] = df_police.loc[i,'Jahresbeginn'] #DELETE? #D
        df_police.loc[i, 'Rendite'] = rendite_aktienfonds_police #E
        df_police.loc[i, 'Wertsteigerung'] = df_police.loc[i,'Nach Beitragskosten und Abschlusskosten']*df_police.loc[i,'Rendite'] #F
        df_police.loc[i, 'Jahresende'] = df_police.loc[i,'Nach Beitragskosten und Abschlusskosten']+df_police.loc[i,'Wertsteigerung'] #G
        df_police.loc[i, 'Kosten Fondsguthaben'] = df_police.loc[i,'Jahresende']*effektivkosten_police #J
        df_police.loc[i, 'Jahresende nach Kosten'] = df_police.loc[i,'Jahresende']-df_police.loc[i,'Kosten Fondsguthaben'] #K
        df_police.loc[i, 'Einzahlung'] = einmalbeitrag_police #L
        df_police.loc[i, 'Umschichtung'] = df_police.loc[i, 'UmschichtungJN']*df_police.loc[i, 'AnteilUmschichtung'] #M
        df_police.loc[i, 'Umschichten oder Auszahlen'] = df_police.loc[i, 'Jahresende nach Kosten']*df_police.loc[i, 'Umschichtung'] #N
    elif i == laufzeit:
        df_police.loc[i, 'Jahr'] = i+1 #A
        df_police.loc[i,'Jahresbeginn'] = df_police.loc[i-1, 'Jahresende nach Kosten'] #B
        df_police.loc[i,'Nach Beitragskosten und Abschlusskosten'] = df_police.loc[i,'Jahresbeginn'] #DELETE? #D
        df_police.loc[i, 'Rendite'] = rendite_aktienfonds_police #E
        df_police.loc[i, 'Wertsteigerung'] = df_police.loc[i,'Nach Beitragskosten und Abschlusskosten']*df_police.loc[i,'Rendite'] #F
        df_police.loc[i, 'Jahresende'] = df_police.loc[i,'Nach Beitragskosten und Abschlusskosten']+df_police.loc[i,'Wertsteigerung'] #G
        df_police.loc[i, 'Kosten Fondsguthaben'] = df_police.loc[i,'Jahresende']*effektivkosten_police #J
        df_police.loc[i, 'Jahresende nach Kosten'] = df_police.loc[i,'Jahresende']-df_police.loc[i,'Kosten Fondsguthaben'] #K
        df_police.loc[i, 'Einzahlung'] = 0 #L
        df_police.loc[i, 'Umschichtung'] = df_police.loc[i, 'UmschichtungJN']*df_police.loc[i, 'AnteilUmschichtung'] #M
        df_police.loc[i, 'Umschichten oder Auszahlen'] = df_police.loc[i, 'Jahresende nach Kosten']*df_police.loc[i, 'Umschichtung'] #N
        df_police.loc[i, 'Einzahlungen'] = einmalbeitrag_police
        df_police.loc[i, 'Erträge'] = df_police.loc[i, 'Umschichten oder Auszahlen'] - df_police.loc[i, 'Einzahlungen']
        df_police.loc[i, 'Teilfreistellung'] = df_police.loc[i, 'Erträge']*teilfreistellung_police
        df_police.loc[i, 'zu besteuern'] = df_police.loc[i, 'Erträge']-df_police.loc[i, 'Teilfreistellung']
        df_police.loc[i, 'HEV'] = df_police.loc[i, 'zu besteuern']/2
        df_police.loc[i, 'Steuerlast'] = df_police.loc[i, 'HEV']*steuersatz_police
    else:
        df_police.loc[i, 'Jahr'] = i+1 #A
        df_police.loc[i,'Jahresbeginn'] = df_police.loc[i-1, 'Jahresende nach Kosten'] #B
        df_police.loc[i,'Nach Beitragskosten und Abschlusskosten'] = df_police.loc[i,'Jahresbeginn'] #DELETE? #D
        df_police.loc[i, 'Rendite'] = rendite_aktienfonds_police #E
        df_police.loc[i, 'Wertsteigerung'] = df_police.loc[i,'Nach Beitragskosten und Abschlusskosten']*df_police.loc[i,'Rendite'] #F
        df_police.loc[i, 'Jahresende'] = df_police.loc[i,'Nach Beitragskosten und Abschlusskosten']+df_police.loc[i,'Wertsteigerung'] #G
        df_police.loc[i, 'Kosten Fondsguthaben'] = df_police.loc[i,'Jahresende']*effektivkosten_police #J
        df_police.loc[i, 'Jahresende nach Kosten'] = df_police.loc[i,'Jahresende']-df_police.loc[i,'Kosten Fondsguthaben'] #K
        df_police.loc[i, 'Einzahlung'] = 0 #L
        df_police.loc[i, 'Umschichtung'] = df_police.loc[i, 'UmschichtungJN']*df_police.loc[i, 'AnteilUmschichtung'] #M
        df_police.loc[i, 'Umschichten oder Auszahlen'] = df_police.loc[i, 'Jahresende nach Kosten']*df_police.loc[i, 'Umschichtung'] #N

#DEPOT TABELLE
df_depot = create_rollover_dataframe_depot(laufzeit, st.session_state['umschichtungen'])

df_depot['Jahresbeginn'] = 0
df_depot['Nach Orderprov. und Ausgabeaufschl.'] = 0
df_depot['Rendite'] = 0
df_depot['Wertsteigerung'] = 0
df_depot['Wertsteigerunglaufend'] = 0
df_depot['Jahresende'] = 0
df_depot['Kosten auf Fondsguthaben'] = 0
df_depot['Jahresende nach Kosten'] = 0
df_depot['Basisertrag'] = 0
df_depot['Vorabpauschale'] = 0
df_depot['Vorabpauschalelaufend'] = 0
df_depot['Teilfreistellung'] = 0
df_depot['zu besteuern'] = 0
df_depot['Freistellungsauftrag'] = 0
df_depot['Freistellung übrig'] = 0
df_depot['danach zu besteuern'] = 0
df_depot['Steuerlast'] = 0
df_depot['Einzahlung'] = 0
df_depot['Umschichtung'] = 0
df_depot['Umschichten'] = 0
df_depot['Erträgelaufend'] = 0
df_depot['Erträge'] = 0
df_depot['minus Vorabpauschale'] = 0
df_depot['Teilfreistellung '] = 0
df_depot['zu besteuern '] = 0
df_depot['nach Freistellungsauftrag'] = 0
df_depot['Steuerlast '] = 0
df_depot['Kapital abzüglich Steuer'] = 0

for i in range(laufzeit + 1):
    if i == 0:
        df_depot.loc[i, 'Jahr'] = i + 1  # A
        df_depot.loc[i, 'Jahresbeginn'] = einmalbeitrag_sparplan  # B
        df_depot.loc[i, 'Nach Orderprov. und Ausgabeaufschl.'] = df_depot.loc[i, 'Jahresbeginn']  # E
        df_depot.loc[i, 'Rendite'] = rendite_aktienfonds_sparplan  # F
        df_depot.loc[i, 'Wertsteigerung'] = df_depot.loc[i, 'Jahresbeginn'] * rendite_aktienfonds_sparplan  # G
        df_depot.loc[i, 'Jahresende'] = df_depot.loc[i, 'Nach Orderprov. und Ausgabeaufschl.'] + df_depot.loc[i, 'Wertsteigerung']  # H
        df_depot.loc[i, 'Kosten auf Fondsguthaben'] = df_depot.loc[i, 'Jahresende'] * effektivkosten_sparplan  # K
        df_depot.loc[i, 'Basisertrag'] = df_depot.loc[i, 'Nach Orderprov. und Ausgabeaufschl.'] * 0.7 * basiszins_sparplan  # M
        # Calculation for Vorabpauschale and subsequent steps...
        if (df_depot.loc[i, 'Jahresende'] - df_depot.loc[i, 'Nach Orderprov. und Ausgabeaufschl.']) <= df_depot.loc[i, 'Basisertrag'] and \
                (df_depot.loc[i, 'Jahresende'] - df_depot.loc[i, 'Nach Orderprov. und Ausgabeaufschl.']) >= 0:
            df_depot.loc[i, 'Vorabpauschale'] = 0  # N
        else:
            df_depot.loc[i, 'Vorabpauschale'] = df_depot.loc[i, 'Basisertrag']  # N
        df_depot.loc[i, 'Vorabpauschalelaufend'] = df_depot.loc[i, 'Vorabpauschale']
        df_depot.loc[i, 'Teilfreistellung'] = df_depot.loc[i, 'Vorabpauschale'] * teilfreistellung_aktienfonds_sparplan  # O
        df_depot.loc[i, 'zu besteuern'] = df_depot.loc[i, 'Vorabpauschale'] - df_depot.loc[i, 'Teilfreistellung']  # P
        df_depot.loc[i, 'Freistellungsauftrag'] = freistellungsauftrag_sparplan  # R
        if df_depot.loc[i, 'zu besteuern'] >= df_depot.loc[i, 'Freistellungsauftrag']:
            df_depot.loc[i, 'Freistellung übrig'] = 0
        else:
            df_depot.loc[i, 'Freistellung übrig'] = df_depot.loc[i, 'Freistellungsauftrag'] - df_depot.loc[i, 'zu besteuern']  # S
        if df_depot.loc[i, 'Freistellungsauftrag'] >= df_depot.loc[i, 'zu besteuern']:
            df_depot.loc[i, 'danach zu besteuern'] = 0  # T
        else:
            df_depot.loc[i, 'danach zu besteuern'] = df_depot.loc[i, 'zu besteuern'] - df_depot.loc[i, 'Freistellungsauftrag']  # T
        df_depot.loc[i, 'Steuerlast'] = df_depot.loc[i, 'danach zu besteuern'] * steuerlast_sparplan  # U
        df_depot.loc[i, 'Jahresende nach Kosten'] = df_depot.loc[i, 'Jahresende'] - df_depot.loc[i, 'Kosten auf Fondsguthaben'] - df_depot.loc[i, 'Steuerlast']  # L
        df_depot.loc[i, 'Einzahlung'] = einmalbeitrag_sparplan  # V
        # For the Umschichtung in the first year: if the entire period is just one year, enforce fixed reallocation.
        if laufzeit == 0:
            df_depot.loc[i, 'Umschichtung'] = 1
            df_depot.loc[i, 'Umschichten'] = df_depot.loc[i, 'Jahresende nach Kosten']
        else:
            df_depot.loc[i, 'Umschichtung'] = df_depot.loc[i, 'UmschichtungJN'] * df_depot.loc[i, 'AnteilUmschichtung']  # W
            df_depot.loc[i, 'Umschichten'] = df_depot.loc[i, 'Jahresende nach Kosten'] * df_depot.loc[i, 'Umschichtung']  # X
        # Continue with remaining calculations...
        df_depot.loc[i, 'Erträgelaufend'] = df_depot.loc[i, 'Wertsteigerung']
        df_depot.loc[i, 'Erträge'] = df_depot.loc[i, 'Erträgelaufend'] * df_depot.loc[i, 'UmschichtungJN']  # Z
        df_depot.loc[i, 'minus Vorabpauschale'] = (df_depot.loc[i, 'Erträgelaufend'] - df_depot.loc[i, 'Vorabpauschalelaufend']) * df_depot.loc[i, 'UmschichtungJN']  # AA
        df_depot.loc[i, 'Teilfreistellung '] = df_depot.loc[i, 'minus Vorabpauschale'] * teilfreistellung_aktienfonds_sparplan  # AB
        df_depot.loc[i, 'zu besteuern '] = df_depot.loc[i, 'minus Vorabpauschale'] - df_depot.loc[i, 'Teilfreistellung ']  # AC

        if df_depot.loc[i, 'Freistellung übrig'] > df_depot.loc[i, 'zu besteuern ']:
            df_depot.loc[i, 'nach Freistellungsauftrag'] = 0  # AD
        else:
            df_depot.loc[i, 'nach Freistellungsauftrag'] = df_depot.loc[i, 'zu besteuern '] - df_depot.loc[i, 'Freistellung übrig']  # AD

        df_depot.loc[i, 'Steuerlast '] = df_depot.loc[i, 'nach Freistellungsauftrag'] * steuerlast_sparplan  # AE
        df_depot.loc[i, 'Kapital abzüglich Steuer'] = df_depot.loc[i, 'Umschichten'] - df_depot.loc[i, 'Steuerlast ']  # AF

    else:
        df_depot.loc[i, 'Jahr'] = i + 1  # A
        df_depot.loc[i, 'Jahresbeginn'] = df_depot.loc[i - 1, 'Jahresende nach Kosten'] - df_depot.loc[i - 1, 'Steuerlast ']  # B
        df_depot.loc[i, 'Nach Orderprov. und Ausgabeaufschl.'] = df_depot.loc[i, 'Jahresbeginn']  # E
        df_depot.loc[i, 'Rendite'] = rendite_aktienfonds_sparplan  # F
        df_depot.loc[i, 'Wertsteigerung'] = df_depot.loc[i, 'Jahresbeginn'] * rendite_aktienfonds_sparplan  # G
        df_depot.loc[i, 'Jahresende'] = df_depot.loc[i, 'Jahresbeginn'] + df_depot.loc[i, 'Wertsteigerung']  # H
        df_depot.loc[i, 'Kosten auf Fondsguthaben'] = df_depot.loc[i, 'Jahresende'] * effektivkosten_sparplan  # K
        df_depot.loc[i, 'Basisertrag'] = df_depot.loc[i, 'Nach Orderprov. und Ausgabeaufschl.'] * 0.7 * basiszins_sparplan  # M
        if (df_depot.loc[i, 'Jahresende'] - df_depot.loc[i, 'Nach Orderprov. und Ausgabeaufschl.']) <= df_depot.loc[i, 'Basisertrag'] and \
                (df_depot.loc[i, 'Jahresende'] - df_depot.loc[i, 'Nach Orderprov. und Ausgabeaufschl.']) >= 0:
            df_depot.loc[i, 'Vorabpauschale'] = 0  # N
        else:
            df_depot.loc[i, 'Vorabpauschale'] = df_depot.loc[i, 'Basisertrag']  # N
        # Update the running sum of Vorabpauschale:
        if df_depot.loc[i - 1, 'UmschichtungJN'] == 1:
            df_depot.loc[i, 'Vorabpauschalelaufend'] = df_depot.loc[i, 'Vorabpauschale']
        else:
            df_depot.loc[i, 'Vorabpauschalelaufend'] = df_depot.loc[i - 1, 'Vorabpauschalelaufend'] + df_depot.loc[i, 'Vorabpauschale']
        df_depot.loc[i, 'Teilfreistellung'] = df_depot.loc[i, 'Vorabpauschale'] * teilfreistellung_aktienfonds_sparplan  # O
        df_depot.loc[i, 'zu besteuern'] = df_depot.loc[i, 'Vorabpauschale'] - df_depot.loc[i, 'Teilfreistellung']  # P
        df_depot.loc[i, 'Freistellungsauftrag'] = freistellungsauftrag_sparplan  # R
        if df_depot.loc[i, 'zu besteuern'] >= df_depot.loc[i, 'Freistellungsauftrag']:
            df_depot.loc[i, 'Freistellung übrig'] = 0
        else:
            df_depot.loc[i, 'Freistellung übrig'] = df_depot.loc[i, 'Freistellungsauftrag'] - df_depot.loc[i, 'zu besteuern']  # S
        if df_depot.loc[i, 'Freistellungsauftrag'] >= df_depot.loc[i, 'zu besteuern']:
            df_depot.loc[i, 'danach zu besteuern'] = 0  # T
        else:
            df_depot.loc[i, 'danach zu besteuern'] = df_depot.loc[i, 'zu besteuern'] - df_depot.loc[i, 'Freistellungsauftrag']  # T
        df_depot.loc[i, 'Steuerlast'] = df_depot.loc[i, 'danach zu besteuern'] * steuerlast_sparplan  # U
        df_depot.loc[i, 'Jahresende nach Kosten'] = df_depot.loc[i, 'Jahresende'] - df_depot.loc[i, 'Kosten auf Fondsguthaben'] - df_depot.loc[i, 'Steuerlast']  # L
        df_depot.loc[i, 'Einzahlung'] = 0  # V

        # For Umschichtung: force a fixed 100% reallocation in the last year
        if i == laufzeit:
            df_depot.loc[i, 'Umschichtung'] = 1
            df_depot.loc[i, 'Umschichten'] = df_depot.loc[i, 'Jahresende nach Kosten']
        else:
            df_depot.loc[i, 'Umschichtung'] = df_depot.loc[i, 'UmschichtungJN'] * df_depot.loc[i, 'AnteilUmschichtung']  # W
            df_depot.loc[i, 'Umschichten'] = df_depot.loc[i, 'Jahresende nach Kosten'] * df_depot.loc[i, 'Umschichtung']  # X

        if df_depot.loc[i - 1, 'UmschichtungJN'] == 1:
            df_depot.loc[i, 'Erträgelaufend'] = df_depot.loc[i, 'Wertsteigerung']
        else:
            df_depot.loc[i, 'Erträgelaufend'] = df_depot.loc[i - 1, 'Erträgelaufend'] + df_depot.loc[i, 'Wertsteigerung']
        df_depot.loc[i, 'Erträge'] = df_depot.loc[i, 'Erträgelaufend'] * df_depot.loc[i, 'Umschichtung']  # Z
        df_depot.loc[i, 'minus Vorabpauschale'] = (df_depot.loc[i, 'Erträgelaufend'] - df_depot.loc[i, 'Vorabpauschalelaufend']) * df_depot.loc[i, 'Umschichtung']  # AA
        df_depot.loc[i, 'Teilfreistellung '] = df_depot.loc[i, 'minus Vorabpauschale'] * teilfreistellung_aktienfonds_sparplan  # AB
        df_depot.loc[i, 'zu besteuern '] = df_depot.loc[i, 'minus Vorabpauschale'] - df_depot.loc[i, 'Teilfreistellung ']  # AC

        if df_depot.loc[i, 'Freistellung übrig'] > df_depot.loc[i, 'zu besteuern ']:
            df_depot.loc[i, 'nach Freistellungsauftrag'] = 0  # AD
        else:
            df_depot.loc[i, 'nach Freistellungsauftrag'] = df_depot.loc[i, 'zu besteuern '] - df_depot.loc[i, 'Freistellung übrig']  # AD

        df_depot.loc[i, 'Steuerlast '] = df_depot.loc[i, 'nach Freistellungsauftrag'] * steuerlast_sparplan  # AE
        df_depot.loc[i, 'Kapital abzüglich Steuer'] = df_depot.loc[i, 'Umschichten'] - df_depot.loc[i, 'Steuerlast ']  # AF

# Row A1
col1, col2, col3 = st.columns(3)

fondspolice_rentenkapital = df_police.loc[i, 'Jahresende nach Kosten']

col1.markdown(custom_metric_html.format(label="Fondspolice Rentenkapital", value=format_german(fondspolice_rentenkapital)), unsafe_allow_html=True)


fondspolice_ertraege = fondspolice_rentenkapital - einmalbeitrag_police
fondspolice_teilfreistellung_result = fondspolice_ertraege * teilfreistellung_police
fondspolice_zu_besteuern_result = fondspolice_ertraege - fondspolice_teilfreistellung_result
fondspolice_hev_result = fondspolice_zu_besteuern_result/2
fondspolice_steuerlast_result = fondspolice_hev_result * steuersatz_police
fondspolice = fondspolice_rentenkapital - fondspolice_steuerlast_result
col2.markdown(custom_metric_html.format(label="Fondspolice", value=format_german(fondspolice)), unsafe_allow_html=True)

fondssparplan = df_depot.loc[i, 'Kapital abzüglich Steuer']
col3.markdown(custom_metric_html.format(label="Fondssparplan", value=format_german(fondssparplan)), unsafe_allow_html=True)


# Add a button to trigger the save
st.sidebar.title(' ')
if st.sidebar.button('Parameter Speichern'):
    # Creating a dictionary of parameters to save
    data_to_save = {
        ### Parameter Police
        'einmalbeitrag_police': einmalbeitrag_police,
        'rendite_mischfonds_police': rendite_mischfonds_police*100,
        'rendite_rentenfonds_police': rendite_rentenfonds_police*100,
        'rendite_aktienfonds_police': rendite_aktienfonds_police*100,
        'teilfreistellung_police': teilfreistellung_police*100,
        'effektivkosten_police': effektivkosten_police*100,
        'steuersatz_police': steuersatz_police*100,
        ### Parameter Sparplan
        'einmalbeitrag_sparplan': einmalbeitrag_sparplan,
        'rendite_aktienfonds_sparplan': rendite_aktienfonds_sparplan*100,
        'rendite_mischfonds_sparplan': rendite_mischfonds_sparplan*100,
        'rendite_rentenfonds_sparplan': rendite_rentenfonds_sparplan*100,
        'freistellungsauftrag_sparplan': freistellungsauftrag_sparplan,
        'teilfreistellung_aktienfonds_sparplan': teilfreistellung_aktienfonds_sparplan*100,
        'teilfreistellung_mischfonds_sparplan': teilfreistellung_mischfonds_sparplan*100,
        'teilfreistellung_rentenfonds_sparplan': teilfreistellung_rentenfonds_sparplan*100,
        'basiszins_sparplan': basiszins_sparplan*100,
        'effektivkosten_sparplan': effektivkosten_sparplan*100,
        'ausgabeaufschlag_sparplan': ausgabeaufschlag_sparplan*100,
        'steuerlast_sparplan': steuerlast_sparplan*100,
        'steuerlast_auszahlung_sparplan': steuerlast_auszahlung_sparplan*100,
        ### Weitere Parameter
        'laufzeit': laufzeit+1,
        'umschichtungen': st.session_state['umschichtungen']
    }

    # Convert dictionary to JSON string
    json_str = json.dumps(data_to_save, indent=4)

    # Convert the string to bytes
    b64 = base64.b64encode(json_str.encode()).decode()

    # Provide a link to download the JSON file
    href = f'<a href="data:file/json;base64,{b64}" download="parameters.json">Parameter Herunterladen</a>'
    st.sidebar.markdown(href, unsafe_allow_html=True)

# Row C
categories = ['Fondspolice Rentenkapital', 'Fondspolice', 'Fondssparplan']
values = [fondspolice_rentenkapital, fondspolice, fondssparplan]

# Create two columns
col1, col2 = st.columns(2)

# Plot the bar chart with a light blue background
with col1:
    fig, ax = plt.subplots(figsize=(10, 7), facecolor='#d6e8ee')
    ax.set_facecolor('#d6e8ee')
    bars = ax.bar(categories, values, color=['#92d050', '#00a44a', '#00b0f0'])
    ax.set_xlabel(' ')
    ax.set_xticks(range(len(categories)))
    ax.set_xticklabels(categories, rotation=0)  # Set the rotation of x-axis labels to 0 for horizontal labels
    ax.set_yticks([])  # Remove y-axis scale
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    plt.tight_layout()

    # Add numerical value on top of each bar
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, yval + 10, f'{yval:,.0f} €'.replace(',', '.'), ha='center', va='bottom')

    # Display the plot in Streamlit
    st.pyplot(plt)

with col2:
    df_police_display = df_police
    df_depot_display = df_depot
    df_fondspolice_display = df_police
    new_row1 = pd.DataFrame({'Jahr': [df_depot_display['Jahr'].max() + 1], 'Jahresende nach Kosten': [fondssparplan]})
    new_row2 = pd.DataFrame({'Jahr': [df_fondspolice_display['Jahr'].max() + 1], 'Jahresende nach Kosten': [fondspolice]})
    df_depot_display = pd.concat([df_depot_display, new_row1], ignore_index=True)
    df_fondspolice_display = pd.concat([df_fondspolice_display, new_row2], ignore_index=True)
    fig, ax = plt.subplots(figsize=(10, 7), facecolor='#d6e8ee')
    ax.set_facecolor('#d6e8ee')
    ax.plot(df_depot_display['Jahr'], df_depot_display['Jahresende nach Kosten'], linestyle='-', color='#00b0f0')
    ax.plot(df_fondspolice_display['Jahr'], df_fondspolice_display['Jahresende nach Kosten'], linestyle='-', color='#00a44a')
    ax.plot(df_police_display['Jahr'], df_police_display['Jahresende nach Kosten'], linestyle='-', color='#92d050')
    ax.set_xlabel(' ')
    ax.set_ylabel(' ')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    #ax.legend()
    plt.tight_layout()

    # Manually set y-axis tick labels
    yticks = ax.get_yticks()
    ax.set_yticklabels([euro_formatter(y) for y in yticks])

    # Display the plot in Streamlit
    st.pyplot(fig)

# Display the DataFrame as a table in Streamlit
st.markdown('### Fondspolice')
df_police = df_police.round(2)
st.dataframe(df_police)

csv = df_police.to_csv(index=False)
st.download_button(
    label="Als CSV herunterladen",
    data=csv,
    file_name="police.csv",
    mime="text/csv",
)


st.markdown('### Fondssparplan')
df_depot = df_depot.round(2)
st.dataframe(df_depot)

csv = df_depot.to_csv(index=False)
st.download_button(
    label="Als CSV herunterladen ",
    data=csv,
    file_name="depot.csv",
    mime="text/csv",
)

###Markdowns
st.markdown("""
<style>
div[data-testid="metric-container"] {
    background-color: #FFFFFF;
    border: 1px solid #CCCCCC;
    padding: 5% 5% 5% 10%;
    border-radius: 15px;
    border-left: 0.5rem solid #405087 !important;
    box-shadow: 0 0.15rem 1.75rem 0 rgba(58, 59, 69, 0.15) !important;
   overflow-wrap: break-word;
}

</style>
"""
            , unsafe_allow_html=True)
