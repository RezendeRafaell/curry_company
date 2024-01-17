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
#from streamlit_folium import folium_static

# Lendo o arquivo usando o pd:
df = pd.read_csv('train.csv')

# Limpando os dados
df1 = df.copy()

# 1. convertendo a coluna Age de texto para número
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

# 2. convertendo a coluna Ratings de texto para numero decimal (float)
df1["Delivery_person_Ratings"] = df1["Delivery_person_Ratings"].astype(float)

# 3. convertendo a coluna de order_date de texto para data
df1['Order_Date'] = pd.to_datetime(df1['Order_Date'], format = '%d-%m-%Y')

# 4. convertendo mutiple_deliveries de texto para número inteiro (int)

df1['multiple_deliveries'] = df1['multiple_deliveries'].astype(int)

# 5. Removendo os espaços dentro de strings/texto/object
# df1 = df1.reset_index(drop=True)
# for i in range(len(df1)):
#   df1.loc[i, 'ID'] = df1.loc[i,'ID'].strip()

#6. Removendo os espaços dentro de strings/texto/object
df1.loc[:, 'ID'] = df1.loc[:, 'ID'].str.strip()
df1.loc[:, 'Road_traffic_density'] = df1.loc[:, 'Road_traffic_density'].str.strip()
df1.loc[:, 'Type_of_order'] = df1.loc[:, 'Type_of_order'].str.strip()
df1.loc[:, 'Type_of_vehicle'] = df1.loc[:, 'Type_of_vehicle'].str.strip()
df1.loc[:, 'City'] = df1.loc[:, 'City'].str.strip()
df1.loc[:, 'Festival'] = df1.loc[:, 'Festival'].str.strip()


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


st.header("Visão dos restaurantes")
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

with st.container():
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    with col1:
        st.markdown("###### Entregadores únicos")
        delivery_unique = len(df1.loc[:, 'Delivery_person_ID'].unique())
        st.write(delivery_unique)

    with col2:
        st.markdown("###### Distância Média")
        col = ['Restaurant_latitude', 'Restaurant_longitude', 'Delivery_location_latitude', 'Delivery_location_longitude']
        #VER DEPOIS O PORQUÊ DE ESTÁ DANDO DIFERENTE.
        df1['distance'] = df1.loc[:, col].apply(lambda x: 
                                                haversine( (x['Restaurant_latitude'], x['Restaurant_longitude']), (x['Delivery_location_latitude'], x['Delivery_location_longitude'] )), axis=1)
        

        avg_distance = df1['distance'].mean()
        st.write(np.round(avg_distance, 2))

    with col3:
        #st.markdown("###### Tempo de entrega Festival")
        
        cols = ['Time_taken(min)', 'Festival']
        df_aux = df1.loc[:, cols].groupby( 'Festival').agg({'Time_taken(min)': ['mean', 'std']})

        df_aux.columns = ['avg_time', 'std_time']
        df_aux = df_aux.reset_index()
        #linhas_selecionadas = df_aux['Festival'] == 'Yes'
        #df_aux = df_aux.loc[linhas_selecionadas, :]
        df_aux = (df_aux.loc[df_aux['Festival'] == "Yes", "avg_time"])
        df_aux = np.round(df_aux, 2)
        # Escrever no write depois
        col3.metric('Média: ', df_aux) 

    with col4:
        #st.markdown("###### Desvio padrão de entrega médio com festival")
        cols = ['Time_taken(min)', 'Festival']
        df_aux = df1.loc[:, cols].groupby( 'Festival').agg({'Time_taken(min)': ['mean', 'std']})
        df_aux.columns = ['avg_time', 'std_time']
        df_aux = df_aux.reset_index()
        #linhas_selecionadas = df_aux['Festival'] == 'Yes'
        #df_aux = df_aux.loc[linhas_selecionadas, :]
        df_aux = (df_aux.loc[df_aux['Festival'] == "Yes", "std_time"])
        df_aux = np.round(df_aux, 2)
        col4.metric('STD Festival: ', df_aux)



    with col5:
        #st.markdown("###### Tempo de entrega sem Festival")
        cols = ['Time_taken(min)', 'Festival']
        df_aux = df1.loc[:, cols].groupby( 'Festival').agg({'Time_taken(min)': ['mean', 'std']})
        df_aux.columns = ['avg_time', 'std_time']
        df_aux = df_aux.reset_index()
        df_aux = (df_aux.loc[df_aux['Festival'] == "No", "avg_time"])
        df_aux = np.round(df_aux, 2)
        col5.metric('Tempo sem festival: ', df_aux)

    with col6   :
        #st.markdown("###### Desvio padrão de entrega médio sem festival")
        cols = ['Time_taken(min)', 'Festival']
        df_aux = df1.loc[:, cols].groupby( 'Festival').agg({'Time_taken(min)': ['mean', 'std']})
        df_aux.columns = ['avg_time', 'std_time']
        df_aux = df_aux.reset_index()
        df_aux = (df_aux.loc[df_aux['Festival'] == "No", "std_time"])
        df_aux = np.round(df_aux, 2)
        col6.metric('STD sem festival: ', df_aux)

with st.container():
        st.markdown("### Distância média dos restaurantes e dos locais de entrega")
        col = ['Restaurant_latitude', 'Restaurant_longitude', 'Delivery_location_latitude', 'Delivery_location_longitude']
        df1['distance'] = df1.loc[:, col].apply(lambda x: haversine( (x['Restaurant_latitude'], x['Restaurant_longitude']), (x['Delivery_location_latitude'], x['Delivery_location_longitude'] )), axis=1)
        avg_distance = df1.loc[:, ['City', 'distance']].groupby('City').mean().reset_index()

        #avg_distance
        # Entender melhor:
        fig = go.Figure(data=[go.Pie(labels=avg_distance['City'], values=avg_distance['distance'], pull=[0,0.2,0])])
        st.plotly_chart(fig)

with st.container():
    st.markdown("## Tempo médio por cidade")
    # Gráfico de barras
    cols = ['City', 'Time_taken(min)']
    df_aux = df1.loc[:, cols].groupby('City').agg({'Time_taken(min)': ['mean', 'std']})

    df_aux.columns = ['avg_time', 'std_time']
    df_aux = df_aux.reset_index()
    cols = ['City', 'Time_taken(min)']
    df_aux = df1.loc[:, cols].groupby('City').agg({'Time_taken(min)': ['mean', 'std']})

    df_aux.columns = ['avg_time', 'std_time']

    df_aux = df_aux.reset_index()
    fig = go.Figure()
    fig.add_trace(go.Bar( name = '',
                        x = df_aux['City'],
                        y = df_aux['avg_time'],
                        error_y = dict(type ='data', array=df_aux['std_time'])))
    fig.update_layout(barmode="group")
    st.plotly_chart(fig)


with st.container():
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(" O tempo médio e o desvio padrão de entrega por cidade ")
        cols = ['City', 'Time_taken(min)', 'Type_of_order']
        df_aux = (df1.loc[:, cols]
                  .groupby(['City', 'Type_of_order'])
                  .agg({'Time_taken(min)': ['mean', 'std']}))
        df_aux.columns = ['avg_time', 'std_time']
        df_aux = df_aux.reset_index()
        st.dataframe(df_aux)



    with col2:
        st.markdown("### Tempo médio de entrega por cidade e por tipo de tráfego")
        # Gráfico Sunbust
        df_aux = (df1.loc[:, ['City', 'Time_taken(min)', 'Road_traffic_density']]
                  .groupby(['City', 'Road_traffic_density'])
                  .agg({'Time_taken(min)': ['mean', 'std']}))
        
        df_aux.columns = ['avg_time', 'std_time']
        df_aux = df_aux.reset_index()
        fig = px.sunburst(df_aux, 
                          path=['City', 'Road_traffic_density' ],
                          values='avg_time',
                          color = 'std_time',
                          color_continuous_scale = 'RdBu',
                          color_continuous_midpoint=np.average(df_aux['std_time']))
        st.plotly_chart(fig)


    