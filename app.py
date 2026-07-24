import streamlit as st
import math
import requests

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Frete Vasto", layout="centered", initial_sidebar_state="collapsed")

# --- CSS MÁGICO (Hack para transformar Streamlit em App Nativo) ---
st.markdown("""
    <style>
    /* Fundo do App e margens */
    .stApp { background-color: #F4F5F7; font-family: 'Helvetica Neue', sans-serif; }
    
    /* Ajuste para tela de celular */
    .block-container { 
        padding-top: 0rem !important; 
        padding-bottom: 2rem !important; 
        max-width: 480px !important; 
    }
    
    /* HEADER AMARELO VASTO */
    .vasto-header {
        background-color: #F2C900;
        padding: 40px 20px 20px 20px;
        margin: 0 -2rem 25px -2rem; 
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-radius: 0 0 15px 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    }
    .logo-box {
        background-color: #111;
        color: #F2C900;
        font-weight: 900;
        font-size: 24px;
        padding: 8px 14px;
        border-radius: 8px;
        margin-right: 12px;
    }
    .text-box h1 { margin: 0; font-size: 18px; font-weight: 900; color: #111; letter-spacing: 1px; line-height: 1.1;}
    .text-box p { margin: 0; font-size: 10px; font-weight: 700; color: #111; letter-spacing: 3px; }
    .badge {
        background-color: rgba(0,0,0,0.1);
        padding: 6px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 700;
        color: #111;
    }
    
    /* INPUTS ESTILIZADOS */
    .stTextInput input, .stNumberInput input {
        background-color: #FFF !important;
        border: 1px solid #E0E0E0 !important;
        border-radius: 12px !important;
        padding: 12px 15px !important;
        font-size: 16px !important;
    }

    /* BOTÕES DE ESCADA (Formato Pílula) */
    div[role="radiogroup"] { flex-direction: row; gap: 8px; flex-wrap: wrap; }
    div[role="radiogroup"] > label {
        background-color: #FFF;
        border: 1px solid #E0E0E0;
        padding: 10px 18px;
        border-radius: 30px;
        cursor: pointer;
    }
    /* Estilo do botão selecionado */
    div[role="radiogroup"] > label[aria-checked="true"] {
        background-color: #111 !important;
        border-color: #111 !important;
    }
    div[role="radiogroup"] > label[aria-checked="true"] p {
        color: #F2C900 !important;
        font-weight: bold;
    }

    /* CHECKBOX MANUAL */
    .stCheckbox label p { font-weight: 800 !important; color: #111 !important; font-size: 15px !important;}
    .subtext { color: #888; font-size: 13px; margin-top: -10px; margin-left: 28px; margin-bottom: 20px; }

    /* BOTÕES INFERIORES */
    .stButton > button {
        border-radius: 12px !important;
        padding: 15px !important;
        font-weight: bold !important;
        font-size: 16px !important;
        border: none !important;
        width: 100% !important;
        margin-top: 20px;
    }
    /* Botão Calcular */
    div[data-testid="column"]:nth-child(2) .stButton > button {
        background-color: #9C7A14 !important; 
        color: #111 !important;
    }
    /* Botão Limpar */
    div[data-testid="column"]:nth-child(1) .stButton > button {
        background-color: #111 !important;
        color: #FFF !important;
    }
    
    /* RODAPÉ CAROL MARQUEZINE */
    .footer-credits {
        text-align: center;
        margin-top: 40px;
        padding: 15px 0 10px 0;
        color: #888888;
        font-size: 12px;
        font-weight: 600;
        letter-spacing: 0.5px;
        border-top: 1px solid #E0E0E0;
    }
    
    /* Ocultar barra nativa do Streamlit */
    header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# --- HEADER DO APP ---
st.markdown("""
    <div class="vasto-header">
        <div style="display: flex; align-items: center;">
            <div class="logo-box">V</div>
            <div class="text-box">
                <h1>VASTO</h1>
                <p>ACABAMENTOS</p>
            </div>
        </div>
        <div class="badge"><span style="color: #10B981;">●</span> Online</div>
    </div>
""", unsafe_allow_html=True)

# --- LÓGICA DE CÁLCULO ---
ORIGEM_LAT, ORIGEM_LON = -23.550520, -46.633308

def calcular_frete(peso_kg, escada_op, distancia_km):
    lances = 0
    if escada_op == "1 lance": lances = 1
    elif escada_op == "2 lances": lances = 2
    elif escada_op == "3 ou mais lances": lances = 3

    if peso_kg <= 300:
        tradicional, especial, faixa = 80.0, 120.0, "0 a 300 kg"
    elif peso_kg <= 400:
        tradicional, especial, faixa = 100.0, 150.0, "301 a 400 kg"
    else:
        n = math.ceil((peso_kg - 300) / 100)
        tradicional = 100 + (n - 1) * 10
        especial    = 150 + (n - 1) * 30
        faixa = f"{300 + (n - 1) * 100 + 1} a {300 + n * 100} kg"

    tipo, base = ("Especial", especial) if lances >= 3 else ("Tradicional", tradicional)
    adicional = round((distancia_km - 15) * 6.0, 2) if distancia_km > 15 else 0.0
    
    return {"tipo": tipo, "faixa": faixa, "total": round(base + adicional, 2)}

def obter_distancia(cep_destino):
    try:
        cep = cep_destino.replace("-", "").replace(".", "").strip()
        resp_cep = requests.get(f"https://viacep.com.br/ws/{cep}/json/").json()
        if "erro" in resp_cep: return None, "CEP não encontrado."
        
        end = f"{resp_cep['logradouro']}, {resp_cep['localidade']}, {resp_cep['uf']}, Brasil"
        geo = requests.get(f"https://nominatim.openstreetmap.org/search?format=json&q={end}", headers={'User-Agent': 'VastoApp'}).json()
        if not geo: return None, "Coordenadas não localizadas."

        url = f"http://router.project-osrm.org/route/v1/driving/{ORIGEM_LON},{ORIGEM_LAT};{geo[0]['lon']},{geo[0]['lat']}?overview=false"
        dist_km = requests.get(url).json()['routes'][0]['distance'] / 1000.0
        return round(dist_km, 2), end
    except:
        return None, "Erro ao processar rota."

# --- FORMULÁRIO (INTERFACE) ---
peso = st.number_input("Peso (kg)", min_value=1.0, value=600.0, step=10.0, help="Ex: 600 kg")

st.markdown("<p style='font-size:14px; font-weight:700; color:#333; margin: 15px 0 -15px 0;'>Lances de escada</p>", unsafe_allow_html=True)
escada = st.radio("Escada", ["Sem escada", "1 lance", "2 lances", "3 ou mais lances"], label_visibility="collapsed")

st.markdown("<hr style='margin: 25px 0 15px 0; border: 0.5px solid #EAEAEA;'>", unsafe_allow_html=True)

manual = st.checkbox("Informar a distância manualmente")
st.markdown("<div class='subtext'>Use se a busca automática não localizar a rota.</div>", unsafe_allow_html=True)

distancia_manual = 0.0
cep = ""

if manual:
    distancia_manual = st.number_input("Distância em KM", min_value=0.0, value=0.0, step=1.0)
else:
    cep = st.text_input("CEP de Destino", placeholder="Ex: 01001-000")

# --- BOTÕES (RODAPÉ) ---
col1, col2 = st.columns([1, 1.5])
with col1:
    btn_limpar = st.button("↻ Limpar")
with col2:
    btn_calcular = st.button("🖩 Calcular Frete")

if btn_limpar:
    st.rerun()

# --- RESULTADO ---
if btn_calcular:
    dist = distancia_manual
    if cep and not manual:
        with st.spinner("Calculando rota..."):
            calc_dist, info = obter_distancia(cep)
            if calc_dist:
                dist = calc_dist
                st.success(f"📍 {info} ({dist} km)")
            else:
                st.error(info)

    if dist > 0 or (manual and dist == 0):
        res = calcular_frete(peso, escada, dist)
        st.markdown(f"""
            <div style="background-color: #111; border-left: 6px solid #F2C900; padding: 20px; border-radius: 8px; margin-top: 15px;">
                <span style="color: #888; font-size: 12px; font-weight: 700; text-transform: uppercase;">Valor do Frete</span>
                <h1 style="color: #F2C900; margin: 5px 0; font-size: 34px;">R$ {res['total']:.2f}</h1>
                <p style="color: #FFF; font-size: 13px; margin: 0;">Modalidade: {res['tipo']} | Faixa: {res['faixa']}</p>
            </div>
        """, unsafe_allow_html=True)

# --- RODAPÉ COM A ASSINATURA ---
st.markdown("""
    <div class="footer-credits">
        Desenvolvido por Carol Marquezine
    </div>
""", unsafe_allow_html=True)
