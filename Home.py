# Importar as bibliotecas:
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go 
from haversine import haversine
import pandas as pd
from datetime import datetime
from PIL import Image
from pages.utils.util import *

st.set_page_config(
    page_title = "Home",
    layout= "wide"
)

df = pd.read_csv('pages/utils/train.csv')
df1 = clean_data(df)



#image_path = "/home/rafael/Desktop/data_projects/pages/utils/"
image = Image.open("curry_image.jpeg")
st.sidebar.image(image, width=140)

st.sidebar.markdown("# Curry Company")
st.sidebar.markdown("## Fastest Delivery in Town")
st.sidebar.markdown("""----""")

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

#Filtro de opções de tráfego
traffic_options = st.sidebar.multiselect(
    "Selecione as que você deseja analisar",
    ["Low", "Jam", "Medium", "High"],
    default= ["Low", "Jam", "Medium", "High"]
)

st.sidebar.markdown("""---""")
st.sidebar.markdown("### Powered by Rafael Rezende dos Santos")

# Filtro de datas
linhas_selecionadas = df1['Order_Date'] < date_slider
df1 = df1.loc[linhas_selecionadas, : ]

# Filtro por tráfego
linhas_selecionadas = df1['Road_traffic_density'].isin(traffic_options)
df1 = df1.loc[linhas_selecionadas, : ]




st.write("# Curry Company Growth Dashboard")



st.markdown(
    """
    Growth Dashboard for construído para acompanhar as métricas de crescimento dos Entregadores e Restaurantes
    ### Com utilizar esse Growth Dashboard?
    - Visão empresa:
        - Visão Gerencial: Métricas gerais de comportamento.
        - Visão Tática: Indicadores semanais de crescimento.
        - Visão Geográfica: Insights de geolocalização
    - Visão Entregador:
        - Acompanhamento dos indicadores semanais de crescimento.
    - Visão Restaurante:
        - Indicadores semanais de crescimnento dos restaurantes.
    ### Ask for Help
    - Falar com o Irineu 
        - github: RezendeRafaell 
""")
