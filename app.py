import streamlit as st

# --- CONFIGURAZIONE PAGINA ---
st.set_page_config(
    page_title="WWM Builder v2.0",
    page_icon="⚔️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- DATABASE DATI (Espandibile) ---
# Qui è dove i tuoi amici possono aiutarti a raccogliere i dati veri!
WEAPON_DATA = {
    "Stormbreaker Spear": {
        "role": "Tank",
        "stat_prio": "Max HP",
        "q_skill": "Storm Roar (Taunt + DR)",
        "e_skill": "Thunder Shock (Vuln)",
        "desc": "L'arma definitiva per l'aggro e la sopravvivenza."
    },
    "Thundercry Blade": {
        "role": "Tank/DPS",
        "stat_prio": "HP / Attack",
        "q_skill": "Predator's Shield (Shield)",
        "e_skill": "Rush Gale (Pull)",
        "desc": "Ottima per scudi e controllo folla."
    },
    "Panacea Fan": {
        "role": "Healer",
        "stat_prio": "Healing Power",
        "q_skill": "Healing Bloom (Single Heal)",
        "e_skill": "Regen Aura (HoT)",
        "desc": "Cure continue e supporto per il team."
    },
    "Soulshade Umbrella": {
        "role": "Healer/Support",
        "stat_prio": "Healing Power",
        "q_skill": "Dew Shield (Shield)",
        "e_skill": "Purify Wind (Cleanse)",
        "desc": "Protezione burst e rimozione debuff."
    },
    "Galeforce Bow": {
        "role": "DPS Ranged",
        "stat_prio": "Crit / Attack",
        "q_skill": "Piercing Shot (Dmg)",
        "e_skill": "Rain of Arrows (AoE)",
        "desc": "Danno sicuro dalla distanza."
    },
    "Shadow Daggers": {
        "role": "DPS Melee",
        "stat_prio": "Crit / Agility",
        "q_skill": "Backstab (Crit)",
        "e_skill": "Poison Coat (DoT)",
        "desc": "Danno esplosivo ma rischioso."
    },
    "Wuji Sword": {
        "role": "DPS Balanced",
        "stat_prio": "Attack / Parry",
        "q_skill": "Sword Qi (Ranged)",
        "e_skill": "Deflect (Parry)",
        "desc": "Equilibrio perfetto tra attacco e difesa."
    }
}

SETS_DATA = {
    "Moonflare Set": {"type": "Tank", "bonus": "Scudo su parata (30%)"},
    "Verdantia Set": {"type": "Healer", "bonus": "+15% Cure"},
    "Rainwhisper Set": {"type": "Survival", "bonus": "+HP Massimi"},
    "Lifeweaver Set": {"type": "Healer", "bonus": "Crit Heals x2"},
    "Crimson Edge": {"type": "DPS", "bonus": "+20% Crit Dmg"},
    "Windwalker": {"type": "DPS", "bonus": "+Attack Speed"}
}

# --- SIDEBAR ---
with st.sidebar:
    st.header("⚙️ Configurazione Eroe")
    
    # Selezione Armi dalle chiavi del dizionario
    weapon_list = list(WEAPON_DATA.keys())
    
    w_main = st.selectbox("Arma Principale", weapon_list, index=0)
    w_sub = st.selectbox("Arma Secondaria", weapon_list, index=1)
    
    st.divider()
    armor = st.selectbox("Set Armatura", list(SETS_DATA.keys()))
    
    st.divider()
    st.subheader("Stats Attuali")
    hp = st.slider("Max HP", 5000, 100000, 35000, 500)
    atk = st.slider("Attack / Heal Power", 100, 10000, 2500, 50)
    crit = st.slider("Crit Rate %", 0, 100, 15, 1)

# --- LOGICA ---
main_data = WEAPON_DATA[w_main]
sub_data = WEAPON_DATA[w_sub]
set_info = SETS_DATA[armor]

# Determinazione Archetipo
archetype = "Ibrido / Custom"
if main_data['role'] == "Tank" and sub_data['role'] in ["Tank", "Tank/DPS"]:
    archetype = "🛡️ MAIN TANK"
elif "Healer" in main_data['role'] and "Healer" in sub_data['role']:
    archetype = "🏥 PURE HEALER"
elif "DPS" in main_data['role'] and "DPS" in sub_data['role']:
    archetype = "⚔️ PURE DPS"

# --- INTERFACCIA PRINCIPALE ---
st.title(f"Analisi Build: {archetype}")
st.markdown(f"**Setup:** {w_main} + {w_sub} | **Set:** {armor}")

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Arma 1 (Main)")
    st.info(f"**{w_main}**")
    st.write(f"🎯 Ruolo: {main_data['role']}")
    st.write(f"✨ Q: {main_data['q_skill']}")
    st.write(f"⚡ E: {main_data['e_skill']}")
    st.caption(main_data['desc'])

with col2:
    st.subheader("Arma 2 (Sub)")
    st.success(f"**{w_sub}**")
    st.write(f"🎯 Ruolo: {sub_data['role']}")
    st.write(f"✨ Q: {sub_data['q_skill']}")
    st.write(f"⚡ E: {sub_data['e_skill']}")
    st.caption(sub_data['desc'])

with col3:
    st.subheader("🔢 Calcoli Teorici")
    
    # Calcoli Tank
    if "Tank" in archetype:
        shield = int(hp * 0.25)
        eff_hp = int(hp * 1.4) # Considerando DR
        st.metric("Scudo Max", f"{shield}", "Blade/Spear Skill")
        st.metric("EHP (Effective HP)", f"{eff_hp}", "+40% DR active")
        if set_info['type'] == "Tank":
            st.write("✅ Bonus Set Attivo!")
        else:
            st.warning("⚠️ Set non ottimale per Tank")
            
    # Calcoli Healer
    elif "Healer" in archetype:
        base_heal = int(atk * 1.2)
        if set_info['type'] == "Healer":
            base_heal = int(base_heal * 1.15)
            st.write("✅ Bonus Set +15% applicato")
        
        st.metric("Cura Base", f"{base_heal}", "Skill Q")
        st.metric("Crit Heal", f"{int(base_heal * 2)}", f"{crit}% Chance")
        
    # Calcoli DPS
    else:
        dps_score = int(atk * (1 + (crit/100)))
        st.metric("DPS Score", f"{dps_score}", "Stima grezza")
        st.write("⚠️ I calcoli DPS sono approssimativi senza dati sui frame.")

st.divider()

# --- SUGGERITORE ROTAZIONE ---
st.subheader("🔄 Rotazione Suggerita (Generata)")

rotazione = []
rotazione.append(f"1. Usa **{main_data['q_skill']}** per ingaggiare.")
rotazione.append(f"2. Usa **{main_data['e_skill']}** per applicare effetti.")
rotazione.append(f"3. **CAMBIO ARMA** (T)")
rotazione.append(f"4. Scarica **{sub_data['q_skill']}**.")
rotazione.append(f"5. Usa **{sub_data['e_skill']}** se disponibile.")

if "Tank" in archetype:
    rotazione.append("6. **PARATA** fino al reset dei cooldown.")
elif "Healer" in archetype:
    rotazione.append("6. **Attacchi Base** per rigenerare DEW.")
else:
    rotazione.append("6. Continua con attacchi base fino ai cooldown.")

for passo in rotazione:
    st.text(passo)
