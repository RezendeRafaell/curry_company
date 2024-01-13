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
#from streamlit_folium import folium_static

# Lendo o arquivo usando o pd:
df = pd.read_csv('train.csv')


# Limpeza dos dados
df1 = df.copy()

## 1. convertendo a coluna Age de texto para número
linhas_selecionadas = df1["Delivery_person_Age"] != 'NaN '
df1 = df1.loc[linhas_selecionadas, :].copy()

linhas_selecionadas = df1["Road_traffic_density"] != 'NaN '
df1 = df1.loc[linhas_selecionadas, :].copy()

linhas_selecionadas = df1["City"] != 'NaN '
df1 = df1.loc[linhas_selecionadas, :].copy()

linhas_selecionadas = df1["Festival"] != 'NaN '
df1 = df1.loc[linhas_selecionadas, :].copy()
df1["multiple_deliveries"] = df1["multiple_deliveries"].astype(str)
linhas_selecionadas = df1["multiple_deliveries"] != 'NaN '
df1 = df1.loc[linhas_selecionadas, :].copy()

linhas_selecionadas = df1["multiple_deliveries"] != 'nan'
df1 = df1.loc[linhas_selecionadas, :].copy()


df1['Delivery_person_Age'] = df1['Delivery_person_Age'].astype(int)

## 2. convertendo a coluna Ratings de texto para numero decimal (float)
df1["Delivery_person_Ratings"] = df1["Delivery_person_Ratings"].astype(float)

## 3. convertendo a coluna de order_date de texto para data
df1['Order_Date'] = pd.to_datetime(df1['Order_Date'], format = '%d-%m-%Y')

## 4. convertendo mutiple_deliveries de texto para número inteiro (int)

df1['multiple_deliveries'] = df1['multiple_deliveries'].astype(int)

## 5. Removendo os espaços dentro de strings/texto/object
# df1 = df1.reset_index(drop=True)
# for i in range(len(df1)):
#   df1.loc[i, 'ID'] = df1.loc[i,'ID'].strip()

##6. Removendo os espaços dentro de strings/texto/object
df1.loc[:, 'ID'] = df1.loc[:, 'ID'].str.strip()
df1.loc[:, 'Road_traffic_density'] = df1.loc[:, 'Road_traffic_density'].str.strip()
df1.loc[:, 'Type_of_order'] = df1.loc[:, 'Type_of_order'].str.strip()
df1.loc[:, 'Type_of_vehicle'] = df1.loc[:, 'Type_of_vehicle'].str.strip()
df1.loc[:, 'City'] = df1.loc[:, 'City'].str.strip()
df1.loc[:, 'Festival'] = df1.loc[:, 'Festival'].str.strip()

##7. Limpando a coluna de time taken

df1['Time_taken(min)'] = df1['Time_taken(min)'].apply(lambda x: x.split('(min) ')[1] )
df1['Time_taken(min)'] = df1['Time_taken(min)'].astype(int)

#===============
# Novas colunas
#===============

# Criando a coluna de semanas por ano:
df1['week_of_year'] = df1['Order_Date'].dt.strftime('%U')




# ============================================================================
# Título
# ============================================================================


st.header("Título")
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
        df_aux = df1.loc[:, ['ID', 'Order_Date']].groupby('Order_Date').count().reset_index()
        fig = px.bar(df_aux, x ='Order_Date', y = 'ID')
        st.plotly_chart(fig, use_container_width=True)

    
    with st.container():
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### Pedidos por tráfego")
            df_aux = df1.loc[:, ['ID', 'Road_traffic_density']].groupby('Road_traffic_density').count().reset_index()
            fig = px.pie(df_aux, values = 'ID', names = 'Road_traffic_density')
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.markdown("### Pedidos por tráfego e cidade")
            df_aux = df1.loc[:, ['ID', 'City', 'Road_traffic_density']].groupby(['City', 'Road_traffic_density']).count().reset_index()
            df_aux = df_aux.loc[(df_aux["Road_traffic_density"]) != 'NaN' , :]
            df_aux = df_aux.loc[(df_aux["City"] != 'NaN' ), :]
            fig = px.scatter(df_aux, x = 'City', y = 'Road_traffic_density', size = 'ID', color = 'City')
            st.plotly_chart(fig, use_container_width=True)

#st.dataframe(df1)


## Tabela 2
with tab2:
    with st.container():
        st.markdown("## Pedidos por semana")
        # Quantidade de pedidos / Número único de entregadores por semana
        df_aux01 = df1.loc[:, ['ID', 'week_of_year']].groupby(['week_of_year']).count().reset_index()
        df_aux02 = df1.loc[:, ['Delivery_person_ID', 'week_of_year']].groupby('week_of_year').nunique().reset_index()
        df_aux = pd.merge(df_aux01, df_aux02, how ='inner')
        df_aux['order_by_deliver'] = df_aux['ID'] / df_aux['Delivery_person_ID']
        fig = px.line(df_aux, x='week_of_year', y= 'order_by_deliver')
        st.plotly_chart(fig, use_container_width=True)
    with st.container():
        # Pensar em um outro gráfico pra colocar aqui!
        pass

## Tabela 3
with tab3:

    with st.container():
        st.markdown("## Country Maps")
        df_aux = df1.loc[:, ["City", "Road_traffic_density", "Delivery_location_latitude", "Delivery_location_longitude"]].groupby(["City", "Road_traffic_density"]).median().reset_index()
        
        map = folium.Map()
        for index, location_info in df_aux.iterrows():
            folium.Marker([location_info['Delivery_location_latitude'],
                        location_info['Delivery_location_longitude']],
                        popup=location_info[['City', 'Road_traffic_density']]).add_to(map)

        streamlit_folium.folium_static(map, width=1024, height=600)

        
        
#