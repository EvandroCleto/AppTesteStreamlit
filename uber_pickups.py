import streamlit as st
import pandas as pd
import numpy as np

#Help .
#$ streamlit help

#Adiona Titulo ao APP
st.title('Uber pickups in NYC')

#Função para baixar o arquivo e carregar-lo em um dataframe
DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
         'streamlit-demo-data/uber-raw-data-sep14.csv.gz')

@st.cache
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data
    
 # Create a text element and let the reader know the data is loading.
data_load_state = st.text('Loading data...')
# Load 10,000 rows of data into the dataframe.
data = load_data(10000)
# Notify the reader that the data was successfully loaded.
data_load_state.text("Done! (using st.cache)")

# Exibe algumas linhas do Dataframe no append
#st.subheader('Raw data')
#st.write(data)# --->>> Pode usar st.dataframe se os dados não estiverem sido exibidos corretamente.

#trecho acima foi trocado pelo abaixo
# Metodo checkbox esconde/exibe a tabela de dados
if st.checkbox('Show Data Table'):
    st.subheader('Data table')
    st.write(data)

#Adiciona Subtitulo
st.subheader('Number of pickups by hour')

# Use NumPy to generate a histogram that breaks down pickup times binned by hour:
hist_values = np.histogram(
    data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]
# ->>> O Horario mais ocupado é as 17hs 

# O metodo  st.bar_chart() desenha o histograma
st.bar_chart(hist_values)

#Adiciona Subtitulo
#st.subheader('Map of all pickups')

#st.map -> transforma dados de latitude e longitude em mapa
#st.map(data)

#Substiruindo o trecho acima por:
# Variável para filtrar o mapa pela horario mais oxupado do dia(17hs), conforme visto no histograma. 
#hour_to_filter = 17 -> Variável estatica foi substituida pelo st.sliderbar que renderiza o mapa pelo horario configurado no slidebar.
hour_to_filter = st.slider('hour', 0, 23, 17)  # min: 0h, max: 23h, default: 17h

#faz o filtro pelo horario
filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]
#Adiciona Subtitulo
st.subheader(f'Map of all pickups at {hour_to_filter}:00')
#st.map -> transforma dados de latitude e longitude em mapa no horario filtrado
st.map(filtered_data)

