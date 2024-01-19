import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go 
from haversine import haversine
import pandas as pd
from datetime import datetime
from PIL import Image
import plotly.graph_objects as go
import folium
import streamlit_folium
from pages.utils.util import *
#from streamlit_folium import folium_static

st.set_page_config(page_title = "Visão Restaurantes", layout="wide")


# Lendo o arquivo usando o pd:
df = pd.read_csv('pages/utils/train.csv')

# Limpando os dados
df1 = clean_data(df)
# ============================================================================
# Título
# ============================================================================


st.header("Visão dos restaurantes")
# ============================================================================
# Barra Lateral
# ============================================================================


# image_path = "/home/rafael/Desktop/data_projects/pages/utils/"
image = Image.open("curry_image.jpeg")
st.sidebar.image(image, width=140)

st.sidebar.markdown("# Curry Company")
st.sidebar.markdown("""---""")

st.sidebar.markdown("## Selecione uma data limite")

#Filtro de data:

date_slider = st.sidebar.slider("Até quando?",
                   min_value= datetime(2022, 3, 1),
                   value= datetime(2022, 3, 15),
                   max_value= datetime(2022, 3, 31),
                   format="DD/MM/YYYY"
 )
                  
st.sidebar.markdown("""---""")                  

st.sidebar.markdown("## Condições de tráfego")

traffic_options = st.sidebar.multiselect(
    "Selecione as que você deseja analisar",
    ["Low", "Jam", "Medium", "High"],
    default=["Low", "Jam", "Medium", "High"]
)

weatherconditions_options = st.sidebar.multiselect(
    "Selecione as condições que você deseja analisar",
    ['conditions Sunny', 'conditions Stormy', 'conditions Sandstorms','conditions Cloudy', 'conditions Fog', 'conditions Windy'],
    default=['conditions Sunny', 'conditions Stormy', 'conditions Sandstorms','conditions Cloudy', 'conditions Fog', 'conditions Windy']
)

st.sidebar.markdown("""---""")
st.sidebar.markdown("### Powered by Rafael Rezende dos Santos")

# Filtro de datas
linhas_selecionadas = df1['Order_Date'] < date_slider
df1 = df1.loc[linhas_selecionadas, : ]

# Filtro por tráfego
linhas_selecionadas = df1['Road_traffic_density'].isin(traffic_options)
df1 = df1.loc[linhas_selecionadas, : ]

# Filtro por condição climática 
linhas_selecionadas = df1['Weatherconditions'].isin(weatherconditions_options)
df1 = df1.loc[linhas_selecionadas,]

# ============================================================================
# Layout do Streamlit
# ============================================================================

# Sem tabelas por enquanto
#=================================================
###FUNÇÕES:

# def avg_delivery_distance(df1):
#     col = ['Restaurant_latitude', 'Restaurant_longitude', 'Delivery_location_latitude', 'Delivery_location_longitude']
#     df1['distance'] = df1.loc[:, col].apply(lambda x: 
#                                             haversine( (x['Restaurant_latitude'], x['Restaurant_longitude']), (x['Delivery_location_latitude'], x['Delivery_location_longitude'] )), axis=1)
#     avg_distance = df1['distance'].mean()
    
#     return avg_distance


#================================================



with st.container():
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    with col1:
        delivery_unique = len(df1.loc[:, 'Delivery_person_ID'].unique())
        col1.metric("Entregadores únicos",delivery_unique)

    with col2:
        avg_distance = avg_delivery_distance(df1)
        col2.metric("Distância Média",np.round(avg_distance, 2))


    with col3:
        df_aux = op_time_delivery(df1, op = "avg_time", Festival=True)
        col3.metric('Tempo médio: ', df_aux) 

    with col4:
        #st.markdown("###### Desvio padrão de entrega com festival")
        df_aux = op_time_delivery(df1, op="std_time", Festival=True)
        col4.metric("STD entrega:", df_aux)



    with col5:
        #st.markdown("###### Tempo de entrega sem Festival")
        df_aux = op_time_delivery(df1, op="avg_time", Festival=False)
        col5.metric("Tempo Médio Festival",df_aux)



    with col6   :

        df_aux = op_time_delivery(df1, op="std_time", Festival=False)
        col6.metric('STD sem festival: ', df_aux)


with st.container():
        st.markdown("### Tempo médio de entrega por cidade e por tipo de tráfego")
        df_aux = op_delivery_by_city(df1, option_col="Road_traffic_density")
        fig = px.sunburst(df_aux, 
                          path=['City', 'Road_traffic_density' ],
                          values='avg_time',
                          color = 'std_time',
                          color_continuous_scale = 'RdBu',
                          color_continuous_midpoint=np.average(df_aux['std_time']))
        st.plotly_chart(fig)

with st.container():
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("## Tempo médio por cidade")
        fig = avg_time_by_city(df1)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("## Tempo médio e o desvio padrão de entrega por cidade ")
        df_aux = op_delivery_by_city(df1, option_col="Type_of_order")
        st.dataframe(df_aux, use_container_width=True)


with st.container():
    st.markdown("### Distância média dos restaurantes e os locais de entrega por cidade")
    col1, col2 = st.columns(2)
    with col1:

        fig, _ = avg_delivery_distance_by_city(df1)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("")
        st.markdown("")
        st.markdown("")
        st.markdown("")
        st.markdown("")
        st.markdown("")
        st.markdown("")
        st.markdown("")
        st.markdown("")
        st.markdown("")
        st.markdown("")
        _, avg_distance = avg_delivery_distance_by_city(df1)
        avg_distance.rename(columns ={"City" : "Tipos_de_cidade", "distance": "Distancia_media_das_entregas"})
        st.dataframe(avg_distance) 



    