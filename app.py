import streamlit as st

# --- CONFIGURAZIONE PAGINA ---
st.set_page_config(
    page_title="WWM Builder",
    page_icon="⚔️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- STILE CSS PERSONALIZZATO (Opzionale, per renderlo più carino) ---
st.markdown("""
<style>
    .big-font { font-size:20px !important; }
    .stMetric { background-color: #f0f2f6; padding: 10px; border-radius: 10px; }
</style>
""", unsafe_allow_html=True)

# --- TITOLO ---
st.title("⚔️ WWM Companion: Build & Combat Assistant")
st.markdown("*Tool sperimentale per creare build e ottenere suggerimenti tattici.*")

# --- SIDEBAR (Opzioni) ---
with st.sidebar:
    st.header("⚙️ Configurazione")
    st.write("Seleziona il tuo equipaggiamento:")
    
    weapon_main = st.selectbox(
        "Arma Principale", 
        ["Stormbreaker Spear", "Panacea Fan", "Thundercry Blade", "Soulshade Umbrella"]
    )
    
    weapon_sub = st.selectbox(
        "Arma Secondaria", 
        ["Thundercry Blade", "Soulshade Umbrella", "Stormbreaker Spear", "Panacea Fan"],
        index=1 # Seleziona la seconda opzione di default
    )
    
    armor_set = st.selectbox(
        "Set Armatura", 
        ["Moonflare Set (Tank)", "Verdantia Set (Healer)", "Rainwhisper Set (HP)", "Lifeweaver Set (Crit Heal)"]
    )
    
    st.divider()
    st.subheader("Statistiche Attuali")
    hp_base = st.number_input("Max HP", 5000, 100000, 35000, step=500)
    atk_power = st.number_input("Attack / Heal Power", 100, 10000, 2500, step=50)

# --- CORPO PRINCIPALE ---
col1, col2 = st.columns([1, 1.5]) # Colonna destra un po' più larga

with col1:
    st.subheader("📊 Analisi Build")
    
    # LOGICA DI RICONOSCIMENTO RUOLO
    role = "Sconosciuto / Ibrido"
    role_color = "gray"
    
    # Tank Logic
    if "Spear" in weapon_main and "Blade" in weapon_sub:
        role = "🛡️ TANK (Meta Build)"
        role_color = "blue"
        st.info(f"**Ruolo Rilevato:** {role}")
        
        # Calcoli specifici Tank
        shield_val = int(hp_base * 0.25)
        st.metric("Valore Scudo (Blade Q)", f"{shield_val} HP", "Basato sul 25% Max HP")
        
        if "Moonflare" in armor_set:
            st.success("✅ **Sinergia Set:** Moonflare è perfetto per questa build!")
        else:
            st.warning("⚠️ **Consiglio:** Prova il Moonflare Set per massimizzare lo scudo.")

    # Healer Logic
    elif "Fan" in weapon_main and "Umbrella" in weapon_sub:
        role = "🏥 HEALER (Meta Build)"
        role_color = "green"
        st.success(f"**Ruolo Rilevato:** {role}")
        
        # Calcoli specifici Healer
        single_heal = int(atk_power * 1.2)
        burst_heal = int(atk_power * 1.8)
        st.metric("Cura Singola (Fan Q)", f"{single_heal} HP", "Moltiplicatore 1.2x")
        st.metric("Burst Charge (Umbrella)", f"{burst_heal} HP", "Moltiplicatore 1.8x")
        
        if "Verdantia" in armor_set:
            st.success("✅ **Sinergia Set:** Verdantia aumenta le tue cure del 15%.")
    
    else:
        st.write(f"Build personalizzata: **{weapon_main}** + **{weapon_sub}**")
        st.info("Questa combinazione non ha calcoli preimpostati nel database.")

with col2:
    st.subheader("💡 Combat Assistant")
    
    tab1, tab2 = st.tabs(["🔄 Rotazione", "📝 Checklist"])
    
    with tab1:
        if "Tank" in role:
            st.markdown("### 🛡️ Rotazione Aggro & Survival")
            st.code("""
1. [INGAGGIO] Spear Q (Storm Roar) -> Prendi Aggro
2. [DEBUFF]   Spear E (Thunder Shock) -> Applica Vulnerability
3. [SWITCH]   Cambia arma (Tasto T)
4. [SCUDO]    Blade Q (Predator's Shield) -> Proteggiti
5. [DANNO]    Blade Caricato -> Fai danno
6. [PARATA]   Tieni Click Destro mentre aspetti i cooldown
            """, language="text")
            st.caption("Nota: Tieni sempre d'occhio il buff Vulnerability sul boss.")
            
        elif "Healer" in role:
            st.markdown("### 🏥 Rotazione Supporto")
            st.code("""
1. [BASE]     Fan Q (Healing Bloom) -> Cura chi serve
2. [REGEN]    Fan E (Regeneration Aura) -> Cura nel tempo
3. [RESOURCE] Attacca col ventaglio per rigenerare DEW
4. [SWITCH]   Cambia arma se serve Burst Heal
5. [BURST]    Umbrella Charge Lv3 -> Grande cura area
            """, language="text")
        
        else:
            st.write("Seleziona una combinazione nota (es. Spear + Blade) per vedere la rotazione suggerita.")

    with tab2:
        st.write("Prima di iniziare il Boss:")
        if "Tank" in role:
            st.checkbox("Golden Bell Body Equipaggiato?", value=True)
            st.checkbox("Cibo buff HP consumato?")
            st.checkbox("Il Healer sa che stai per pullare?")
        elif "Healer" in role:
            st.checkbox("Risorsa DEW al massimo (100)?")
            st.checkbox("Sei posizionato DIETRO il Tank?")
            st.checkbox("Hai il tasto per il Target Lock pronto?")
        else:
            st.write("Nessuna checklist specifica disponibile.")

# --- FOOTER ---
st.divider()
st.text("WWM Builder v0.1 - Creato con Streamlit e 'Antigravity'")
