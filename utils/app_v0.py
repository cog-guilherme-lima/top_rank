import streamlit as st
from pytrends.request import TrendReq
import pandas as pd
import time
import altair as alt  
import bcrypt

# Configuração de proxies
PROXIES = [
    'http://200.174.198.86:8888',
    'http://85.215.64.49:80',
    'http://162.223.90.130:80',
    'http://159.203.178.26:8080',
    'http://51.89.255.67:80',
    'http://172.191.74.198:8080',
    'http://47.83.192.255:8888',
    'http://165.22.77.86:80',
    'http://113.108.13.120:8083',
    'http://203.89.8.107:80',
    'http://179.107.85.2:8180',
]

def get_trend_instance():
    try:
        # Tenta usar proxies
        pytrends = TrendReq(hl='pt-BR', tz=360, proxies=PROXIES, timeout=(10, 25))
        pytrends.build_payload(["teste"], geo="BR", timeframe="now 1-H")  # Testa a conexão
        print("Usando proxies")
        return pytrends
    except Exception as e:
        print("Falha ao usar proxies:")
        st.warning(f"Falha ao usar proxies: {e}. Tentando sem proxies...")
        # Se falhar, tenta sem proxy
        return TrendReq(hl='pt-BR', tz=360)

st.set_page_config(page_title="Mynd8 | Trends", page_icon="images/icon_cog.png", layout="wide")
pd.set_option('future.no_silent_downcasting', True)

st.markdown(
    """
    <style>
    .stButton > button {
        background-color: #0048ff;  /* Cor de fundo */
        color: white;               /* Cor do texto */
        border: none;               /* Sem borda */
        padding: 10px 20px;         /* Espaçamento interno */
        font-size: 16px;            /* Tamanho da fonte */
        border-radius: 5px;        /* Bordas arredondadas */
    }
    /* Estilo para o botão de download */
    .stDownloadButton > button {
        background-color: #0048ff;  /* Cor de fundo */
        color: white;               /* Cor do texto */
        border: none;               /* Sem borda */
        padding: 10px 20px;         /* Espaçamento interno */
        font-size: 16px;            /* Tamanho da fonte */
        border-radius: 5px;        /* Bordas arredondadas */
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.image(
    "images/icons.png", width=65, use_container_width="never", caption="", output_format="auto"
)

st.markdown("<h1 style='color: #0048ff;'>Análise de Tendências com Google Trends</h1>", unsafe_allow_html=True)

st.markdown("<h3 style='color: #0048ff;'>Por favor, insira o termo que deseja explorar:</h3>", unsafe_allow_html=True)

termo1, termo2 = st.columns(2)

with termo1:
    termo = st.text_input("Termo de Pesquisa:", placeholder="Digite seu termo de interesse aqui...")

with termo2:
    termo2 = st.text_input("Comparar:", placeholder="Digite o termo para comparação...")

col1, col2, col3, col4 = st.columns(4)

with col1:
    countries_dict = {"Brasil": "BR", "Mundo": ""}
    countries_input = st.selectbox("Selecione o país", list(countries_dict.keys()))
    country_code = countries_dict[countries_input]

with col2:
    period_dict = {
        "Última hora": "now 1-H",
        "Últimas 4 horas": "now 4-H",
        "Último dia": "now 1-d",
        "Últimos 7 dias": "now 7-d",
        "Últimos 30 dias": "today 1-m",
        "Últimos 90 dias": "today 3-m",
        "Últimos 12 meses": "today 12-m",
        "Últimos 5 anos": "today 5-y",
        "Desde 2004": "all"
    }
    period_input = st.selectbox("Selecione o período", list(period_dict.keys()))
    period_code = period_dict[period_input]

with col3:
    category_dict = {
        "Todas as categorias": 0,
        "Animais de Estimação e Animais": 66,
        "Artes e Entretenimento": 3,
        "Automóveis e Veículos": 47,
        "Casa e Jardim": 68,
        "Ciência": 107,
        "Comercial e Industrial": 12,
        "Comida e bebida": 71,
        "Compras": 18,
        "Computadores e aparelhos eletrônicos": 5,
        "Comunidades on-line": 174,
        "Condicionamento físico e beleza": 44,
        "Empregos e educação": 958,
        "Esportes": 20,
        "Finanças": 7,
        "Hobbies e lazer": 64,
        "Imóveis": 110,
        "Internet e telecomunicações": 13,
        "Jogos": 8,
        "Lei e governo": 19,
        "Livros e literatura": 22,
        "Notícias": 16,
        "Pessoas e sociedade": 14,
        "Referência": 533,
        "Saúde": 45,
        "Viagens": 67
    }
    category_input = st.selectbox("Selecione a categoria", list(category_dict.keys()))
    category_code = category_dict[category_input]

with col4:
    source_dict = {
        "Pesquisa na Web": "",
        "Pesquisa de Imagem": "images",
        "Pesquisa de Notícias": "news",
        "Google Shopping": "froogle",
        "Pesquisa do YouTube": "youtube"
    }
    source_input = st.selectbox("Selecione a fonte", list(source_dict.keys()))
    source_code = source_dict[source_input]

analysis_type = st.selectbox("Escolha o tipo de análise", ["Interesse ao longo do tempo", "Interesse por região"])

if st.button('Processar dados'):
    if termo and period_code and category_code is not None and source_code is not None:
        with st.spinner('Coletando dados...'):
            pytrends = get_trend_instance()

            def fetch_trend_data(term):
                pytrends.build_payload([term], geo=country_code, timeframe=period_code, cat=category_code, gprop=source_code)
                time.sleep(2)
                df = pytrends.interest_over_time().reset_index()
                if 'isPartial' in df.columns:
                    df.drop(columns=['isPartial'], inplace=True)
                return df

            try:
                if analysis_type == "Interesse ao longo do tempo":
                    if termo2:
                        df1 = fetch_trend_data(termo)
                        time.sleep(5)
                        df2 = fetch_trend_data(termo2)

                        results = pd.merge(df1, df2, on='date', how='outer', suffixes=(f'_{termo}', f'_{termo2}'))
                    else:
                        results = fetch_trend_data(termo)

                    if not results.empty:
                        results.to_csv("dados_trends.csv", index=False)

                        st.markdown("<br>", unsafe_allow_html=True)

                        if analysis_type == "Interesse ao longo do tempo":
                            melted_results = results.melt(id_vars=['date'], var_name='Termo', value_name='Interesse')

                            chart = alt.Chart(melted_results).mark_point(filled=True).encode(
                                x=alt.X('date:T', title='Período'),
                                y='Interesse:Q',
                                color='Termo:N',
                                tooltip=['date:T', 'Termo:N', 'Interesse:Q']
                            ).properties(
                                title='Interesse ao Longo do Tempo',
                                width=800,
                                height=400
                            ) + alt.Chart(melted_results).mark_line().encode(
                                x=alt.X('date:T', title='Período'),
                                y='Interesse:Q',
                                color='Termo:N'
                            ).interactive()

                            chart2 = alt.Chart(melted_results).mark_circle().encode(
                                x=alt.X('date:T', title='Período'),
                                y='Interesse:Q',
                                color='Termo:N',
                                size='Interesse:Q',
                                tooltip=['date:T', 'Termo:N', 'Interesse:Q']
                            ).properties(
                                title='Recorrência dos termos ao longo do tempo',
                                width=800,
                                height=400
                            ).interactive()

                            chart3 = alt.Chart(melted_results).mark_bar().encode(
                                x=alt.X('Interesse:Q', bin=True, title='Interesse'),
                                y=alt.Y('count()', title='Contagem de Registros'),
                                color='Termo:N'
                            ).add_selection(
                                alt.selection_single(fields=['Interesse'], bind='scales', empty='all')
                            ).properties(
                                title='Distribuição Interativa do Interesse',
                                width=800,
                                height=400
                            ).interactive()

                            chart4 = alt.Chart(melted_results).mark_line().encode(
                                x=alt.X('date:T', title='Período'),
                                y='Interesse:Q',
                                color='Termo:N',
                                tooltip=['date:T', 'Termo:N', 'Interesse:Q']
                            ) + alt.Chart(melted_results).mark_area(opacity=0.2).encode(
                                x=alt.X('date:T', title='Período'),
                                y='Interesse:Q',
                                color='Termo:N'
                            ).properties(
                                title='Evolução do Interesse com Margem de Confiança',
                                width=800,
                                height=400
                            ).interactive()

                            st.altair_chart(chart, use_container_width=True)
                            st.altair_chart(chart2, use_container_width=True)
                            st.altair_chart(chart3, use_container_width=True)
                            st.altair_chart(chart4, use_container_width=True)

                            with open("dados_trends.csv", "rb") as file:
                                btn = st.download_button(
                                label="Baixar dados em CSV",
                                data=file,
                                file_name="dados_trends.csv",
                                mime="text/csv"
                            )

                elif analysis_type == "Interesse por região":
                    st.markdown("<br>", unsafe_allow_html=True)
                    if termo2:
                        pytrends.build_payload([termo], geo=country_code, timeframe=period_code, cat=category_code, gprop=source_code)
                        region_data_termo1 = pytrends.interest_by_region(resolution='COUNTRY', inc_low_vol=True, inc_geo_code=False).reset_index()
                        region_data_termo1 = region_data_termo1[['geoName', termo]].rename(columns={termo: f'{termo}'})

                        time.sleep(2)
                        
                        pytrends.build_payload([termo2], geo=country_code, timeframe=period_code, cat=category_code, gprop=source_code)
                        region_data_termo2 = pytrends.interest_by_region(resolution='COUNTRY', inc_low_vol=True, inc_geo_code=False).reset_index()
                        region_data_termo2 = region_data_termo2[['geoName', termo2]].rename(columns={termo2: f'{termo2}'})
                        region_data = pd.merge(region_data_termo1, region_data_termo2, on='geoName', how='outer').fillna(0)
                        region_data_melted = region_data.melt(id_vars=['geoName'], var_name='Termo', value_name='Interesse')

                    else:
                        pytrends.build_payload([termo], geo=country_code, timeframe=period_code, cat=category_code, gprop=source_code)
                        region_data = pytrends.interest_by_region(resolution='COUNTRY', inc_low_vol=True, inc_geo_code=False).reset_index()
                        region_data = region_data[['geoName', termo]].rename(columns={termo: 'Interesse'})
                        region_data['Termo'] = termo 
                        region_data_melted = region_data.rename(columns={'geoName': 'geoName', 'Interesse': 'Interesse', 'Termo': 'Termo'})

                    region_data_melted = region_data_melted.sort_values(by='Interesse', ascending=False)

                    chart = alt.Chart(region_data_melted).mark_bar().encode(
                        x=alt.X('Interesse:Q', title='Interesse'),
                        y=alt.Y('geoName:N', sort='-x', title='Região'),
                        color='Termo:N',
                        tooltip=['geoName:N', 'Termo:N', 'Interesse:Q']
                    ).properties(
                        title=f'Interesse por região para os termos "{termo}" e "{termo2}"' if termo2 else f'Interesse por região para o termo "{termo}"',
                        width=800,
                        height=400
                    )

                    chart2 = alt.Chart(region_data_melted).mark_line().encode(
                        x=alt.X('geoName:N', title='Região'),
                        y='Interesse:Q',
                        color='Termo:N',
                        tooltip=['geoName:N', 'Termo:N', 'Interesse:Q']
                    ).properties(
                        title=f'Interesse por região para os termos "{termo}" e "{termo2}"' if termo2 else f'Interesse por região para o termo "{termo}"',
                        width=800,
                        height=400
                    )

                    chart3 = alt.Chart(region_data_melted).mark_rect().encode(
                        x=alt.X('geoName:N', title='Região'),
                        y='Termo:N',
                        color='Interesse:Q',
                        tooltip=['geoName:N', 'Termo:N', 'Interesse:Q']
                    ).properties(
                        title=f'Mapa de calor do interesse por região para os termos "{termo}" e "{termo2}"' if termo2 else f'Mapa de calor do interesse por região para o termo "{termo}"',
                        width=800,
                        height=400
                    )

                    st.altair_chart(chart, use_container_width=True)
                    st.altair_chart(chart2, use_container_width=True)
                    st.altair_chart(chart3, use_container_width=True)

                    with open("dados_trends.csv", "rb") as file:
                        btn = st.download_button(
                            label="Baixar dados em CSV",
                            data=file,
                            file_name="dados_trends.csv",
                            mime="text/csv"
                        )
                else:
                    st.write("Nenhum dado encontrado para os parâmetros informados.")

            except Exception as e:
                st.error(f"Erro ao coletar os dados: {str(e)}")
    else:
        st.write('Por favor, preencha todos os campos para processar os dados.')

st.markdown("<br>", unsafe_allow_html=True)

st.image(
    "images/logo_cog.png", width=150, use_container_width="never", caption="", output_format="auto"
)
