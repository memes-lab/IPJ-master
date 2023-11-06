import pandas as pd
import csv
import matplotlib.pyplot as plt
import matplotlib.style as style
import datetime
import time
import streamlit as st


## Apply dark background style
style.use('dark_background')

st.title("WATT-Meister-Consulting Calculator")
st.divider()
st.subheader('Energy production and consumption')
st.write('For the following plots, we collected the electricity market data of Germany for the years 2020, 2021, and 2022 and analyzed the production and consumption. In the first plot, you can see the production and consumption for any specific day in the period from 2020 to 2022.')

start_date = datetime.date(2020, 1, 1)
end_date = datetime.date(2022, 12, 31)
default_date = datetime.date(2020, 1, 1)
st.write("##")
input_date = st.date_input("Select a Date",value = default_date, min_value=start_date, max_value=end_date)

def parse_datetime(date_str, time_str):
    return datetime.datetime.strptime(f"{date_str} {time_str}", "%d.%m.%Y %H:%M")

startzeit = time.time()

csv_datei = 'Realisierte_Erzeugung_202001010000_202212312359_Viertelstunde.csv'
csv_datei2 = 'Realisierter_Stromverbrauch_202001010000_202212312359_Viertelstunde.csv'


energie_daten = []
energie_daten2 = []
production = []
consumption = []

#function that reads Erzeugung csv data
with open(csv_datei, 'r') as file:
    csv_reader = csv.reader(file, delimiter=';')
    next(csv_reader)
    
    #for loop to read in csv rows
    for row in csv_reader:
        datum = row[0]
        anfang = row[1]
        ende = row[2]
        biomasse = float(row[3].replace('.', '').replace(',', '.'))
        wasserkraft = float(row[4].replace('.', '').replace(',', '.'))
        wind_offshore = float(row[5].replace('.', '').replace(',', '.'))
        wind_onshore = float(row[6].replace('.', '').replace(',', '.'))
        photovoltaik = float(row[7].replace('.', '').replace(',', '.'))
        try:
            sonstige_erneuerbare = float(row[8].replace('.', '').replace(',', '.')) 
        except ValueError:
            sonstige_erneuerbare = 0.0
        kernenergie = float(row[9].replace('.', '').replace(',', '.'))
        braunkohle = float(row[10].replace('.', '').replace(',', '.'))
        steinkohle = float(row[11].replace('.', '').replace(',', '.'))
        erdgas = float(row[12].replace('.', '').replace(',', '.'))
        pumpspeicher = float(row[13].replace('.', '').replace(',', '.'))
        sonstige_konventionelle = float(row[14].replace('.', '').replace(',', '.'))

        datensatz = {
            'Datum': datum,
            'Anfang': anfang,
            'Ende': ende,
            'Biomasse [MWh]': biomasse,
            'Wasserkraft [MWh]': wasserkraft,
            'Wind Offshore [MWh]': wind_offshore,
            'Wind Onshore [MWh]': wind_onshore,
            'Photovoltaik [MWh]': photovoltaik,
            'Sonstige Erneuerbare [MWh]': sonstige_erneuerbare,
            'Kernenergie [MWh]': kernenergie,
            'Braunkohle [MWh]': braunkohle,
            'Steinkohle [MWh]': steinkohle,
            'Erdgas [MWh]': erdgas,
            'Pumpspeicher [MWh]': pumpspeicher,
            'Sonstige Konventionelle [MWh]': sonstige_konventionelle
        }
        ## datensatz is added to  list energie daten
        energie_daten.append(datensatz) 

## Viertelstunden Verbrauch csv read in
with open(csv_datei2, 'r') as file:
    csv_reader = csv.reader(file, delimiter=';')
    next(csv_reader)
    for row in csv_reader:
        datum = row[0]
        anfang = row[1]
        gesamt = float(row[3].replace('.', '').replace(',', '.'))

        datensatz1 = {
            'Datum': datum,
            'Anfang': anfang,
            'Gesamt (Netzlast) [MWh]': gesamt,
        }
        energie_daten2.extend([datensatz1])



production = [datensatz['Biomasse [MWh]'] + datensatz['Wasserkraft [MWh]'] + datensatz['Wind Offshore [MWh]'] + datensatz['Wind Onshore [MWh]'] + datensatz['Photovoltaik [MWh]'] + datensatz['Sonstige Erneuerbare [MWh]'] for datensatz in energie_daten]

consumption = [datensatz1['Gesamt (Netzlast) [MWh]'] for datensatz1 in energie_daten2]
    

selected_date = input_date
filtered_data = [datensatz for datensatz in energie_daten if parse_datetime(datensatz['Datum'], datensatz['Anfang']).date() == selected_date]
filtered_data2 = [datensatz1 for datensatz1 in energie_daten2 if parse_datetime(datensatz1['Datum'], datensatz1['Anfang']).date() == selected_date]


hours = [parse_datetime(datensatz['Datum'], datensatz['Anfang']).hour + parse_datetime(datensatz['Datum'], datensatz['Anfang']).minute / 60 for datensatz in filtered_data]
production_day = [datensatz['Biomasse [MWh]'] + datensatz['Wasserkraft [MWh]'] + datensatz['Wind Offshore [MWh]'] + datensatz['Wind Onshore [MWh]'] + datensatz['Photovoltaik [MWh]'] + datensatz['Sonstige Erneuerbare [MWh]'] for datensatz in filtered_data]
consumption_day = [datensatz1['Gesamt (Netzlast) [MWh]'] for datensatz1 in filtered_data2]

def range1(array1, array2):
    if len(array1) != len(array2):
        raise ValueError("Arrays must be the same length")
    
    count10 = 0
    count20 = 0
    count30 =0
    count40 = 0
    count50 = 0
    count60 = 0
    count70 = 0
    count80 = 0
    count90 = 0
    count100 = 0

    for val1, val2 in zip(array1, array2):
        if 0.1 <= val1 / val2 < 0.2:
            count10 += 1
        if 0.2 <= val1 / val2 < 0.3:
            count20 +=1
        if 0.3 <= val1 / val2 < 0.4:
            count30 +=1
        if 0.4 <= val1 / val2 < 0.5:
            count40 +=1
        if 0.5 <= val1 / val2 < 0.6:
            count50 +=1
        if 0.6 <= val1 / val2 < 0.7:
            count60 +=1
        if 0.7 <= val1 / val2 < 0.8:
            count70 +=1
        if 0.8 <= val1 / val2 < 0.9:
            count80 +=1
        if 0.9 <= val1 / val2 < 1:
            count90 +=1
        if  val1 / val2  == 1:
            count100+=1

    return [count10, count20, count30, count40, count50, count60, count70, count80, count90, count100]

counts =[]
counts = range1(production, consumption)
print(counts)




if input_date:
    selected_date = datetime.datetime.strptime(str(input_date), "%Y-%m-%d").date()

    # Create the figure and axes objects for the first plot
    fig1, ax1 = plt.subplots(figsize=(12, 6))

    ax1.plot(hours, consumption_day, label='Consumption')
    ax1.plot(hours, production_day, label='Production (renewable energy)', linewidth=2.5)

    ax1.set_xlabel('Time [Hour]')
    ax1.set_ylabel('Power (MWh)')
    ax1.set_title(f'Energy production and consumption for {selected_date.strftime("%d.%m.%Y")}')
    ax1.fill_between(hours, consumption_day)
    ax1.fill_between(hours, production_day)
    ax1.legend()
    # plt.tight_layout()
    ax1.grid(True)
    ax1.set_xticks(range(0, 24))

    # printing out the daily metrics
    #'''biomass_production = sum(datensatz['Biomasse [MWh]'] for datensatz in filtered_data)
    #water_production = sum(datensatz['Wasserkraft [MWh]'] for datensatz in filtered_data)
    #wind_off_production = sum(datensatz['Wind Offshore [MWh]'] for datensatz in filtered_data)
    #wind_on_production = sum(datensatz['Wind Onshore [MWh]'] for datensatz in filtered_data)
    #pv_production = sum(datensatz['Photovoltaik [MWh]'] for datensatz in filtered_data)
    #other_re_production = sum(datensatz['Sonstige Erneuerbare [MWh]'] for datensatz in filtered_data)
    #nuclear_production = sum(datensatz[ 'Kernenergie [MWh]'] for datensatz in filtered_data)
    #browncoal_production = sum(datensatz['Braunkohle [MWh]'] for datensatz in filtered_data)
    #stonecoal_production = sum(datensatz['Steinkohle [MWh]'] for datensatz in filtered_data)
    #gas_production = sum(datensatz['Erdgas [MWh]'] for datensatz in filtered_data)
    #storage_production = sum(datensatz['Pumpspeicher [MWh]'] for datensatz in filtered_data)
    #other_conv_production = sum(datensatz['Sonstige Konventionelle [MWh]'] for datensatz in filtered_data)
    #
#
    #st.subheader('Overview')
    #st.metric(label='Biomass Production (MWh)', value=biomass_production)
    #st.metric(label='Wasserkraft [MWh]', value=biomass_production)
    #st.metric(label='Wind Offshore Production (MWh)', value=wind_off_production)
    #st.metric(label='Wind Onshore Production (MWh)', value=wind_on_production)
    #st.metric(label='Photovoltaik Production (MWh)', value=pv_production)
    #st.metric(label='Sonstige Erneuerbare Production (MWh)', value=other_re_production)
    #st.metric(label='Nuclear Production (MWh)', value=nuclear_production)
    #st.metric(label='Browncoal Production (MWh)', value=browncoal_production)
    #st.metric(label='Stonecoal Production (MWh)', value=stonecoal_production)
    #st.metric(label='Gas Production (MWh)', value=gas_production)
    #st.metric(label='Storage Production (MWh)', value=storage_production)
    #st.metric(label='Sonstige Konventionelle Production (MWh)', value=other_conv_production)'''


    # Create the figure and axes objects for the second plot
    ##fig2, ax2 = plt.subplots(figsize=(6, 4))
    
    # Create the figure and axes objects for the second plot
fig2, ax2 = plt.subplots(figsize=(6, 4))

    # Set the x-tick positions and labels
    
##Geändert!!!
x_ticks = range(len(counts))
x_labels = ['10%', '20%', '30%', '40%', '50%', '60%', '70%', '80%', '90%', '100%']
ax2.set_xticks(x_ticks)
ax2.set_xticklabels(x_labels)

ax2.bar(x_ticks, counts)
ax2.set_title('Anzahl der Viertelstunden mit 10-100 % EE-Anteil')

###
    ## ALTER CODE
    ##ax2.bar(range(len(counts)), counts)
    ##ax2.set_title('Anzahl der Viertelstunden mit 10-100 % EE-Anteil')
    ##ax2.set_xticklabels(['10%', '20%', '30%', '40%', '50%', '60%', '70%', '80%', '90%', '100%'])
    ##


# ... Remaining code omitted for brevity ...

if input_date:


    st.pyplot(fig1)


    st.write("##")
    st.write("##")
    st.subheader('Amount of quarter hours with Renewable Energy in Percent')
    st.markdown("---")
    st.pyplot(fig2)

    endzeit = time.time()
    dauer = endzeit - startzeit
    st.write(f"Startzeit: {startzeit}")
    st.write(f"Endzeit: {endzeit}")
    st.write(f"Dauer des Programms: {dauer} Sekunden")




# Define the threshold value for low renewables production
threshold = 1000

# Create a dictionary to store the total renewable energy production for each day
daily_production = {}

# Loop through the energy data and calculate the total renewable energy production for each day
for row in csv_reader:
    # Parse the date and time from the row
    date_str, time_str = row[0], row[1]
    dt = parse_datetime(date_str, time_str)
    date = dt.date()

    # Calculate the total renewable energy production for this row
    biomasse = float(row[3].replace('.', '').replace(',', '.'))
    wasserkraft = float(row[4].replace('.', '').replace(',', '.'))
    wind_offshore = float(row[5].replace('.', '').replace(',', '.'))
    wind_onshore = float(row[6].replace('.', '').replace(',', '.'))
    photovoltaik = float(row[7].replace('.', '').replace(',', '.'))
    sonstige_erneuerbare = float(row[8].replace('.', '').replace(',', '.'))
    total_renewables = biomasse + wasserkraft + wind_offshore + wind_onshore + photovoltaik + sonstige_erneuerbare

    # Add the total renewable energy production to the daily_production dictionary
    if date in daily_production:
        daily_production[date] += total_renewables
    else:
        daily_production[date] = total_renewables

# Loop through the daily_production dictionary and print out the dates with low renewables production
for date, production in daily_production.items():
    if production < threshold:
        print(f"{date}: {production}")

        ## whats the issue here?
    st.write(f"{date}: {production}") 