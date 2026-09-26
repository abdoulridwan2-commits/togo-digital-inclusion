"""
Moteur analytique territorial avancé
Togo Digital & Financial Inclusion
Calculs corrigés, indicateurs préfectoraux, score d'inclusion et déserts financiers
"""

from pathlib import Path
import re
import pandas as pd
import numpy as np
import streamlit as st

ROOT_DIR = Path(__file__).resolve().parents[2]
DATA_PROCESSED = ROOT_DIR / "data" / "processed"

# Dictionnaire de correspondance des préfectures togolaises et de leurs régions
PREFECTURE_TO_REGION = {
    # Savanes
    "TONE": "Savanes", "TÔNE": "Savanes",
    "CINKASSE": "Savanes", "CINKASSÉ": "Savanes",
    "KPENDJAL": "Savanes", "KPENDJAL-OUEST": "Savanes",
    "OTI": "Savanes", "OTI-SUD": "Savanes",
    "TANDJOARE": "Savanes", "TANDJOARÉ": "Savanes",
    
    # Kara
    "KOZAH": "Kara",
    "ASSOLI": "Kara",
    "BASSAR": "Kara",
    "BINAH": "Kara",
    "DANKPEN": "Kara",
    "DOUFELGOU": "Kara",
    "KERAN": "Kara", "KÉRAN": "Kara",
    
    # Centrale
    "TCHAOUDJO": "Centrale",
    "BLITTA": "Centrale",
    "SOTOUBOUA": "Centrale",
    "MO": "Centrale", "MÔ": "Centrale",
    "TCHAMBA": "Centrale",
    
    # Plateaux
    "OGOU": "Plateaux",
    "HAHO": "Plateaux",
    "AMOU": "Plateaux",
    "ANIE": "Plateaux", "ANIÉ": "Plateaux",
    "DANYI": "Plateaux",
    "AGOU": "Plateaux",
    "KLOTO": "Plateaux",
    "KPELE": "Plateaux", "KPÉLÉ": "Plateaux",
    "WAWA": "Plateaux",
    "MOYEN-MONO": "Plateaux",
    "EST-MONO": "Plateaux",
    
    # Maritime (hors Grand Lomé)
    "ZIO": "Maritime",
    "VO": "Maritime",
    "LACS": "Maritime",
    "YOTO": "Maritime",
    "AVE": "Maritime", "AVÉ": "Maritime", "TOTOAL AVE": "Maritime",
    "BAS-MONO": "Maritime",
    
    # Grand Lomé (DAGL)
    "GOLFE": "Grand Lomé",
    "AGOE-NYIVE": "Grand Lomé", "AGOÈ-NYIVÉ": "Grand Lomé",
}


def normalize_string(val):
    if not val or pd.isna(val):
        return ""
    s = str(val).strip().upper()
    s = s.replace("É", "E").replace("È", "E").replace("Ê", "E").replace("À", "A").replace("Ô", "O")
    s = re.sub(r"\s+", " ", s)
    return s


def parse_geometry_point(geom):
    """Extrait lon, lat d'une chaîne POINT (x y)."""
    if pd.isna(geom):
        return None, None
    m = re.search(r"POINT\s*\(\s*([-\d.]+)\s+([-\d.]+)\s*\)", str(geom))
    if m:
        return float(m.group(1)), float(m.group(2))
    return None, None


@st.cache_data
def get_clean_geodata():
    """Charge et nettoie les points agents et établissements avec coordonnées."""
    agents_path = DATA_PROCESSED / "agents_mobile_money_clean.csv"
    etabs_path = DATA_PROCESSED / "etablissements_financiers_clean.csv"
    
    agents = pd.read_csv(agents_path) if agents_path.exists() else pd.DataFrame()
    etabs = pd.read_csv(etabs_path) if etabs_path.exists() else pd.DataFrame()
    
    # Parser coordonnées
    if not agents.empty and "geometry" in agents.columns:
        coords = agents["geometry"].map(parse_geometry_point)
        agents["lon"] = [c[0] for c in coords]
        agents["lat"] = [c[1] for c in coords]
        agents["prefecture_norm"] = agents["prefecture"].apply(normalize_string)
        # Assigner Grand Lomé pour le découpage 6 entités
        agents["territoire_6"] = agents.apply(
            lambda r: "Grand Lomé" if normalize_string(r.get("prefecture")) in ["GOLFE", "AGOE-NYIVE"] else r.get("region"),
            axis=1
        )
        
        # Normaliser opérateur
        def clean_op(op):
            if pd.isna(op) or str(op).lower() in ["nsp", "none", "nan", ""]:
                return "Non spécifié"
            op_str = str(op)
            if "Moov" in op_str and "Togocom" in op_str:
                return "Multi-opérateur (Togocom + Moov)"
            if "Togocom" in op_str:
                return "Togocom (T-Money)"
            if "Moov" in op_str:
                return "Moov Africa (Flooz)"
            return op_str
            
        agents["operateur_clean"] = agents["operateur"].apply(clean_op)

    if not etabs.empty and "geometry" in etabs.columns:
        coords = etabs["geometry"].map(parse_geometry_point)
        etabs["lon"] = [c[0] for c in coords]
        etabs["lat"] = [c[1] for c in coords]
        etabs["prefecture_norm"] = etabs["prefecture"].apply(normalize_string)
        etabs["territoire_6"] = etabs.apply(
            lambda r: "Grand Lomé" if normalize_string(r.get("prefecture")) in ["GOLFE", "AGOE-NYIVE"] else r.get("region"),
            axis=1
        )
        
        def clean_cat(cat):
            if pd.isna(cat):
                return "Autre"
            c = str(cat).strip()
            if "Banque" in c:
                return "Banque Commerciale"
            if "Micro" in c or "IMF" in c or "COOPEC" in c:
                return "Microfinance / SFD"
            if "Mutuelle" in c:
                return "Mutuelle d'Épargne"
            if "Assurance" in c:
                return "Assurance"
            return c
            
        etabs["categorie_clean"] = etabs["categorie"].apply(clean_cat)
        
    return agents, etabs


@st.cache_data
def get_population_hierarchy():
    """
    Extrait les populations consolidées officielles RGPH-5 (2022) :
    - Total Togo : 8 095 498
    - Par région (5 officielles)
    - Par territoire (6 avec Grand Lomé)
    - Par préfecture
    """
    pop_path = DATA_PROCESSED / "population_clean.csv"
    if not pop_path.exists():
        return {}, {}, {}
        
    df_pop = pd.read_csv(pop_path)
    
    # 6 Territoires officiels RGPH-5
    # Savanes: 1,143,520; Kara: 985,512; Centrale: 795,529; Plateaux: 1,635,946; Maritime: 1,346,615; DAGL: 2,188,376
    pop_territoire_6 = {
        "Savanes": 1143520,
        "Kara": 985512,
        "Centrale": 795529,
        "Plateaux": 1635946,
        "Maritime": 1346615,      # Hors Grand Lomé
        "Grand Lomé": 2188376,    # District Autonome (Golfe + Agoè-Nyivé)
    }
    
    # 5 Régions officielles historiques (Maritime réunifiée)
    pop_region_5 = {
        "Centrale": 795529,
        "Kara": 985512,
        "Maritime": 1346615 + 2188376,  # 3 534 991 (43.7% du Togo)
        "Plateaux": 1635946,
        "Savanes": 1143520,
    }
    
    # Dictionnaire des populations par préfecture
    pop_prefecture = {}
    known_prefs = [
        "TONE", "CINKASSE", "KPENDJAL", "KPENDJAL-OUEST", "OTI", "OTI-SUD", "TANDJOARE",
        "KOZAH", "ASSOLI", "BASSAR", "BINAH", "DANKPEN", "DOUFELGOU", "KERAN",
        "TCHAOUDJO", "BLITTA", "SOTOUBOUA", "MO", "TCHAMBA",
        "OGOU", "HAHO", "AMOU", "ANIE", "DANYI", "AGOU", "KLOTO", "KPELE", "WAWA", "MOYEN-MONO", "EST-MONO",
        "ZIO", "VO", "LACS", "YOTO", "AVE", "TOTOAL AVE", "BAS-MONO",
        "GOLFE", "AGOE-NYIVE"
    ]
    
    for _, row in df_pop.iterrows():
        decoupage = normalize_string(row.get("découpage_administratif", ""))
        val = row.get("value")
        if pd.notna(val):
            try:
                pop_val = int(val)
                if decoupage in known_prefs:
                    clean_pref = "AVE" if decoupage == "TOTOAL AVE" else decoupage
                    pop_prefecture[clean_pref] = pop_val
            except Exception:
                pass

    return pop_region_5, pop_territoire_6, pop_prefecture


@st.cache_data
def get_indicators_table(mode="5_regions"):
    """
    Retourne la table des indicateurs consolidés.
    mode = '5_regions' (officiel unifié) ou '6_territoires' (avec Grand Lomé séparé)
    """
    agents, etabs = get_clean_geodata()
    pop_5, pop_6, _ = get_population_hierarchy()
    
    if mode == "6_territoires":
        pop_dict = pop_6
        group_col = "territoire_6"
    else:
        pop_dict = pop_5
        group_col = "region"
        
    records = []
    for territory, pop in pop_dict.items():
        sub_agents = agents[agents[group_col].str.lower() == territory.lower()] if not agents.empty else pd.DataFrame()
        sub_etabs = etabs[etabs[group_col].str.lower() == territory.lower()] if not etabs.empty else pd.DataFrame()
        
        nb_agents = len(sub_agents)
        nb_points = len(sub_etabs)
        
        nb_banques = len(sub_etabs[sub_etabs["categorie_clean"] == "Banque Commerciale"]) if not sub_etabs.empty else 0
        nb_micro = len(sub_etabs[sub_etabs["categorie_clean"].isin(["Microfinance / SFD", "Mutuelle d'Épargne"])]) if not sub_etabs.empty else 0
        
        hab_par_agent = round(pop / nb_agents) if nb_agents > 0 else 0
        hab_par_point = round(pop / nb_points) if nb_points > 0 else 0
        ratio_mm_point = round(nb_agents / nb_points, 1) if nb_points > 0 else 0
        
        # Agents pour 10 000 habitants
        agents_par_10k = round((nb_agents / pop) * 10000, 1) if pop > 0 else 0
        # Points pour 100 000 habitants
        points_par_100k = round((nb_points / pop) * 100000, 1) if pop > 0 else 0
        
        # Calcul du Score d'Inclusion Territorial (0-100)
        # Base : combinaison normalisée de la densité MM, des points bancaires et de la microfinance
        score_mm = min(100, (agents_par_10k / 30.0) * 50)  # max benchmark 30 agents / 10k hab
        score_phy = min(100, (points_par_100k / 15.0) * 50) # max benchmark 15 points / 100k hab
        score_inclusion = round(score_mm * 0.6 + score_phy * 0.4, 1)
        
        records.append({
            "territoire": territory,
            "population": pop,
            "nb_agents_mm": nb_agents,
            "nb_points_financiers": nb_points,
            "nb_banques": nb_banques,
            "nb_microfinances": nb_micro,
            "habitants_par_agent_mm": hab_par_agent,
            "habitants_par_point_financier": hab_par_point,
            "ratio_agents_par_point": ratio_mm_point,
            "agents_par_10k_hab": agents_par_10k,
            "points_par_100k_hab": points_par_100k,
            "score_inclusion": score_inclusion,
        })
        
    df = pd.DataFrame(records)
    # Trier par score décroissant
    df = df.sort_values(by="score_inclusion", ascending=False).reset_index(drop=True)
    return df


@st.cache_data
def get_prefecture_indicators():
    """
    Calcule les indicateurs au niveau préfectoral.
    Permet d'identifier les déserts financiers et les champions de l'inclusion.
    """
    agents, etabs = get_clean_geodata()
    _, _, pop_pref = get_population_hierarchy()
    
    # Recenser toutes les préfectures uniques
    prefs_in_data = set(list(PREFECTURE_TO_REGION.keys()))
    if not agents.empty:
        prefs_in_data.update(agents["prefecture_norm"].dropna().unique())
    if not etabs.empty:
        prefs_in_data.update(etabs["prefecture_norm"].dropna().unique())
        
    records = []
    for pref in sorted(prefs_in_data):
        if not pref or pref in ["NSP", "INCONNU", "TOTAL"]:
            continue
            
        region = PREFECTURE_TO_REGION.get(pref, "Autre")
        pop = pop_pref.get(pref, 0)
        
        # Filtre agents
        sub_agents = agents[agents["prefecture_norm"] == pref] if not agents.empty else pd.DataFrame()
        nb_agents = len(sub_agents)
        
        # Filtre etabs
        sub_etabs = etabs[etabs["prefecture_norm"] == pref] if not etabs.empty else pd.DataFrame()
        nb_points = len(sub_etabs)
        nb_banques = len(sub_etabs[sub_etabs["categorie_clean"] == "Banque Commerciale"]) if not sub_etabs.empty else 0
        nb_micro = len(sub_etabs[sub_etabs["categorie_clean"].isin(["Microfinance / SFD", "Mutuelle d'Épargne"])]) if not sub_etabs.empty else 0
        
        hab_par_agent = round(pop / nb_agents) if nb_agents > 0 and pop > 0 else None
        hab_par_point = round(pop / nb_points) if nb_points > 0 and pop > 0 else None
        ratio_mm_point = round(nb_agents / nb_points, 1) if nb_points > 0 else None
        
        # Statut désert financier
        if nb_banques == 0 and nb_points == 0:
            statut_desert = "Désert financier complet (100% dépendant MM)"
        elif nb_banques == 0:
            statut_desert = "Désert bancaire (Microfinance & MM uniquement)"
        elif nb_banques <= 2:
            statut_desert = "Faible desserte bancaire"
        else:
            statut_desert = "Zone bancarisée"
            
        records.append({
            "prefecture": pref.title(),
            "region": region,
            "population": pop,
            "nb_agents_mm": nb_agents,
            "nb_points_financiers": nb_points,
            "nb_banques": nb_banques,
            "nb_microfinances": nb_micro,
            "habitants_par_agent_mm": hab_par_agent,
            "habitants_par_point_financier": hab_par_point,
            "ratio_agents_par_point": ratio_mm_point,
            "statut_desert": statut_desert,
        })
        
    df = pd.DataFrame(records)
    return df
