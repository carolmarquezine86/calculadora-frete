import streamlit as st
import math
import requests
import base64
import os

# --- VERIFICA SE EXISTE ÍCONE PERSONALIZADO ---
icone_path = "icone.png" if os.path.exists("icone.png") else ("logo.png" if os.path.exists("logo.png") else "🚚")

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Frete Vasto", page_icon=icone_path, layout="centered")

# --- FUNÇÃO PARA CARREGAR A LOGO / ÍCONE EM BASE64 ---
def get_image_base64(filename):
    if os.path.exists(filename):
        with open(filename, "rb") as img_file:
            ext = filename.split('.')[-1]
            return base64.b64encode(img_file.read()).decode(), ext
    return None, None

logo_b64, logo_ext = get_image_base64("logo.png") or get_image_base64("logo.jpg")
icone_file = "icone.png" if os.path.exists("icone.png") else "logo.png"
icon_b64, icon_ext = get_image_base64(icone_file)

# --- FORÇAR "VA" AMARELO NO PC E LOGO COMPLETA NO CELULAR (PWA) ---
favicon_svg = '''data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><rect width="100" height="100" rx="20" fill="%23111111"/><text x="50%" y="58%" font-family="Arial, sans-serif" font-weight="900" font-size="52" fill="%23F2C900" text-anchor="middle" dominant-baseline="middle">VA</text></svg>'''

apple_touch_icon_html = ""
if icon_b64:
    mime = "jpeg" if icon_ext.lower() == "jpg" else icon_ext.lower()
    apple_touch_icon_html = f'<link rel="apple-touch-icon" href="data:image/{mime};base64,{icon_b64}">'

st.markdown(f"""
    <head>
        <link rel="icon" type="image/svg+xml" href="{favicon_svg}">
        {apple_touch_icon_html}
    </head>
""", unsafe_allow_html=True)

# --- CSS COM ALINHAMENTO PERFEITO DA LOGO E BOTÕES AMARELOS ---
st.markdown("""
    <style>
    /* Fundo geral da aplicação */
    .stApp { 
        background-color: #F8F9FA; 
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }
    
    /* Largura máxima e espaçamento */
    .block-container { 
        padding-top: 1rem !important; 
        padding-bottom: 2rem !important; 
        max-width: 480px !important; 
    }
    
    /* HEADER VASTO COM LOGO PERFEITAMENTE CENTRALIZADA */
    .vasto-header {
        background-color: transparent;
        padding: 5px 0px 15px 0px;
        margin-bottom: 10px;
        text-align: center;
        width: 100%;
        display: flex;
        justify-content: center;
        align-items: center;
    }
    
    .vasto-header img {
        width: 100% !important;
        max-width: 320px !important;
        height: auto !important;
        object-fit: contain !important;
        display: block !important;
        margin: 0 auto !important;
    }

    /* CARD SAÍDA DO CD */
    .cd-card {
        background-color: #111111;
        border-radius: 12px;
        padding: 14px 18px;
        color: white;
        margin-bottom: 20px;
    }
    .cd-label { color: #F2C900; font-size: 10px; font-weight: 800; letter-spacing: 1px; }
    .cd-address { font-size: 14px; font-weight: 800; color: #FFFFFF; margin-top: 2px; }
    .cd-city { font-size: 11px; color: #9CA3AF; }

    /* RÓTULOS E TEXTOS DA PÁGINA */
    label, p, span, div[data-testid="stMarkdownContainer"] p, div[data-testid="stMarkdownContainer"] h3 {
        color: #111111 !important;
        font-weight: 700 !important;
    }

    /* INPUTS */
    .stTextInput input, .stNumberInput input {
        background-color: #FFFFFF !important;
        border: 1.5px solid #D1D5DB !important;
        border-radius: 8px !important;
        color: #111111 !important;
        font-weight: 700 !important;
    }

    /* === ESTILIZAÇÃO DOS BOTÕES (AMBOS AMARELOS COM FONTE PRETA) === */
    .stButton > button, button[kind="secondary"] {
        background-color: #F2C900 !important;
        color: #111111 !important;
        border: 2px solid #F2C900 !important;
        border-radius: 10px !important;
        padding: 12px 20px !important;
        font-weight: 900 !important;
        font-size: 15px !important;
        width: 100% !important;
        transition: all 0.2s ease-in-out !important;
        cursor: pointer !important;
    }

    .stButton > button *, button[kind="secondary"] * {
        color: #111111 !important;
        font-weight: 900 !important;
    }

    .stButton > button:hover, button[kind="secondary"]:hover,
    .stButton > button:active, button[kind="secondary"]:active,
    .stButton > button:focus, button[kind="secondary"]:focus {
        background-color: #FFFFFF !important;
        color: #111111 !important;
        border-color: #111111 !important;
    }
    .stButton > button:hover *, button[kind="secondary"]:hover *,
    .stButton > button:active *, button[kind="secondary"]:active *,
    .stButton > button:focus *, button[kind="secondary"]:focus * {
        color: #111111 !important;
    }

    /* CORREÇÃO DE MÉTRICAS */
    div[data-testid="stMetricValue"] {
        color: #111111 !important;
        font-weight: 900 !important;
        font-size: 20px !important;
    }
    div[data-testid="stMetricLabel"] p {
        color: #6B7280 !important;
        font-weight: 700 !important;
        font-size: 12px !important;
    }

    /* CAIXA AMARELA DE VALOR TOTAL */
    .result-total-box {
        background-color: #F2C900;
        border-radius: 12px;
        padding: 18px 20px;
        margin-top: 15px;
        text-align: left;
    }
    .result-total-box .total-label {
        color: #111111 !important;
        font-size: 11px !important;
        font-weight: 900 !important;
        letter-spacing: 1.5px;
        display: block;
        margin-bottom: 4px;
    }
    .result-total-box .total-value {
        color: #111111 !important;
        font-size: 34px !important;
        font-weight: 900 !important;
        line-height: 1;
        margin: 0;
    }

    /* RODAPÉ */
    .footer-credits {
        text-align: center;
        margin-top: 35px;
        padding-top: 15px;
        color: #6B7280;
        font-size: 12px;
        font-weight: 600;
        border-top: 1px solid #E5E7EB;
    }

    header { visibility: hidden; }
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    </style>
""", unsafe_allow_html=True)

# --- HEADER VASTO COM LOGO CENTRALIZADA ---
if logo_b64:
    mime_ext = "jpeg" if logo_ext.lower() == "jpg" else logo_ext.lower()
    html_logo = f'<img src="data:image/{mime_ext};base64,{logo_b64}" alt="Vasto Logo">'
else:
    html_logo = '<h1 style="margin: 0; font-size: 26px; font-weight: 900; color: #111; letter-spacing: 1px; text-align: center;">VASTO ACABAMENTOS</h1>'

st.markdown(f"""
    <div class="vasto-header">
        {html_logo}
    </div>
""", unsafe_allow_html=True)

st.markdown("<h2 style='font-size: 22px; font-weight: 900; margin-bottom: 2px; color: #111;'>Calculadora de Frete</h2>", unsafe_allow_html=True)
st.markdown("<p style='font-size: 13px; color: #6B7280; margin-bottom: 20px;'>Informe o CEP e os dados da entrega para gerar o valor.</p>", unsafe_allow_html=True)

# --- CARD SAÍDA DO CD ---
st.markdown("""
    <div class="cd-card">
        <div class="cd-label">SAÍDA DO CD</div>
        <div class="cd-address">📍 Rua Paulino Nunes Esposo, 120</div>
        <div class="cd-city">São Paulo — SP</div>
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
        base, faixa = (80.0, "0 a 300 kg") if lances < 3 else (120.0, "0 a 300 kg")
    elif peso_kg <= 400:
        base, faixa = (100.0, "301 a 400 kg") if lances < 3 else (150.0, "301 a 400 kg")
    else:
        n = math.ceil((peso_kg - 300) / 100)
        tradicional = 100 + (n - 1) * 10
        especial = 150 + (n - 1) * 30
        base = especial if lances >= 3 else tradicional
        faixa = f"{300 + (n - 1) * 100 + 1} a {300 + n * 100} kg"

    tipo = "Especial" if lances >= 3 else "Tradicional"
    adicional = round((distancia_km - 15) * 6.0, 2) if distancia_km > 15 else 0.0
    total = round(base + adicional, 2)
    
    return {
        "tipo": tipo,
        "faixa": faixa,
        "base": base,
        "adicional": adicional,
        "total": total
    }

def obter_distancia(cep_destino, numero_casa):
    try:
        cep = cep_destino.replace("-", "").replace(".", "").strip()
        resp_cep = requests.get(f"https://viacep.com.br/ws/{cep}/json/").json()
        if "erro" in resp_cep: return None, "CEP não encontrado."
        
        num_str = f", {numero_casa}" if numero_casa else ""
        end = f"{resp_cep['logradouro']}{num_str}, {resp_cep['localidade']}, {resp_cep['uf']}, Brasil"
        
        geo = requests.get(f"https://nominatim.openstreetmap.org/search?format=json&q={end}", headers={'User-Agent': 'VastoApp'}).json()
        if not geo:
            end = f"{resp_cep['logradouro']}, {resp_cep['localidade']}, {resp_cep['uf']}, Brasil"
            geo = requests.get(f"https://nominatim.openstreetmap.org/search?format=json&q={end}", headers={'User-Agent': 'VastoApp'}).json()

        if not geo: return None, "Coordenadas não localizadas."

        url = f"http://router.project-osrm.org/route/v1/driving/{ORIGEM_LON},{ORIGEM_LAT};{geo[0]['lon']},{geo[0]['lat']}?overview=false"
        dist_km = requests.get(url).json()['routes'][0]['distance'] / 1000.0
        
        end_exibicao = f"{resp_cep['logradouro']}{num_str} - {resp_cep['localidade']}/{resp_cep['uf']}"
        return round(dist_km, 1), end_exibicao
    except:
        return None, "Erro ao processar rota."

# --- FORMULÁRIO ---
col_cep, col_num = st.columns([2, 1])
with col_cep:
    cep = st.text_input("CEP de Destino", placeholder="Ex: 05767-330")
with col_num:
    numero = st.text_input("Número", placeholder="Ex: 551")

peso = st.number_input("Peso total da carga (kg)", min_value=1.0, value=500.0, step=10.0)
escada = st.radio("Lances de escada", ["Sem escada", "1 lance", "2 lances", "3 ou mais lances"])

manual = st.checkbox("Informar a distância manualmente")
distancia_manual = 0.0
if manual:
    distancia_manual = st.number_input("Distância em KM", min_value=0.0, value=0.0, step=0.1)

st.write("")

# --- BOTÕES ---
col1, col2 = st.columns([1, 1.5])
with col1:
    btn_limpar = st.button("↺ Limpar")
with col2:
    btn_calcular = st.button("🖩 Calcular Frete")

if btn_limpar:
    st.rerun()

# --- EXIBIÇÃO DO RESULTADO ---
if btn_calcular:
    dist = distancia_manual
    info_end = ""
    
    if cep and not manual:
        with st.spinner("Calculando rota..."):
            calc_dist, info = obter_distancia(cep, numero)
            if calc_dist:
                dist = calc_dist
                info_end = info
            else:
                st.error(info)

    if dist > 0 or (manual and dist == 0):
        res = calcular_frete(peso, escada, dist)
        
        v_base_str = f"{res['base']:.2f}".replace('.', ',')
        v_adic_str = f"{res['adicional']:.2f}".replace('.', ',')
        v_tot_str  = f"{res['total']:.2f}".replace('.', ',')

        if info_end:
            st.success(f"📍 Endereço: {info_end} ({dist} km)")

        st.markdown(f"<h3 style='color: #111111; font-weight: 900; margin-top: 15px;'>📦 Frete {res['tipo']}</h3>", unsafe_allow_html=True)
        
        c1, c2, c3 = st.columns(3)
        c1.metric("Distância", f"{dist} km")
        c2.metric("Peso", f"{int(peso)} kg")
        c3.metric("Faixa", res['faixa'])

        st.markdown(f"""
            <div style="margin-top: 10px; font-size: 14px; color: #111111;">
                <p style="margin: 4px 0;"><strong>Valor-base por peso:</strong> R$ {v_base_str}</p>
                <p style="margin: 4px 0;"><strong>Adicional de distância:</strong> R$ {v_adic_str}</p>
            </div>
            
            <div class="result-total-box">
                <span class="total-label">VALOR TOTAL DO FRETE</span>
                <p class="total-value">R$ {v_tot_str}</p>
            </div>
        """, unsafe_allow_html=True)

# --- RODAPÉ ---
st.markdown("""
    <div class="footer-credits">
        Desenvolvido por Carol Marquezine
    </div>
""", unsafe_allow_html=True)
