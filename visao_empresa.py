# Importar as bibliotecas:
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go 
from haversine import haversine
import pandas as pd
from datetime import datetime
from PIL import Image
import folium
import streamlit_folium
from utils import *
#from streamlit_folium import folium_static

# Lendo o arquivo:
df = pd.read_csv('train.csv')
# Limpeza e tratamento:
df1 = clean_data(df)



# ============================================================================
# Título
# ============================================================================


st.header("Visão da Empresa")
# ============================================================================
# Barra Lateral
# ============================================================================

image_path = "/home/rafael/Desktop/comunidadeds/FTC/projeto_copia/Imagem1.jpg"
image = Image.open(image_path)
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


# ________________________

# ============================================================================
# Layout do Streamlit
# ============================================================================

# Tabelas
tab1, tab2, tab3 = st.tabs(["Visão Empresa", "Visão Tática", "Visão Geográfica"])

## Tabela 1
with tab1:

    with st.container():
        #Métrica de Pedidos
        st.header("Pedidos por dia")
        fig = order_date_metric(df1)
        st.plotly_chart(fig, use_container_width=True)

    
    with st.container():
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### Pedidos por tráfego")
            fig = traffic_order_city(df1)
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.markdown("### Pedidos por tráfego e cidade")
            fig = oder_by_traffic_and_city(df1)
            st.plotly_chart(fig, use_container_width=True)

#st.dataframe(df1)


## Tabela 2
with tab2:
    with st.container():
        st.markdown("## Pedidos por semana")
        #### Dúvida: Isso é uma boa prática? Minha função tá me retornando dois valores
        df_aux, fig = order_share_by_week(df1)
        st.plotly_chart(fig, use_container_width=True)
    

## Tabela 3
with tab3:

    with st.container():
        st.markdown("## Country Maps")
        country_maps(df1)




