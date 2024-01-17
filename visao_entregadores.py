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

# Tabelas
tab1, tab2, tab3 = st.tabs(["Visão ...", "", ""])

## Tabela 1

with tab1:
    with st.container():
        col1, col2, col3, col4 = st.columns(4, gap="large")
        with col1:
            st.markdown("##### Maior idade")
            st.write("{}".format(df1.loc[:, 'Delivery_person_Age'].max() ))

            
        with col2:
            st.markdown("##### Menor idade")
            st.write("{}".format(df1.loc[:, 'Delivery_person_Age'].min() ))
        
        with col3:
            st.markdown("##### Melhor condição de veículos")
            st.write('{}'.format(df1.loc[:, 'Vehicle_condition'].min() ))

        with col4:
            st.markdown("##### Pior condição de veículos")
            st.write('{}'.format(df1.loc[:, 'Vehicle_condition'].max() ))
        
    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("##### Avaliação média por entregador")
            st.dataframe(df1.loc[:, ['Delivery_person_Ratings', 'Delivery_person_ID']]
                         .groupby('Delivery_person_ID')
                         .mean().reset_index())

        with col2:
            # Ver depois como separar bem, são dois quadradinhos em uma mesma coluna
            st.markdown("##### Avaliação média por condições trânsito")
            df_avg_std_rating_by_traffic = (df1.loc[:, ['Delivery_person_Ratings', 'Road_traffic_density']]
                                            .groupby('Road_traffic_density')
                                            .agg({'Delivery_person_Ratings': ['mean', 'std']}))
            df_avg_std_rating_by_traffic.columns = ['delivery_mean', 'delivery_std']
            df_avg_std_rating_by_traffic = df_avg_std_rating_by_traffic.reset_index()
            st.dataframe(df_avg_std_rating_by_traffic)

            st.markdown("##### Avaliação média por condições climáticas")
            df_avg_std_rating_by_weatherconditions = (df1.loc[:, [ 'Delivery_person_Ratings','Weatherconditions']]
                                                      .groupby('Weatherconditions')
                                                      .agg({'Delivery_person_Ratings' : ['mean', 'std']}))
            
            df_avg_std_rating_by_weatherconditions.columns = ['delivery_mean', 'delivery_std']
            df_avg_std_rating_by_weatherconditions = df_avg_std_rating_by_weatherconditions.reset_index()
            st.dataframe(df_avg_std_rating_by_weatherconditions)

    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Top entregadores mais rápidos")
            df2 = (df1.loc[:, ['Delivery_person_ID', 'City', 'Time_taken(min)']]
                   .groupby(['City', 'Delivery_person_ID'])
                   .min().sort_values(['City', 'Time_taken(min)']).reset_index())
            df_aux01 = df2.loc[df2['City'] == 'Metropolitian', :].head(10)
            df_aux02 = df2.loc[df2['City'] == 'Urban', :].head(10)
            df_aux03 = df2.loc[df2['City'] == 'Semi-Urban', :].head(10)
            df3 = pd.concat([df_aux01, df_aux02, df_aux03]).reset_index(drop=True)
            
            st.dataframe(df3)

        with col2:
            st.subheader("Top entregadores mais lentos")
            df2 = (df1.loc[:, ['Delivery_person_ID', 'City', 'Time_taken(min)']]
                   .groupby(['City', 'Delivery_person_ID'])
                   .max().sort_values(['City', 'Time_taken(min)'], ascending=False).reset_index())
            
            df_aux01 = df2.loc[df2['City'] == 'Metropolitian', :].head(10)
            df_aux02 = df2.loc[df2['City'] == 'Urban', :].head(10)
            df_aux03 = df2.loc[df2['City'] == 'Semi-Urban', :].head(10)
            df3 = pd.concat([df_aux01, df_aux02, df_aux03]).reset_index(drop=True)

            st.dataframe(df3)
#