import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
from streamlit_option_menu import option_menu
from PIL import Image


st.set_page_config(page_title="Tableau de Bord Énergétique", layout="wide")


@st.cache_data
def load_data():
    data = pd.read_csv('departement.csv',sep=';')  
    return data


st.markdown("---")


st.markdown("""
    <style>
    .footer {
        font-size: 0.8em;
        text-align: center;
        color: #6c757d;
    }
    </style>
    <div class="footer">
        © 2024 Dany Costa. All rights reserved.
    </div>
    """, unsafe_allow_html=True)

logo = Image.open("logo-efrei.65d4f0ab.png")


departement = load_data()

rename_dict = {
    "energie_produite_annuelle_photovoltaique_enedis_mwh": "Energie Photovoltaique",
    "energie_produite_annuelle_eolien_enedis_mwh": "Energie Eolienne",
    "energie_produite_annuelle_hydraulique_enedis_mwh": "Energie Hydraulique",
    "energie_produite_annuelle_bio_energie_enedis_mwh": "Bio Energie",
    "energie_produite_annuelle_autres_filieres_enedis_mwh": "Autres Filières"
}


departement = departement.rename(columns=rename_dict)


with st.sidebar:
    st.image(logo, use_column_width=True)
    selected = option_menu("Menu", ["Portfolio", 'Project DataViz (Enedis french energie)',"Context"], 
        icons=['person', 'search'], menu_icon="house", default_index=0)
    st.title("Contact Information")
    
   
    st.write("Feel free to check my profile and reach out to me on:")

    st.markdown("[Linkedin](https://www.linkedin.com/in/-costa-dany/)")
    st.markdown('[GitHub](https://github.com/Foxykav2?tab=repositories)')
    
    
    st.write("You can also download my CV here:")
    st.download_button(label="Download CV", data=open('CV_Dany_Costa.pdf', 'rb').read(), file_name='Dany_Costa_CV.pdf', mime='application/pdf')
    
    


if selected == "Portfolio":
    st.title("Welcome to My Data Visualization Dashboard!")
    
    st.write("""
        This dashboard showcases my skills in **Data Visualization**, **data analysis**, and **programming**.
        Through various interactive graphs, I demonstrate my ability to process and visualize complex datasets
        to extract meaningful insights. It is a reflection of my proficiency with tools such as **Python**, **Pandas**, 
        **Matplotlib**, **Seaborn**, and **Plotly**, which are essential for any professional in **Data Science**.
    """)
    
    st.subheader("About Me")
    st.write("""
        I am **Dany Costa**, a **Master's student in Data Engineering** at **EFREI Paris**, passionate about **Data Science**, 
        **Machine Learning**, and solving real-world problems through data. This project is a glimpse of what I am capable of
        when it comes to data analysis and developing interactive dashboards.
    """)
    
    st.subheader("Cover Letter")
    st.write("""
        I am currently in the **Master's in Data Engineering** program, in my 4th year at **EFREI Paris**, and I am looking for a 
        five-month internship starting from **November 4, 2024**, until **April 6, 2025**. My areas of interest include **Data Science**, 
        **data analysis**, **Machine Learning**, and learning new technologies.

        Throughout my academic journey, I have developed a deep passion for data science and solving complex problems through data analysis. 
        I have honed my programming skills, particularly in **Python** and **SQL**, and I am proficient with tools such as **Pandas**, 
        **Scikit-learn**, **Numpy**, and **Matplotlib**. During academic projects, I have applied these skills, especially in processing 
        and visualizing data through interactive dashboards.

        My international experience in **Poland** has also strengthened my autonomy and adaptability to new technical environments. 
        Furthermore, during my previous internship at **Loxam Power**, I developed customer communication skills, which has made me more 
        comfortable engaging with both clients and colleagues. My **teamwork skills**, **organizational sense**, and **initiative** 
        are assets that will allow me to contribute effectively to your projects.

        I would be delighted to discuss my skills and motivations during an interview. I appreciate your consideration of my profile and 
        look forward to the opportunity to contribute to your company.

        **Best regards, Dany Costa**
    """)
    st.subheader("Interested in My Profile?")
    st.write("""
    If you're interested in learning more about my background or considering me for a position, please don't hesitate to **contact me** via LinkedIn or explore my projects on GitHub. You can find the links in the sidebar.
    """)

    
    st.write("Thank you for your time, and I hope you enjoy exploring my work!")

elif selected == "Project DataViz (Enedis french energie)":
    
    st.title("Annual Electricity Production by Energy Source (2011 - 2023)")
    
    st.write("""
        This dashboard visualizes the **annual electricity production** by green energy source at the **department level** 
        from **2011 to 2023**. The data is provided by **Enedis**, a major electricity distribution operator in France, 
        responsible for managing and maintaining the majority of the electricity grid.

        The production values for each energy type are represented in **megawatt-hours (MWh)**. Below are the energy sources:
        
        - **Energie Photovoltaique**: Solar power generation
        - **Energie Eolienne**: Wind power generation
        - **Energie Hydraulique**: Hydropower generation
        - **Bio Energie**: Energy from biomass
        - **Autres Filières**: Other energy sources
    """)
   
    
    energy_sources = ["Energie Photovoltaique", "Energie Eolienne", "Energie Hydraulique", "Bio Energie", "Autres Filières"]
    
    selected_energy = st.selectbox("Select the energy type to visualize over time:", energy_sources, key="energy_select_line")
    
    # 1. Graphique 1 : Total Electricity Production by Selected Energy Type Over Time
    st.subheader("Total Annual Energy Production by Region Over Time")
    plt.figure(figsize=(10, 6))
    sns.lineplot(x='annee', y=selected_energy, hue='nom_region', data=departement.groupby(['annee', 'nom_region']).sum().reset_index())
    plt.title(f"Total {selected_energy} Production by Region Over Time")
    plt.ylabel("Energy Produced (MWh)")
    plt.show()
    st.pyplot(plt)

    # 2. Graphique 2 : Distribution of Energy Sources by Department
    st.subheader("Stacked Bar Chart of Energy Production by Source Across Departments")
    department_sum = departement.groupby('nom_departement')[energy_sources].sum().reset_index()

    department_sum.plot(kind='bar', stacked=True, x='nom_departement', figsize=(12, 7))
    plt.title("Distribution of Energy Sources by Department")
    plt.ylabel("Energy Produced (MWh)")
    plt.xticks(rotation=90)
    plt.show()
    st.pyplot(plt)

    # 3. Graphique 3 : Photovoltaic Energy Production Distribution by Year
    st.subheader("Distribution of Energy Production by Year for Selected Energy Source")
    selected_energy_box = st.selectbox("Select the energy type for the boxplot:", energy_sources, key="energy_select_box")

    plt.figure(figsize=(10, 6))
    sns.boxplot(x='annee', y=selected_energy_box, data=departement)
    plt.title(f"{selected_energy_box} Production Distribution by Year")
    plt.ylabel("Energy Produced (MWh)")
    plt.show()
    st.pyplot(plt)

    # 4. Graphique 4 : Proportion of Energy Sources in 2020
    st.subheader("Proportion of Energy Sources in 2020")
    year_data = departement[departement['annee'] == 2020][energy_sources].sum()
    year_data.plot(kind='pie', autopct='%1.1f%%', figsize=(8, 8))
    plt.title("Proportion of Energy Sources in 2020")
    plt.ylabel("")
    st.pyplot(plt)

    # 5. Graphique 5 : Energy Flow from Regions to Sources (Sankey Diagram)

    st.subheader("Energy Flow from Regions to Sources")
    labels = list(departement['nom_region'].unique()) + energy_sources
    region_indices = list(range(len(departement['nom_region'].unique())))
    energy_indices = list(range(len(departement['nom_region'].unique()), len(labels)))

    links = {'source': [], 'target': [], 'value': []}
    for i, region in enumerate(departement['nom_region'].unique()):
        region_data = departement[departement['nom_region'] == region]
        total_by_source = region_data[energy_sources].sum()
        for j, energy in enumerate(energy_sources):
            if total_by_source[energy] > 0:
                links['source'].append(i)
                links['target'].append(len(departement['nom_region'].unique()) + j)
                links['value'].append(total_by_source[energy])

    fig = go.Figure(go.Sankey(
        node=dict(pad=15, thickness=20, line=dict(color="black", width=0.5), label=labels),
        link=dict(source=links['source'], target=links['target'], value=links['value'])
    ))
    st.plotly_chart(fig)

   # 6. Graphique 6 : Sunburst de la Production d'Énergie par Région et Département
    st.subheader("Sunburst Chart of Energy Production by Region and Department")
    regions = departement['nom_region'].unique()
    selected_region = st.selectbox("Sélectionnez une région:", ["Tous"] + list(regions), key='sunburst_region_selection')

    default_energy = 'Energie Photovoltaique'  
    if selected_region == "Tous":
        filtered_data = departement
    else:
        filtered_data = departement[departement['nom_region'] == selected_region]

    if default_energy in filtered_data.columns:
        if filtered_data[default_energy].sum() > 0:
            # Create the Sunburst chart
            fig = px.sunburst(filtered_data, path=['nom_region', 'nom_departement'], values=default_energy,
                            title="Répartition de la Production d'Énergie par Région et Département", color=default_energy)
            st.plotly_chart(fig)
        else:
            st.warning(f"Aucune donnée disponible pour le type d'énergie '{default_energy}' dans cette région.")
    else:
        st.error(f"La colonne '{default_energy}' n'existe pas dans les données.")

    # 7. Graphique 7 : Radar Chart de la Production d'Énergie par Département
    st.subheader("Polar Plot of Energy Production by Department")
    selected_energy_radar = st.selectbox("Sélectionnez le type d'énergie pour le radar chart:", energy_sources)

   
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111, polar=True)
    categories = list(departement['nom_departement'].unique())
    angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
    data = departement.groupby('nom_departement')[selected_energy_radar].sum().fillna(0).tolist()
    data += data[:1]
    angles += angles[:1]
    ax.fill(angles, data, color='red', alpha=0.25)
    ax.plot(angles, data, color='red')
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, fontsize=8)
    plt.title(f'Production d\'Énergie Photovoltaïque par Département ({selected_energy_radar})')
    st.pyplot(plt)

elif selected == "Context":
    st.title("Project Context")

    st.write("""
    This project is part of the 4th-year study programme at **EFREI Paris**, within the Data Visualization course **ST2DVZ - Data Visualization (I2 - 2425S7)**. 
    The goal of the project is to apply various data visualization techniques to effectively analyze and represent datasets.
             
    The course was taught by **Mano Joseph Mathew**, an **Enseignant-Chercheur** at EFREI Paris, 
    with expertise in **IT & Data IA**.
    """)

    st.markdown("""
    ### Project Objectives:
    - Explore and analyze the dataset using different types of visualizations
    - Provide insights on annual electricity production by energy type and region in France (in my case)
    - Develop an interactive dashboard for data exploration

    This dashboard showcases my skills in **data visualization**, **Python programming**, and the use of different python libraries 

    Feel free to explore the project and interact with the visualizations!
    """)
