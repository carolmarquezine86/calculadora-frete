import streamlit as st
import math
import requests

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Frete Vasto", page_icon="🚚", layout="centered")

# --- CSS AJUSTADO E 100% LEGÍVEL ---
st.markdown("""
    <style>
    /* Fundo suave da página */
    .stApp { 
        background-color: #F8F9FA; 
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }
    
    /* Container centralizado e responsivo */
    .block-container { 
        padding-top: 1rem !important; 
        padding-bottom: 2rem !important; 
        max-width: 520px !important; 
    }
    
    /* HEADER VASTO */
    .vasto-header {
        background-color: #F2C900;
        padding: 20px 25px;
        border-radius: 12px;
        margin-bottom: 25px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 4px 12px rgba(0,0,0,0.06);
    }
    .logo-box {
        background-color: #111;
        color: #F2C900;
        font-weight: 900;
        font-size: 22px;
        padding: 6px 12px;
        border-radius: 8px;
        margin-right: 12px;
    }
    .text-box h1 { margin: 0; font-size: 18px; font-weight: 900; color: #111; letter-spacing: 1px; line-height: 1.1; }
    .text-box p { margin: 0; font-size: 10px; font-weight: 700; color: #111; letter-spacing: 2px; }
    .badge {
        background-color: rgba(0,0,0,0.08);
        padding: 6px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 700;
        color: #111;
    }
    
    /* RÓTULOS DOS CAMPOS COM COR BEM ESCURA */
    label, div[data-testid="stMarkdownContainer"] p {
        color: #111111 !important;
        font-weight: 700 !important;
    }

    /* INPUTS LEGÍVEIS COM BORDA */
    .stTextInput input, .stNumberInput input {
        background-color: #FFFFFF !important;
        color: #111111 !important;
        border: 1px solid #CCCCCC !important;
        border-radius: 8px !important;
        padding: 10px 14px !important;
        font-weight: 600 !important;
    }

    /* BOTÕES DA ESCADA (RADIO) */
    div[role="radiogroup"] {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
    }
    div[role="radiogroup"] > label {
        background-color: #FFFFFF !important;
        border: 1px solid #D1D5DB !important;
        padding: 8px 16px !important;
        border-radius: 20px !important;
        cursor: pointer !important;
        color: #111111 !important;
        font-weight: 600 !important;
    }

    /* BOTÕES INFERIORES */
    .stButton > button {
        border-radius: 10px !important;
        padding: 12px !important;
        font-weight: 800 !important;
        font-size: 15px !important;
        border: none !important;
        width: 100% !important;
        transition: all 0.2s ease !important;
    }
    
    /* Botão Calcular (Amarelo Vasto) */
    div[data-testid="column"]:nth-child(2) .stButton > button {
        background-color: #F2C900 !important; 
        color: #111111 !important;
    }
    div[data-testid="column"]:nth-child(2) .stButton > button:hover {
        background-color: #D6B200 !important;
    }

    /* Botão Limpar (Preto) */
    div[data-testid="column"]:nth-child(1) .stButton > button {
        background-color: #111111 !important;
        color: #FFFFFF !important;
    }
    
    /* RODAPÉ CAROL MARQUEZINE */
    .footer-credits {
        text-align: center;
        margin-top: 35px;
        padding-top: 15px;
        color: #777777;
        font-size: 12px;
        font-weight: 600;
        border-top: 1px solid #E5E7EB;
    }

    /* Ocultar elementos desnecessários da tela */
    header { visibility: hidden; }
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
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

# --- FORMULÁRIO DE ENTRADA ---
peso = st.number_input("Peso total da carga (kg)", min_value=1.0, value=600.0, step=10.0)

escada = st.radio("Lances de escada", ["Sem escada", "1 lance", "2 lances", "3 ou mais lances"])

st.markdown("<hr style='margin: 20px 0; border: none; border-top: 1px solid #E5E7EB;'>", unsafe_allow_html=True)

manual = st.checkbox("Informar a distância manualmente")

distancia_manual = 0.0
cep = ""

if manual:
    distancia_manual = st.number_input("Distância em KM", min_value=0.0, value=0.0, step=1.0)
else:
    cep = st.text_input("CEP de Destino", placeholder="Ex: 01001-000")

# --- BOTÕES ---
st.write("")
col1, col2 = st.columns([1, 1.5])
with col1:
    btn_limpar = st.button("↻ Limpar")
with col2:
    btn_calcular = st.button("🖩 Calcular Frete")

if btn_limpar:
    st.rerun()

# --- EXIBIÇÃO DE RESULTADO ---
if btn_calcular:
    dist = distancia_manual
    if cep and not manual:
        with st.spinner("Calculando rota por CEP..."):
            calc_dist, info = obter_distancia(cep)
            if calc_dist:
                dist = calc_dist
                st.success(f"📍 **Endereço:** {info} ({dist} km)")
            else:
                st.error(info)

    if dist > 0 or (manual and dist == 0):
        res = calcular_frete(peso, escada, dist)
        st.markdown(f"""
            <div style="background-color: #111111; border-left: 6px solid #F2C900; padding: 20px; border-radius: 10px; margin-top: 20px; box-shadow: 0 4px 12px rgba(0,0,0,0.15);">
                <span style="color: #9CA3AF; font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 1px;">Valor Estimado do Frete</span>
                <h1 style="color: #F2C900; margin: 4px 0 10px 0; font-size: 34px; font-weight: 800;">R$ {res['total']:.2f}</h1>
                <p style="color: #E5E7EB; font-size: 13px; margin: 0;">Modalidade: <strong>{res['tipo']}</strong> | Faixa: <strong>{res['faixa']}</strong></p>
            </div>
        """, unsafe_allow_html=True)

# --- RODAPÉ COM ASSINATURA ---
st.markdown("""
    <div class="footer-credits">
        Desenvolvido por Carol Marquezine
    </div>
""", unsafe_allow_html=True)
