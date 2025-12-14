import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import plotly.express as px
import pandas as pd
import numpy as np
import warnings
import folium
from streamlit_folium import st_folium
from prophet import Prophet
from pathlib import Path

# Répertoire racine
BASE_DIR = Path(__file__).parent

warnings.filterwarnings('ignore')

# ---------------------- PARAMÈTRES GÉNÉRAUX ----------------------
st.set_page_config(page_title="Les Derniers Flocons", layout="wide")


# ---------------------- FONCTIONS DE CHARGEMENT ----------------------

@st.cache_data
def load_data_full():
    df_full = pd.read_csv(BASE_DIR / "donnees_meteo_avec_stations_et_altitudes_full.csv")
    df_full['date'] = pd.to_datetime(df_full['date'])
    df_full['year'] = df_full['date'].dt.year

    df_filtered = df_full[df_full['year'] < 2025]
    df_filtered2 = df_full[df_full['date'] < '2024-08-01']
    df_filtered2['season'] = df_filtered2['date'].apply(lambda x: x.year if x.month >= 8 else x.year - 1)

    df_yearly = df_full.groupby('year')[['rain_sum', 'snowfall_water_equivalent_sum']].sum().reset_index()
    df_yearly = df_yearly[df_yearly['year'] != 2025]
    df_yearly_mean = df_filtered.groupby('year')['temperature_2m_mean'].mean().reset_index()
    df_yearly_mean2 = df_filtered.groupby('year')['rain_sum'].mean().reset_index()
    df_yearly_mean3 = df_filtered.groupby('year')['snowfall_sum'].mean().reset_index()

    seasonal_snowfall = df_filtered2.groupby('season')['snowfall_sum'].sum().reset_index()
    seasonal_snowfall['snowfall_sum'] = seasonal_snowfall['snowfall_sum'] / 1000
    seasonal_snowfall = seasonal_snowfall.sort_values('season')

    x1 = df_yearly_mean['year']
    y1 = df_yearly_mean['temperature_2m_mean']
    x2 = df_yearly_mean2['year']
    y2 = df_yearly_mean2['rain_sum']
    x3 = df_yearly_mean3['year']
    y3 = df_yearly_mean3['snowfall_sum']

    coef_quad = np.polyfit(x1, y1, deg=2)
    coef_quad2 = np.polyfit(x2, y2, deg=2)
    coef_quad3 = np.polyfit(x3, y3, deg=2)

    quad_curve = np.poly1d(coef_quad)
    quad_curve2 = np.poly1d(coef_quad2)
    quad_curve3 = np.poly1d(coef_quad3)

    return df_full, x1, y1, x2, y2, x3, y3, df_yearly, seasonal_snowfall, quad_curve, quad_curve2, quad_curve3


@st.cache_data
def load_data_prophet():
    df_prophet = pd.read_csv(BASE_DIR / "donnees_meteo_148_stations.csv")
    stations_fermees = [
        "Alex", "Bozel", "Brison", "Burzier", "Cellier Valmorel", "Chamonix - les Pèlerins",
        "Col de Creusaz", "Col des Aravis", "Col du Champet", "Col du Chaussy", "Col du Frêne",
        "Col du Galibier", "Col du Plainpalais", "Col du Pré", "Col du Sommeiller", "Col du Tamié",
        "Crey Rond", "Doucy en Bauges", "Drouzin-Le-Mont", "Entremont", "Granier sur Aime",
        "Jarrier - La Tuvière", "La Sambuy", "Le Bouchet - Mont Charvin", "Le Cry - Salvagny",
        "Le Petit Bornand", "Les Bossons - Chamonix", "Marthod", "Molliessoulaz", "Montisel",
        "Notre Dame du pré", "Richebourg", "Saint Nicolas la Chapelle", "Saint-Jean de Sixt",
        "Sainte Foy", "Saxel", "Serraval", "Seytroux", "Sixt Fer à Cheval", "St-Pierre d'Entremont",
        "Termignon", "Thônes", "Thorens Glières", "Ugine", "Val Pelouse",
        "Verthemex - Mont du Chat", "Villards sur Thônes"
    ]

    for station in stations_fermees:
        suppression = df_prophet[df_prophet["stations"].apply(lambda x: station in x)].index
        df_prophet = df_prophet.drop(suppression)

    df_prophet = df_prophet.drop(columns=[
        "Unnamed: 0_x", "Unnamed: 0_y", "latitude", "longitude",
        "snowfall_water_equivalent_sum", "wind_speed_10m_mean", "soil_temperature_0_to_100cm_mean",
        "temperature_2m_max", "sunshine_duration", "temperature_2m_mean",
        "cloud_cover_mean", "rain_sum", "temperature_2m_min"
    ], axis=1)

    df_prophet["snowfall_sum"] = df_prophet["snowfall_sum"] / 100

    return df_prophet


@st.cache_data
def load_data_prophet2():
    df_prophet2 = pd.read_csv(BASE_DIR / "donnees_meteo_148_stations.csv")

    stations_fermees = [
        "Alex", "Bozel", "Brison", "Burzier", "Cellier Valmorel", "Chamonix - les Pèlerins",
        "Col de Creusaz", "Col des Aravis", "Col du Champet", "Col du Chaussy", "Col du Frêne",
        "Col du Galibier", "Col du Plainpalais", "Col du Pré", "Col du Sommeiller", "Col du Tamié",
        "Crey Rond", "Doucy en Bauges", "Drouzin-Le-Mont", "Entremont", "Granier sur Aime",
        "Jarrier - La Tuvière", "La Sambuy", "Le Bouchet - Mont Charvin", "Le Cry - Salvagny",
        "Le Petit Bornand", "Les Bossons - Chamonix", "Marthod", "Molliessoulaz", "Montisel",
        "Notre Dame du pré", "Richebourg", "Saint Nicolas la Chapelle", "Saint-Jean de Sixt",
        "Sainte Foy", "Saxel", "Serraval", "Seytroux", "Sixt Fer à Cheval", "St-Pierre d'Entremont",
        "Termignon", "Thônes", "Thorens Glières", "Ugine", "Val Pelouse",
        "Verthemex - Mont du Chat", "Villards sur Thônes"
    ]

    for station in stations_fermees:
        suppression = df_prophet2[df_prophet2["stations"].apply(lambda x: station in x)].index
        df_prophet2 = df_prophet2.drop(suppression)

    df_prophet2 = df_prophet2.drop(columns=[
        "Unnamed: 0_x", "Unnamed: 0_y", "latitude", "longitude",
        "snowfall_water_equivalent_sum", "snowfall_sum", "wind_speed_10m_mean",
        "soil_temperature_0_to_100cm_mean", "temperature_2m_max",
        "sunshine_duration", "cloud_cover_mean", "rain_sum", "temperature_2m_min"
    ], axis=1)

    return df_prophet2


@st.cache_data
def load_data_result():
    return pd.read_csv(BASE_DIR / "df_combined_cox_results.csv")


# ---------------------- CHARGEMENT DES DONNÉES ----------------------
df_meteo_full, x1, y1, x2, y2, x3, y3, df_yearly, seasonal_snowfall, quad_curve, quad_curve2, quad_curve3 = load_data_full()
df_prophet = load_data_prophet()
df_prophet2 = load_data_prophet2()
df_result = load_data_result()


# ---------------------- TITRE ----------------------
st.title("❄️ Les Derniers Flocons")
st.markdown('<style>div.block-container{padding-top:2rem;}</style>', unsafe_allow_html=True)


# ---------------------- TABS ----------------------
tab_accueil, tab_apropos, tab_visualisation, tab_tendances, tab_station, tab_risque = st.tabs([
    "🏠 Accueil",
    "ℹ️ À Propos",
    "📊 Visualisation des Données Météo",
    "📈 Tendances Météorologiques",
    "🌨️ Ma Station",
    "🔍 Stations à Risques"
])

# ====================== ONGLET ACCUEIL ======================
with tab_accueil:
    container_accueil = st.container(border=True)
    container_accueil2 = st.container(border=True)

    # Utiliser df_meteo_full ici pour avoir toutes les stations
    df_map = df_meteo_full.drop_duplicates(subset=['latitude', 'longitude'])

    # Créer la carte de base avec un centre défini et un zoom par défaut
    m = folium.Map(location=[46.0, 7.5], zoom_start=8)

    # Ajouter des marqueurs pour chaque station de ski
    for _, row in df_map.iterrows():
        folium.Marker(
            location=[row['latitude'], row['longitude']],
            popup=f"Station: {row['stations']}<br>Altitude: {row['altitude']}m",
            icon=folium.Icon(color='blue')
        ).add_to(m)

    # Affichage du titre de la page
    container_homeTitle = st.container(border=True)
    container_homeTitle.header("🗺️ Carte des stations de ski des Alpes")

    # Affichage de la carte dans Streamlit
    st_folium(m, width=1500)

    container_accueil2.markdown(
        "Bienvenue sur **Les Derniers Flocons**, un projet visant à fournir des "
        "prédictions quant aux potentielles fermetures des stations de ski alpines."
    )
    container_accueil2.markdown(
        "Réalisation par Ambre TRAN, Andreea LOUISON, Mathilde REJASSE et Nicolas Saad FORTUIT."
    )


# ====================== ONGLET À PROPOS ======================
with tab_apropos:
    container_apropos2 = st.container(border=True)

    texte_apropos = """
***Objectif du projet***  

Le projet « Les Derniers Flocons » vise à anticiper l’impact du changement climatique sur l’activité des stations de ski.
En s’appuyant sur des données météorologiques historiques (depuis 1970) et des modèles de prévision,
l’application estime l’évolution future de la neige et de la température afin de prédire les risques de fermeture des stations à une date donnée.
Cette plateforme, développée sous Streamlit, s’adresse principalement aux professionnels de la montagne (gestionnaires de stations, exploitants touristiques)
ainsi qu’aux décideurs publics.

***Données utilisées***  

Les données proviennent de l’API open-meteo.com et couvrent 148 stations de ski situées dans les Alpes françaises.
Elles intègrent des mesures journalières agrégées :
- Température moyenne de l’air  
- Température du sol (de 0 à -100 cm)  
- Somme des chutes de neige  
- Équivalent en eau des chutes de neige  
- Somme des précipitations pluvieuses  
- Durée d’ensoleillement  
- Vitesse moyenne du vent  
- Couverture nuageuse  
Des informations sur les stations déjà fermées (incluant leur date de fermeture) ont également été collectées afin d’entraîner un modèle prédictif.

***Méthodologie***  

- Collecte & nettoyage des données  
- Scraping des stations de ski (Savoie, Haute-Savoie, Isère)  
- Récupération des coordonnées GPS et de l’altitude  
- Extraction via API des données météorologiques historiques (1970–2024)  
- Intégration des dates de fermeture pour les stations déjà inactives  
- Détection et correction des valeurs aberrantes  

***Analyse exploratoire***  

- Étude des tendances saisonnières et climatiques  
- Comparaisons par altitude et région  

***Modélisation & prévision***  

- Visualisation de l’évolution climatique station par station  
- Modélisation des séries temporelles avec Prophet (températures, neige)  
- Analyse de survie (survival analysis) pour estimer le risque de fermeture dans le temps  

***Perspectives***  

Cette application souhaite contribuer à une meilleure prise de décision pour l’avenir de la montagne.
En éclairant les tendances climatiques locales, elle permet d’anticiper les enjeux liés à l’enneigement,
à l’économie des sports d’hiver et à l’adaptation des territoires alpins face aux changements en cours.
"""

    colAbout1, colAbout2 = st.columns(2)

    with colAbout1:
        container_apropos3 = st.container(border=True)
        container_apropos3.markdown(texte_apropos)

    with colAbout2:
        containerAboutImg = st.container(border=True)
        containerAboutImg.image(BASE_DIR / "image1.png", use_container_width=True)

        containerAboutImg2 = st.container(border=True)
        containerAboutImg2.image(BASE_DIR / "image2.png", use_container_width=True)

        containerAboutImg3 = st.container(border=True)
        containerAboutImg3.image(BASE_DIR / "image3.png", use_container_width=True)


# ====================== ONGLET VISUALISATION DES DONNÉES ======================
with tab_visualisation:
    # -------- Graphique 1 : Températures moyennes annuelles --------
    col_edafig1, col_edaint1 = st.columns(2)

    with col_edafig1:
        container_fig1 = st.container(border=True)
        with container_fig1:
            fig1, ax1 = plt.subplots(figsize=(12, 5))
            ax1.plot(x1, y1, marker='o', color='orange', label='Température moyenne annuelle')

            ax1.set_title("Évolution des températures moyennes annuelles")
            ax1.set_xlabel("Année")
            ax1.set_ylabel("Température moyenne (°C)")
            ax1.grid(True, linestyle='--', alpha=0.5)
            ax1.legend()

            yticks = np.arange(y1.min(), y1.max() + 0.5, 0.5)
            ax1.set_yticks(yticks)
            ax1.set_yticklabels([f"{tick:.2f}" for tick in yticks])
            ax1.set_xticks(range(int(x1.min()), int(x1.max()) + 1, 5))

            plt.tight_layout()
            st.pyplot(fig1)

    with col_edaint1:
        container_titleint1 = st.container(border=True)
        container_int1 = st.container(border=True)
        container_titleint1.markdown("❓ **Interprétation :**")
        texte2 = """Ce graphique montre l'évolution de la température moyenne annuelle au fil des années.

La courbe met en évidence une tendance globale à la hausse des températures, malgré certaines fluctuations d’une année à l’autre.

Cette trajectoire ascendante est cohérente avec les effets du réchauffement climatique, indiquant une augmentation progressive des températures au fil des décennies."""
        container_int1.markdown(texte2)

    # -------- Graphique 2 : Précipitations pluie + neige --------
    col_edafig2, col_edaint2 = st.columns(2)

    with col_edafig2:
        container_fig2 = st.container(border=True)
        with container_fig2:
            fig2, ax2 = plt.subplots(figsize=(10, 8))
            ax2.barh(df_yearly['year'], df_yearly['rain_sum'], label='Pluie', alpha=0.7)
            ax2.barh(
                df_yearly['year'],
                df_yearly['snowfall_water_equivalent_sum'],
                left=df_yearly['rain_sum'],
                label='Neige (équivalent eau)',
                alpha=0.7
            )

            ax2.set_title('Cumul annuel des précipitations (pluie + équivalent neige en eau)', fontsize=14)
            ax2.set_ylabel('Année')
            ax2.set_xlabel('Précipitations totales (mm)')
            ax2.set_yticks(df_yearly['year'])
            ax2.legend()
            ax2.grid(axis='x', linestyle='--', alpha=0.5)
            plt.tight_layout()

            st.pyplot(fig2)

    with col_edaint2:
        container_titleint2 = st.container(border=True)
        container_int2 = st.container(border=True)
        container_titleint2.markdown("❓ **Interprétation :**")
        texte3 = """Ce graphique montre le cumul annuel des précipitations, en séparant pluie et neige (convertie en équivalent eau).

Il permet de visualiser l’évolution globale des précipitations au fil des années.  
Une baisse de la part de neige au profit de la pluie peut refléter les effets du réchauffement climatique,
avec des hivers plus doux et une diminution de l’enneigement naturel."""
        container_int2.markdown(texte3)

    # -------- Graphique 3 : Cumul de neige par saison --------
    col_edafig3, col_edaint3 = st.columns(2)

    with col_edafig3:
        container_fig3 = st.container(border=True)
        with container_fig3:
            fig3, ax3 = plt.subplots(figsize=(10, 6))
            ax3.plot(seasonal_snowfall['season'], seasonal_snowfall['snowfall_sum'],
                     marker='o', color='steelblue')
            ax3.set_xlabel('Saison')
            ax3.set_ylabel('Chutes de neige totales (mètres)')
            ax3.set_title('Cumul des chutes de neige par saison – Toutes stations')
            ax3.grid(True, linestyle='--', alpha=0.5)
            plt.tight_layout()
            st.pyplot(fig3)

    with col_edaint3:
        container_titleint3 = st.container(border=True)
        container_int3 = st.container(border=True)
        container_titleint3.markdown("❓ **Interprétation :**")
        texte4 = """Ce graphique présente le cumul total des chutes de neige par saison, toutes stations confondues.

Chaque point représente la quantité totale de neige tombée pendant une saison hivernale donnée.

On y observe les variations interannuelles : certaines saisons se distinguent par un fort enneigement, d’autres par un cumul plus faible.
Cette visualisation permet de détecter des tendances de long terme, comme une éventuelle diminution progressive des cumuls de neige,
en lien avec le réchauffement climatique."""
        container_int3.markdown(texte4)

# ====================== ONGLET TENDANCES MÉTÉOROLOGIQUES ======================
with tab_tendances:
    colv1, colv2 = st.columns(2)
    with colv1:
        st.container(border=True).subheader("📗 Historiques et prévisions neigeuses par altitude")
    with colv2:
        st.container(border=True).subheader("📘 Historiques et prévisions de températures par altitude")

    # Préparation des données
    df_selection = df_prophet.copy()
    df_selection['ds'] = pd.to_datetime(df_selection['date']).dt.tz_localize(None)
    df_selection = df_selection.rename(columns={'snowfall_sum': 'y'})
    df_selection = df_selection[df_selection['ds'] < "2025-01-01"]

    df_selection2 = df_prophet2.copy()
    df_selection2['ds'] = pd.to_datetime(df_selection2['date']).dt.tz_localize(None)
    df_selection2 = df_selection2.rename(columns={'temperature_2m_mean': 'y'})
    df_selection2 = df_selection2[df_selection2['ds'] < "2025-01-01"]

    def afficher_double_prevision(df_neige, df_temp, condition, titre_neige, titre_temp,
                                  interpretation_neige, interpretation_temp,
                                  ylim_neige=(1, 8), ylim_temp=(0, 12)):

        # Préparation des données neige
        df_n = df_neige[condition]
        df_n = (
            df_n.set_index('ds')
            .resample('YS')
            .agg({'y': 'mean', 'altitude': 'first'})
            .dropna()
            .reset_index()
        )
        df_n['y'] *= 365  # passage en cumul annuel

        # Préparation des données température
        df_t = df_temp[condition]
        df_t = (
            df_t.set_index('ds')
            .resample('YS')
            .agg({'y': 'mean', 'altitude': 'first'})
            .dropna()
            .reset_index()
        )

        col1, col2 = st.columns(2)

        # -------- Neige --------
        if len(df_n) >= 3:
            with col1:
                model_n = Prophet(
                    yearly_seasonality=False,
                    daily_seasonality=False,
                    weekly_seasonality=False,
                    changepoint_prior_scale=1,
                    seasonality_prior_scale=10
                )
                model_n.fit(df_n[['ds', 'y']])
                future_n = model_n.make_future_dataframe(5, freq='YS')
                forecast_n = model_n.predict(future_n)
                fig_n = model_n.plot(forecast_n)
                plt.ylim(ylim_neige)
                plt.title(titre_neige)
                plt.xlabel("Date")
                plt.ylabel("Cumul de neige (m)")
                plt.grid(True, linestyle='--', alpha=0.5)
                st.container(border=True).pyplot(fig_n)

                with st.container(border=True):
                    st.markdown("❓ **Interprétation :**")
                    st.markdown(interpretation_neige)
        else:
            st.warning(f"Pas assez de données pour la prévision neige ({titre_neige}).")

        # -------- Température --------
        if len(df_t) >= 3:
            with col2:
                model_t = Prophet(
                    yearly_seasonality=False,
                    daily_seasonality=False,
                    weekly_seasonality=False,
                    changepoint_prior_scale=1,
                    seasonality_prior_scale=10
                )
                model_t.fit(df_t[['ds', 'y']])
                future_t = model_t.make_future_dataframe(5, freq='YS')
                forecast_t = model_t.predict(future_t)
                fig_t = model_t.plot(forecast_t)
                fig_t.axes[0].get_lines()[0].set_color('darkorange')
                fig_t.axes[0].collections[0].set_facecolor('moccasin')

                plt.ylim(ylim_temp)
                plt.yticks(range(1, 13))
                plt.title(titre_temp)
                plt.xlabel("Date")
                plt.ylabel("Température (°C)")
                plt.grid(True, linestyle='--', alpha=0.5)
                st.container(border=True).pyplot(fig_t)

                with st.container(border=True):
                    st.markdown("❓ **Interprétation :**")
                    st.markdown(interpretation_temp)
        else:
            st.warning(f"Pas assez de données pour la prévision température ({titre_temp}).")

    # -------- 1. Toutes stations confondues --------
    afficher_double_prevision(
        df_selection, df_selection2,
        condition=slice(None),
        titre_neige="Prévision annuelle des chutes de neige - toutes stations",
        titre_temp="Prévision annuelle des températures moyennes - toutes stations",
        interpretation_neige="""
Ce graphique agrège les chutes de neige de toutes les stations météo situées en Savoie, Haute-Savoie et Isère.
Il met en lumière les tendances climatiques globales qui affectent l’ensemble des massifs, toutes altitudes confondues.
On peut ainsi observer si une diminution généralisée du cumul neigeux annuel se dessine, ce qui aurait un impact direct sur l’économie touristique hivernale.
""",
        interpretation_temp="""
Ce graphique regroupe la température moyenne annuelle de toutes les stations.
On y décèle les effets du réchauffement climatique à l’échelle régionale.
L’élévation de la température moyenne sur plusieurs années consécutives est un indicateur fort du bouleversement climatique en cours.
"""
    )

    # -------- 2. Altitude < 1000m --------
    afficher_double_prevision(
        df_selection, df_selection2,
        condition=(df_selection["altitude"] < 1000),
        titre_neige="Neige annuelle - Altitude < 1000m",
        titre_temp="Températures annuelles - Altitude < 1000m",
        interpretation_neige="""
Les zones situées sous 1000 mètres sont les premières à souffrir de la raréfaction de la neige naturelle.
Les hivers doux y entraînent souvent une absence totale de couche neigeuse, ou des périodes très courtes d'enneigement.
Les prévisions ici servent d’alerte pour les stations de basse altitude, souvent dépendantes de la neige de culture.
""",
        interpretation_temp="""
Les températures dans cette tranche sont particulièrement sensibles à la hausse des moyennes hivernales.
Même une faible élévation provoque une disparition progressive des conditions favorables à la neige.
L’évolution actuelle suggère que les hivers seront de moins en moins rigoureux, avec un impact fort sur la biodiversité locale.
"""
    )

    # -------- 3. 1000m à 1300m --------
    afficher_double_prevision(
        df_selection, df_selection2,
        condition=(df_selection["altitude"] >= 1000) & (df_selection["altitude"] < 1300),
        titre_neige="Neige annuelle - 1000 à 1300m",
        titre_temp="Températures annuelles - 1000 à 1300m",
        interpretation_neige="""
Cette tranche d’altitude constitue une zone charnière : encore parfois enneigée naturellement, mais de plus en plus fragile face au réchauffement.
Les prévisions ici permettent d’anticiper l’évolution des conditions pour les petites stations et les zones de moyenne montagne.
""",
        interpretation_temp="""
La température dans cette zone monte plus lentement qu’en plaine, mais les effets s’accumulent.
On observe une tendance de fond à l’augmentation des températures moyennes, ce qui peut compromettre la tenue de la neige sur plusieurs hivers consécutifs.
"""
    )

    # -------- 4. 1300m à 1600m --------
    afficher_double_prevision(
        df_selection, df_selection2,
        condition=(df_selection["altitude"] >= 1300) & (df_selection["altitude"] < 1600),
        titre_neige="Neige annuelle - 1300 à 1600m",
        titre_temp="Températures annuelles - 1300 à 1600m",
        interpretation_neige="""
Ce niveau d’altitude offre encore aujourd’hui de bonnes conditions pour la neige.
Cependant, les prévisions montrent des signes de déclin progressif du cumul annuel, ce qui doit inciter à la vigilance à moyen terme.
""",
        interpretation_temp="""
Les températures restent relativement basses dans cette tranche, mais la hausse progressive risque d’entraîner une réduction de la durée d’enneigement.
C’est une zone stratégique où l’adaptation est encore possible, mais qui nécessitera des investissements pour rester viable.
"""
    )

    # -------- 5. > 1600m --------
    afficher_double_prevision(
        df_selection, df_selection2,
        condition=(df_selection["altitude"] >= 1600),
        titre_neige="Neige annuelle - > 1600m",
        titre_temp="Températures annuelles - > 1600m",
        interpretation_neige="""
Les stations situées au-dessus de 1600 mètres bénéficient encore d’un enneigement régulier et important.
Ces zones sont les plus résilientes face aux changements climatiques, et restent les plus sûres pour les activités de sports d’hiver.
Mais même ici, une baisse tendancielle à long terme pourrait apparaître si le réchauffement se poursuit.
""",
        interpretation_temp="""
Les températures y restent relativement stables, mais l’augmentation lente et continue peut progressivement modifier la qualité de la neige.
Cette altitude est cruciale pour maintenir l’activité touristique hivernale : surveiller son évolution est indispensable à long terme.
"""
    )


# ====================== ONGLET MA STATION ======================
with tab_station:
    st.markdown("## 🔍 Analyse climatique par station", unsafe_allow_html=True)

    station_selectionnee = st.selectbox(
        label="**Sélectionnez une station météo :**",
        options=sorted(df_prophet["stations"].unique()),
        key="station_met",
        label_visibility="visible"
    )

    if station_selectionnee:
        # --- Prévision neige ---
        df_neige_station = df_prophet[df_prophet["stations"] == station_selectionnee].copy()
        df_neige_station['ds'] = pd.to_datetime(df_neige_station['date']).dt.tz_localize(None)
        df_neige_station = df_neige_station.rename(columns={'snowfall_sum': 'y'})
        df_neige_station = df_neige_station[df_neige_station['ds'] < "2025-01-01"]

        df_neige_agg = (
            df_neige_station
            .set_index('ds')
            .resample('YS')
            .agg({'y': 'sum', 'altitude': 'first'})
            .dropna()
            .reset_index()
        )

        # --- Prévision température ---
        df_temp_station = df_prophet2[df_prophet2["stations"] == station_selectionnee].copy()
        df_temp_station['ds'] = pd.to_datetime(df_temp_station['date']).dt.tz_localize(None)
        df_temp_station = df_temp_station.rename(columns={'temperature_2m_mean': 'y'})
        df_temp_station = df_temp_station[df_temp_station['ds'] < "2025-01-01"]

        df_temp_agg = (
            df_temp_station
            .set_index('ds')
            .resample('YS')
            .agg({'y': 'mean', 'altitude': 'first'})
            .dropna()
            .reset_index()
        )

        col1, col2 = st.columns(2)

        # --- Graphique neige ---
        with col1:
            if len(df_neige_agg) >= 3:
                model_neige = Prophet(
                    yearly_seasonality=False,
                    daily_seasonality=False,
                    weekly_seasonality=False,
                    changepoint_prior_scale=1,
                    seasonality_prior_scale=10
                )
                model_neige.fit(df_neige_agg[['ds', 'y']])
                future_neige = model_neige.make_future_dataframe(periods=5, freq='YS')
                forecast_neige = model_neige.predict(future_neige)
                fig_neige = model_neige.plot(forecast_neige)
                plt.title(f"Prévision annuelle des chutes de neige – {station_selectionnee}")
                plt.xlabel("Année")
                plt.ylabel("Cumul neige (m)")
                plt.grid(True, linestyle='--', alpha=0.5)
                plt.tight_layout()
                st.container(border=True).pyplot(fig_neige)

                with st.container(border=True):
                    st.markdown("❓ **Interprétation :**")
                    st.markdown(f"""
Ce graphique montre les prévisions des chutes de neige annuelles pour la station **{station_selectionnee}**.  
Grâce aux données historiques, le modèle **Prophet** extrapole les cumuls de neige possibles jusqu’en 2029.  
La tendance révélée permet d’anticiper la viabilité future de l’activité hivernale à cette altitude.  
Une baisse progressive pourrait indiquer une vulnérabilité accrue aux effets du réchauffement climatique.
""")
            else:
                st.warning("Pas assez de données pour la prévision des chutes de neige.")

        # --- Graphique température ---
        with col2:
            if len(df_temp_agg) >= 3:
                model_temp = Prophet(
                    yearly_seasonality=False,
                    daily_seasonality=False,
                    weekly_seasonality=False,
                    changepoint_prior_scale=1,
                    seasonality_prior_scale=10
                )
                model_temp.fit(df_temp_agg[['ds', 'y']])
                future_temp = model_temp.make_future_dataframe(periods=5, freq='YS')
                forecast_temp = model_temp.predict(future_temp)
                fig_temp = model_temp.plot(forecast_temp)
                fig_temp.axes[0].get_lines()[0].set_color('darkorange')
                fig_temp.axes[0].collections[0].set_facecolor('moccasin')
                plt.title(f"Prévision annuelle des températures moyennes – {station_selectionnee}")
                plt.xlabel("Année")
                plt.ylabel("Température moyenne (°C)")
                plt.grid(True, linestyle='--', alpha=0.5)
                plt.tight_layout()
                st.container(border=True).pyplot(fig_temp)

                with st.container(border=True):
                    st.markdown("❓ **Interprétation :**")
                    st.markdown(f"""
Ce graphique présente l’évolution des **températures moyennes annuelles** enregistrées à **{station_selectionnee}**.  
Le modèle **Prophet** capte les tendances à long terme et projette leur poursuite sur les prochaines années.  
Une pente ascendante signale un réchauffement local progressif, avec des conséquences possibles sur la **durée d’enneigement**, la biodiversité et l’écosystème de montagne.  
C’est un indicateur clé pour suivre l’impact du changement climatique station par station.
""")
            else:
                st.warning("Pas assez de données pour la prévision des températures.")
    else:
        st.info("Veuillez sélectionner une station.")


# ====================== ONGLET STATIONS À RISQUES ======================
with tab_risque:
    container_analyses = st.container()
    col_analyse1, col_analyse2 = st.columns(2)

    # -------- Explication modèle --------
    with col_analyse1:
        modele_1 = st.container()
        modele_1des = st.container()
        container_inter1 = st.container()

        modele_1.header("🧠 Survival Analysis")
        modele_1des.markdown(
            """**L’analyse de survie** est une méthode statistique utilisée pour prédire combien de temps un événement prendra avant de se produire,
ou si un événement se produira ou non, en fonction de différentes variables.

Pour prédire si une station de ski va fermer ou non, l’analyse de survie permet de modéliser la "durée de vie" d'une station avant sa fermeture.
Contrairement à d'autres modèles statiques, elle prend en compte la dimension temporelle et les événements censurés.

C’est une approche pertinente pour comprendre des événements comme la fermeture d'une station de ski,
qui peut dépendre de multiples facteurs sur une longue période."""
        )

        st.subheader("❓ Interprétation des résultats", divider="gray")
        interpretation_text = st.container()
        with interpretation_text:
            st.markdown("""
La courbe de survie est un outil classique pour analyser le temps jusqu'à un événement d’intérêt.

Dans notre cas, la courbe représente la probabilité qu’une station de ski reste ouverte au fil du temps.

- **Axe des x (horizontal)** : le temps en années à partir de 2025.  
- **Axe des y (vertical)** : la probabilité de survie, c’est-à-dire la probabilité que la station ne soit pas fermée à ce moment-là (entre 0 et 1).

Plus la courbe descend, plus le risque de fermeture augmente.
Les comparaisons entre stations permettent d’identifier celles qui sont les plus vulnérables à moyen ou long terme.
""")

    # -------- Résultats + courbes de survie --------
    with col_analyse2:
        container_res1 = st.container()
        container_res1.header("🏆 Résultats")

        def plot_survival_curves(df):
            if df.empty:
                st.write("Les données sont vides !")
                return

            fig, ax = plt.subplots(figsize=(12, 8))

            for idx, row in df.iterrows():
                survie_values = row.iloc[0:65].values[::2]
                station_name = row['station']
                ax.plot(survie_values, label=station_name)

            ax.set_title("Courbes de survie des stations", fontsize=16)
            ax.set_xlabel("Années", fontsize=12)
            ax.set_ylabel("Probabilité de survie", fontsize=12)
            ax.legend(loc='best', bbox_to_anchor=(1, 1))
            ax.grid(True)
            plt.tight_layout()

            st.pyplot(fig)

        def show_survival_curves(df_result):
            if df_result.empty:
                st.write("Les données sont vides !")
                return

            station_names = df_result['station'].tolist()
            selected_stations = st.multiselect(
                "Choisir les stations à afficher",
                station_names
            )
            df_filtered = df_result[df_result['station'].isin(selected_stations)]

            if df_filtered.empty:
                st.write("Aucune station sélectionnée.")
                return

            plot_survival_curves(df_filtered)

        show_survival_curves(df_result)
