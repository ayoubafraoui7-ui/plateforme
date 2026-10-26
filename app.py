
import sqlite3
from pathlib import Path

import pandas as pd
import streamlit as st


# =====================================================
# 1. CONFIGURATION
# =====================================================
st.set_page_config(
    page_title="Diabetes | Data Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)


st.markdown("""
<style>
:root {
    --medical-blue: #176B87;
    --deep-blue: #124559;
    --turquoise: #20B8A6;
    --page-bg: #F4F8FB;
    --surface: #FFFFFF;
    --muted: #647985;
    --border: #DCE8EE;
}

html, body, [class*="css"] {
    font-family: "Segoe UI", "Helvetica Neue", sans-serif;
}

[data-testid="stAppViewContainer"],
[data-testid="stMain"],
[data-testid="stHeader"] {
    background: var(--page-bg) !important;
}

[data-testid="stMain"] > div {
    padding-top: 2rem;
    padding-bottom: 3rem;
}

h1, h2, h3, h4 {
    color: var(--deep-blue) !important;
    font-weight: 700 !important;
    letter-spacing: -0.02em;
}

h1 {
    margin-bottom: 0.15rem !important;
}

.subtitle {
    color: var(--muted);
    font-size: 1.05rem;
    margin-top: 0.1rem;
    margin-bottom: 1.8rem;
}

[data-testid="stCaptionContainer"] {
    color: var(--muted);
}

[data-testid="stSidebar"] {
    background: #EAF4F8 !important;
    border-right: 1px solid #D8E8EE;
}

[data-testid="stSidebar"] > div:first-child {
    background: #EAF4F8 !important;
    padding-top: 1.5rem;
}

[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: var(--deep-blue) !important;
}

[data-testid="stSidebar"] [data-testid="stRadio"] label {
    color: var(--deep-blue);
    font-weight: 550;
}

[data-testid="stSidebar"] [data-testid="stRadio"] > div {
    gap: 0.35rem;
}

[data-testid="stSidebar"] [data-testid="stRadio"] label:has(input:checked) {
    color: var(--medical-blue);
    font-weight: 700;
}

[data-testid="stMetric"] {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-left: 4px solid var(--turquoise) !important;
    border-radius: 14px !important;
    padding: 1.1rem 1.25rem !important;
    box-shadow: 0 5px 16px rgba(18, 69, 89, 0.07) !important;
    transition: transform 160ms ease, box-shadow 160ms ease;
}

[data-testid="stMetric"]:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 20px rgba(18, 69, 89, 0.11) !important;
}

[data-testid="stMetricValue"] {
    color: var(--deep-blue) !important;
    font-weight: 800 !important;
}

.stButton > button,
[data-testid="stFormSubmitButton"] > button,
[data-testid="stDownloadButton"] > button {
    background: linear-gradient(115deg, var(--medical-blue), var(--turquoise)) !important;
    color: white !important;
    border: 0 !important;
    border-radius: 10px !important;
    min-height: 2.65rem;
    font-weight: 650 !important;
    box-shadow: 0 4px 10px rgba(23, 107, 135, 0.18);
    transition: transform 150ms ease, box-shadow 150ms ease, filter 150ms ease;
}

.stButton > button:hover,
[data-testid="stFormSubmitButton"] > button:hover,
[data-testid="stDownloadButton"] > button:hover {
    filter: brightness(1.04);
    transform: translateY(-1px);
    box-shadow: 0 6px 14px rgba(23, 107, 135, 0.24);
}

.stButton > button:focus,
[data-testid="stFormSubmitButton"] > button:focus,
[data-testid="stDownloadButton"] > button:focus {
    outline: 3px solid rgba(32, 184, 166, 0.28) !important;
    outline-offset: 2px;
}

[data-testid="stForm"] {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 14px !important;
    padding: 1.35rem !important;
    box-shadow: 0 4px 14px rgba(18, 69, 89, 0.045);
}

[data-testid="stTextInput"] input,
[data-testid="stNumberInput"] input,
[data-testid="stSelectbox"] [data-baseweb="select"] > div,
[data-testid="stTextArea"] textarea {
    border-color: #C9DCE4 !important;
    border-radius: 9px !important;
    background-color: #FFFFFF !important;
}

[data-testid="stTextInput"] input:focus,
[data-testid="stNumberInput"] input:focus,
[data-testid="stTextArea"] textarea:focus {
    border-color: var(--turquoise) !important;
    box-shadow: 0 0 0 2px rgba(32, 184, 166, 0.14) !important;
}

[data-testid="stExpander"] {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 11px;
    overflow: hidden;
}

[data-testid="stDataFrame"] {
    border: 1px solid var(--border) !important;
    border-radius: 11px !important;
    overflow: hidden;
    box-shadow: 0 3px 12px rgba(18, 69, 89, 0.04);
}

[data-testid="stAlert"] {
    border-radius: 10px !important;
}

[data-testid="stHorizontalBlock"] {
    gap: 1rem;
}

hr {
    border-color: var(--border) !important;
    margin-top: 1.35rem !important;
    margin-bottom: 1.35rem !important;
}

@media (max-width: 768px) {
    [data-testid="stMain"] > div {
        padding-top: 1.2rem;
        padding-bottom: 2rem;
    }

    h1 {
        font-size: 1.8rem !important;
    }

    [data-testid="stForm"] {
        padding: 1rem !important;
    }
}
</style>
""", unsafe_allow_html=True)


DB_PATH = Path(__file__).parent / "dwh_diabete.db"



# =====================================================
# 3. CHARGEMENT SQLITE
# =====================================================
@st.cache_data
def load_tables(db_path, db_mtime):
    with sqlite3.connect(db_path) as conn:
        names = pd.read_sql_query("""
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
              AND name NOT LIKE 'sqlite_%'
            ORDER BY name
        """, conn)["name"].tolist()

        result = {}

        for name in names:
            # Échapper les guillemets dans le nom de table
            safe_name = name.replace('"', '""')
            result[name] = pd.read_sql_query(
                f'SELECT * FROM "{safe_name}"',
                conn
            )

    return result


def find_table(tables, keyword):
    """Cherche une table par son nom, sans tenir compte de la casse."""
    for name in tables:
        if keyword.lower() in name.lower():
            return name
    return None


def find_column(df, keywords):
    """Cherche une colonne correspondant à un mot-clé."""
    for col in df.columns:
        normalized = str(col).lower().replace("_", "").replace(" ", "")
        for keyword in keywords:
            if keyword.lower().replace("_", "") in normalized:
                return col
    return None


# =====================================================
# 4. VERIFICATION DE LA BASE
# =====================================================
st.sidebar.title("📊 Diabetes Analytics")
st.sidebar.caption("Plateforme de consultation des données")

if not DB_PATH.exists():
    st.error(
        "Base de données introuvable. "
        "Placez dwh_diabete.db dans le même dossier que app.py."
    )
    st.stop()

try:
    tables = load_tables(
        str(DB_PATH),
        DB_PATH.stat().st_mtime
    )
except Exception as error:
    st.error("Impossible de lire la base SQLite.")
    st.exception(error)
    st.stop()

if not tables:
    st.warning("Aucune table disponible dans la base.")
    st.stop()


fact_name = find_table(tables, "Fait_Hospitalisation")
patient_name = find_table(tables, "Dim_Patient")
diagnostic_name = find_table(tables, "Dim_Diagnostic")
specialite_name = find_table(tables, "Dim_Specialite")

fact_df = tables[fact_name] if fact_name else pd.DataFrame()
patient_df = tables[patient_name] if patient_name else pd.DataFrame()
diagnostic_df = tables[diagnostic_name] if diagnostic_name else pd.DataFrame()
specialite_df = tables[specialite_name] if specialite_name else pd.DataFrame()


# =====================================================
# 5. NAVIGATION
# =====================================================
page = st.sidebar.radio(
    "Navigation",
    [
        "Vue générale",
        "Analyse des hospitalisations",
        "Exploration des données",
        "Qualité des données",
        "Structure SQLite",
        "Administration",
    ],
)
st.sidebar.divider()
st.sidebar.caption(f"{len(tables)} tables détectées dans SQLite")


# =====================================================
# 6. TITRE
# =====================================================
st.title("📊 Diabetes Data Analytics")
st.markdown(
    '<p class="subtitle">Modélisation et intégration des données hospitalières</p>',
    unsafe_allow_html=True
)


# =====================================================
# 7. DASHBOARD PRINCIPAL
# =====================================================
if page == "Vue générale":

    st.subheader("Vue générale")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Tables disponibles", len(tables))

    c2.metric(
        "Hospitalisations",
        f"{len(fact_df):,}" if fact_name else "N/D"
    )

    c3.metric(
        "Patients référencés",
        f"{len(patient_df):,}" if patient_name else "N/D"
    )

    c4.metric(
        "Diagnostics référencés",
        f"{len(diagnostic_df):,}" if diagnostic_name else "N/D"
    )

    st.divider()

    left, right = st.columns(2)

    with left:
        st.subheader("Répartition des données")

        counts = pd.DataFrame({
            "Table": list(tables.keys()),
            "Nombre de lignes": [
                len(df) for df in tables.values()
            ],
        })

        st.bar_chart(
            counts.set_index("Table"),
            y="Nombre de lignes"
        )

    with right:
        st.subheader("Informations sur la base")

        total_rows = sum(len(df) for df in tables.values())

        st.write(f"**Nombre total de tables :** {len(tables)}")
        st.write(f"**Total des lignes dans les tables :** {total_rows:,}")
        st.write(f"**Base SQLite :** `{DB_PATH.name}`")

        st.caption(
            "Le total des lignes additionne les tables de faits "
            "et de dimensions. Il ne représente pas un nombre "
            "de patients uniques."
        )

    st.divider()
    st.subheader("Aperçu des hospitalisations")

    if fact_name:
        st.caption(f"Source : {fact_name}")
        st.dataframe(
            fact_df.head(10),
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info(
            "La table Fait_Hospitalisation n'a pas été détectée. "
            "Consultez la page Structure SQLite."
        )


# =====================================================
# 8. ANALYSE DES HOSPITALISATIONS
# =====================================================

elif page == "Analyse des hospitalisations":

   
    st.subheader("Analyse interactive des hospitalisations")

    if fact_df.empty:
        st.warning("Aucune donnée disponible dans Fait_Hospitalisation.")
        st.stop()

    # Copie de la table de faits
    analysis_df = fact_df.copy()

    # Filtres interactifs
    st.markdown("### Filtres")

    filter_cols = st.columns(3)
    selected_specialty = None
    selected_diagnostic = None
    selected_year = None

    specialty_key = find_column(
        analysis_df,
        ["specialite_key", "specialty_key"]
    )
    diagnostic_key = find_column(
        analysis_df,
        ["diag_key", "diagnostic_key"]
    )
    date_key = find_column(
        analysis_df,
        ["date_key"]
    )

    with filter_cols[0]:
        if specialty_key and specialite_name:
            specialty_values = sorted(
                analysis_df[specialty_key].dropna().unique().tolist(),
                key=str
            )
            selected_specialty = st.selectbox(
                "Spécialité",
                ["Toutes"] + specialty_values,
                key="filter_specialty"
            )

    with filter_cols[1]:
        if diagnostic_key and diagnostic_name:
            diagnostic_values = sorted(
                analysis_df[diagnostic_key].dropna().unique().tolist(),
                key=str
            )
            selected_diagnostic = st.selectbox(
                "Diagnostic",
                ["Tous"] + diagnostic_values,
                key="filter_diagnostic"
            )

    with filter_cols[2]:
        if date_key:
            years = (
                analysis_df[date_key]
                .dropna()
                .astype(str)
                .str[:4]
            )
            years = sorted(years.unique().tolist())

            if years:
                selected_year = st.selectbox(
                    "Année",
                    ["Toutes"] + years,
                    key="filter_year"
                )

    # Application des filtres
    if selected_specialty is not None and selected_specialty != "Toutes":
        analysis_df = analysis_df[
            analysis_df[specialty_key] == selected_specialty
        ]

    if selected_diagnostic is not None and selected_diagnostic != "Tous":
        analysis_df = analysis_df[
            analysis_df[diagnostic_key] == selected_diagnostic
        ]

    if selected_year is not None and selected_year != "Toutes":
        analysis_df = analysis_df[
            analysis_df[date_key]
            .astype(str)
            .str.startswith(selected_year)
            | analysis_df[date_key]
            .astype(str)
            .str.startswith(selected_year + "01")
        ]

    st.divider()

    # KPI mises à jour selon les filtres
    k1, k2, k3 = st.columns(3)

    k1.metric(
        "Hospitalisations filtrées",
        f"{len(analysis_df):,}"
    )

    patient_key = find_column(
        analysis_df,
        ["patient_key"]
    )

    if patient_key:
        patient_count = analysis_df[patient_key].nunique()
        k2.metric("Patients distincts", f"{patient_count:,}")
    else:
        k2.metric("Patients distincts", "N/D")

    k3.metric(
        "Colonnes disponibles",
        len(analysis_df.columns)
    )

    st.markdown("### Répartition des hospitalisations")

    chart_cols = st.columns(2)

    with chart_cols[0]:
        if specialty_key:
            st.markdown("**Par spécialité (clé)**")
            st.bar_chart(
                analysis_df[specialty_key]
                .value_counts()
                .sort_index()
            )
        else:
            st.info("Clé de spécialité indisponible.")

    with chart_cols[1]:
        if diagnostic_key:
            st.markdown("**Par diagnostic (clé)**")
            st.bar_chart(
                analysis_df[diagnostic_key]
                .value_counts()
                .sort_index()
                .head(15)
            )
        else:
            st.info("Clé de diagnostic indisponible.")

    st.markdown("### Données filtrées")
    st.dataframe(
        analysis_df,
        use_container_width=True,
        hide_index=True
    )

    st.download_button(
        "Télécharger les résultats filtrés",
        data=analysis_df.to_csv(index=False).encode("utf-8-sig"),
        file_name="hospitalisations_filtrees.csv",
        mime="text/csv"
    )



# =====================================================
# 9. EXPLORATION DES DONNEES
# =====================================================
elif page == "Exploration des données":

    st.subheader("Exploration des données")

    selected_table = st.selectbox(
        "Choisir une table",
        list(tables.keys())
    )

    df = tables[selected_table]

    col1, col2 = st.columns(2)
    col1.metric("Nombre de lignes", f"{len(df):,}")
    col2.metric("Nombre de colonnes", len(df.columns))

    search = st.text_input(
        "Rechercher dans toutes les colonnes",
        placeholder="Saisir une valeur..."
    )

    filtered = df.copy()

    if search:
        mask = filtered.astype(str).apply(
            lambda col: col.str.contains(
                search,
                case=False,
                na=False,
                regex=False
            )
        ).any(axis=1)

        filtered = filtered[mask]

    st.write(f"Résultats : {len(filtered):,} lignes")

    st.dataframe(
        filtered,
        use_container_width=True,
        hide_index=True,
        height=450
    )

    st.download_button(
        "⬇️ Télécharger en CSV",
        data=filtered.to_csv(index=False).encode("utf-8-sig"),
        file_name=f"{selected_table}.csv",
        mime="text/csv",
    )


# =====================================================
# 10. QUALITE DES DONNEES
# =====================================================
elif page == "Qualité des données":

    st.subheader("Contrôle de la qualité des données")

    selected_table = st.selectbox(
        "Table à contrôler",
        list(tables.keys()),
        key="quality_table"
    )

    df = tables[selected_table]

    missing_by_column = df.isna().sum()

    quality = pd.DataFrame({
        "Colonne": df.columns,
        "Valeurs manquantes": [
            int(missing_by_column[col]) for col in df.columns
        ],
        "Pourcentage manquant (%)": [
            round(
                100 * missing_by_column[col] / len(df), 2
            ) if len(df) else 0
            for col in df.columns
        ],
        "Valeurs distinctes": [
            int(df[col].nunique(dropna=True))
            for col in df.columns
        ],
    })

    q1, q2, q3 = st.columns(3)

    q1.metric("Lignes", f"{len(df):,}")
    q2.metric("Colonnes", len(df.columns))
    q3.metric(
        "Lignes dupliquées",
        f"{int(df.duplicated().sum()):,}"
    )

    st.markdown("#### Valeurs manquantes par colonne")
    st.dataframe(
        quality,
        use_container_width=True,
        hide_index=True
    )

    if len(df.columns):
        missing_chart = quality.set_index("Colonne")[
            "Valeurs manquantes"
        ]

        st.bar_chart(missing_chart)

    st.caption(
        "Cette page mesure les valeurs NULL/NaN et les doublons exacts "
        "dans chaque table. Les valeurs codées par '?' ou 'Unknown' "
        "ne sont pas automatiquement considérées comme manquantes."
    )


# =====================================================
# 11. STRUCTURE SQLITE
# =====================================================
elif page == "Structure SQLite":

    st.subheader("Structure de la base de données")

    st.write(f"**Fichier :** `{DB_PATH.name}`")

    with sqlite3.connect(DB_PATH) as conn:
        schema = pd.read_sql_query("""
            SELECT name AS table_name, sql AS creation_sql
            FROM sqlite_master
            WHERE type = 'table'
              AND name NOT LIKE 'sqlite_%'
            ORDER BY name
        """, conn)

    st.dataframe(
        schema[["table_name"]],
        use_container_width=True,
        hide_index=True
    )

    for table_name, table_df in tables.items():
        with st.expander(
            f"{table_name} — {len(table_df):,} lignes"
        ):
            st.write("Colonnes :", ", ".join(map(str, table_df.columns)))
            st.write("Dimensions :", table_df.shape)

            st.dataframe(
                table_df.head(10),
                use_container_width=True,
                hide_index=True
            )

            row = schema[schema["table_name"] == table_name]

            if not row.empty and pd.notna(row.iloc[0]["creation_sql"]):
                st.code(row.iloc[0]["creation_sql"], language="sql")


# =====================================================
# 12. ESPACE ADMINISTRATEUR
# =====================================================
elif page == "Administration":

    st.subheader("🔐 Espace Administrateur")
    st.write(
        "Ajouter une nouvelle hospitalisation "
        "dans la base de données SQLite."
    )

    st.warning(
        "Version locale de démonstration. "
        "Changez le mot de passe avant toute utilisation réelle."
    )

    
    # Mot de passe de démonstration
    # Connexion Administration

    if "admin_connecte" not in st.session_state:
        st.session_state["admin_connecte"] = False

    if not st.session_state["admin_connecte"]:
        with st.form("connexion_admin"):
            username = st.text_input("Nom d'utilisateur")
            password = st.text_input(
                "Mot de passe administrateur",
                type="password"
            )
            connexion = st.form_submit_button("Se connecter")

        if connexion:
            if username.strip().lower() == "admin" and password == "1234":
                st.session_state["admin_connecte"] = True
                st.rerun()
            else:
                st.error("Identifiant ou mot de passe incorrect.")

        st.stop()

    if st.button("🚪 Déconnexion"):
        st.session_state["admin_connecte"] = False
        st.rerun()


    # Récupération des clés existantes
    def get_key_values(table_name, possible_keys):
        if not table_name or table_name not in tables:
            return []

        dimension = tables[table_name]
        key_col = find_column(dimension, possible_keys)

        if not key_col:
            return []

        return dimension[key_col].dropna().drop_duplicates().tolist()

    patient_keys = get_key_values(
        patient_name, ["patient_key"]
    )
    date_keys = get_key_values(
        find_table(tables, "Dim_Temps"), ["date_key"]
    )
    diagnostic_keys = get_key_values(
        diagnostic_name, ["diag_key", "diagnostic_key"]
    )
    specialty_keys = get_key_values(
        specialite_name, ["specialite_key", "specialty_key"]
    )

    st.markdown("### Nouvelle hospitalisation")

    # ==========================================
    # AJOUTER UN PATIENT
    # ==========================================
    st.divider()
    st.markdown("### 👤 Ajouter un patient")

    with st.form("form_ajouter_patient"):

        id_patient = st.text_input(
            "Identifiant anonymisé du patient"
        )

        genre = st.selectbox(
            "Genre",
            ["Female", "Male", "Non renseigné"]
        )

        race = st.selectbox(
            "Race",
            [
                "Caucasian",
                "AfricanAmerican",
                "Asian",
                "Hispanic",
                "Other",
                "Non renseigné"
            ]
        )

        tranche_age = st.selectbox(
            "Tranche d'âge",
            ["0-30", "30-55", "55-60", "60+", "Non renseigné"]
        )

        ajouter_patient = st.form_submit_button(
            "💾 Enregistrer le patient"
        )

    if ajouter_patient:

        id_patient = id_patient.strip()

        if not id_patient:
            st.error("L'identifiant anonymisé est obligatoire.")

        elif patient_name is None:
            st.error("Table Dim_Patient introuvable.")

        elif id_patient in tables[patient_name][
            "id_patient_anonyme"
        ].astype(str).values:
            st.error("Cet identifiant existe déjà.")

        else:
            try:
                with sqlite3.connect(DB_PATH) as conn:

                    # Vérifier les clés déjà utilisées
                    keys = pd.read_sql_query(
                        """
                        SELECT patient_key
                        FROM Dim_Patient
                        """,
                        conn
                    )["patient_key"]

                    keys = pd.to_numeric(keys, errors="coerce").dropna()

                    next_key = (
                        int(keys.max()) + 1
                        if not keys.empty else 1
                    )

                    conn.execute(
                        """
                        INSERT INTO Dim_Patient (
                            id_patient_anonyme,
                            genre,
                            race,
                            tranche_age,
                            patient_key
                        )
                        VALUES (?, ?, ?, ?, ?)
                        """,
                        (
                            id_patient,
                            genre,
                            race,
                            tranche_age,
                            next_key
                        )
                    )

                    conn.commit()

                load_tables.clear()

                st.success(
                    f"Patient ajouté avec succès ! "
                    f"Patient key : {next_key}"
                )

                st.rerun()

            except sqlite3.Error as error:
                st.error(f"Erreur SQLite : {error}")

    with st.form("add_hospitalisation_form"):

        encounter_id = st.number_input(
            "Identifiant de l'hospitalisation",
            min_value=1,
            step=1
        )

        if not patient_keys or not date_keys:
            st.error(
                "Les clés des dimensions Patient ou Temps "
                "n'ont pas été détectées."
            )
            st.stop()

        patient_key = st.selectbox(
            "Patient existant",
            patient_keys
        )

        date_key = st.selectbox(
            "Date",
            date_keys
        )

        if diagnostic_keys:
            diag_key = st.selectbox(
                "Diagnostic",
                diagnostic_keys
            )
        else:
            diag_key = None
            st.warning("Aucune clé de diagnostic disponible.")

        if specialty_keys:
            specialite_key = st.selectbox(
                "Spécialité",
                specialty_keys
            )
        else:
            specialite_key = None
            st.warning("Aucune clé de spécialité disponible.")

        st.markdown("#### Informations sur le séjour")

        time_in_hospital = st.number_input(
            "Durée du séjour (jours)",
            min_value=1,
            value=1
        )

        num_lab_procedures = st.number_input(
            "Nombre de procédures de laboratoire",
            min_value=0,
            value=0
        )

        num_procedures = st.number_input(
            "Nombre de procédures",
            min_value=0,
            value=0
        )

        num_medications = st.number_input(
            "Nombre de médicaments",
            min_value=0,
            value=0
        )

        number_diagnoses = st.number_input(
            "Nombre de diagnostics",
            min_value=0,
            value=1
        )

        number_outpatient = st.number_input(
            "Visites ambulatoires",
            min_value=0,
            value=0
        )

        number_emergency = st.number_input(
            "Visites aux urgences",
            min_value=0,
            value=0
        )

        number_inpatient = st.number_input(
            "Hospitalisations antérieures",
            min_value=0,
            value=0
        )

        a1c_result = st.selectbox(
            "Résultat HbA1c",
            ["Non mesuré", "Norm", ">7", ">8"]
        )

        insulin = st.selectbox(
            "Insuline",
            ["No", "Steady", "Up", "Down"]
        )

        diabetes_med = st.selectbox(
            "Médicament contre le diabète",
            ["Yes", "No"]
        )

        readmitted = st.selectbox(
            "Réadmission",
            ["NO", "<30", ">30"]
        )

        submitted = st.form_submit_button(
            "💾 Enregistrer l'hospitalisation"
        )

    if submitted:

        fact_columns = [
            "encounter_id",
            "patient_key",
            "date_key",
            "diag_key",
            "specialite_key",
            "time_in_hospital",
            "num_lab_procedures",
            "num_procedures",
            "num_medications",
            "number_diagnoses",
            "number_outpatient",
            "number_emergency",
            "number_inpatient",
            "A1Cresult",
            "insulin",
            "diabetesMed",
            "readmitted",
        ]

        values = [
            int(encounter_id),
            patient_key,
            date_key,
            diag_key,
            specialite_key,
            time_in_hospital,
            num_lab_procedures,
            num_procedures,
            num_medications,
            number_diagnoses,
            number_outpatient,
            number_emergency,
            number_inpatient,
            a1c_result,
            insulin,
            diabetes_med,
            readmitted,
        ]

        actual_columns = set(fact_df.columns)

        if not set(fact_columns).issubset(actual_columns):
            st.error(
                "Les colonnes de Fait_Hospitalisation ne correspondent "
                "pas au formulaire. Vérifiez la structure SQLite."
            )

        elif diag_key is None or specialite_key is None:
            st.error(
                "Impossible d'enregistrer : une clé de dimension manque."
            )

        else:
            try:
                with sqlite3.connect(DB_PATH) as conn:
                    exists = conn.execute(
                        """
                        SELECT 1
                        FROM Fait_Hospitalisation
                        WHERE encounter_id = ?
                        LIMIT 1
                        """,
                        (int(encounter_id),)
                    ).fetchone()

                    if exists:
                        st.error(
                            "Cet identifiant existe déjà. "
                            "Choisissez un identifiant différent."
                        )
                    else:
                        placeholders = ", ".join(
                            ["?"] * len(fact_columns)
                        )
                        columns_sql = ", ".join(
                            f'"{col}"' for col in fact_columns
                        )

                        conn.execute(
                            f"""
                            INSERT INTO Fait_Hospitalisation
                            ({columns_sql})
                            VALUES ({placeholders})
                            """,
                            values
                        )
                        conn.commit()

                        load_tables.clear()
                        st.success(
                            "Hospitalisation ajoutée avec succès !"
                        )
                        st.rerun()

            except sqlite3.Error as error:
                st.error(
                    f"Erreur SQLite : {error}"
                )

# =====================================================
# 12. FOOTER
# =====================================================
