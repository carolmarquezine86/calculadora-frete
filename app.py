import streamlit as st
import math
import requests

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Frete Vasto", page_icon="🚚", layout="centered")

# --- CSS APENAS PARA ESTILIZAÇÃO VISUAL SEGURA ---
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
    
    /* HEADER VASTO */
    .vasto-header {
        background-color: #F2C900;
        padding: 16px 20px;
        border-radius: 12px;
        margin-bottom: 20px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .logo-box {
        background-color: #111;
        color: #F2C900;
        font-weight: 900;
        font-size: 20px;
        padding: 6px 12px;
        border-radius: 8px;
        margin-right: 10px;
    }
    .text-box h1 { margin: 0; font-size: 16px; font-weight: 900; color: #111; letter-spacing: 1px; line-height: 1.1; }
    .text-box p { margin: 0; font-size: 9px; font-weight: 700; color: #111; letter-spacing: 2px; }
    .badge {
        background-color: rgba(0,0,0,0.08);
        padding: 5px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 700;
        color: #111;
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

    /* RÓTULOS DOS CAMPOS */
    label, p, div[data-testid="stMarkdownContainer"] p {
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

    /* === BOTÕES === */
    .stButton > button {
        border-radius: 10px !important;
        padding: 12px 20px !important;
        font-weight: 900 !important;
        font-size: 15px !important;
        width: 100% !important;
        transition: all 0.2s ease-in-out !important;
        cursor: pointer !important;
    }

    /* Botão Limpar */
    div[data-testid="column"]:nth-child(1) .stButton > button {
        background-color: #FFFFFF !important;
        color: #111111 !important;
        border: 2px solid #111111 !important;
    }
    div[data-testid="column"]:nth-child(1) .stButton > button * {
        color: #111111 !important;
        font-weight: 900 !important;
    }

    /* Botão Calcular (Amarelo) */
    div[data-testid="column"]:nth-child(2) .stButton > button {
        background-color: #F2C900 !important;
        color: #111111 !important;
        border: 2px solid #F2C900 !important;
    }
    div[data-testid="column"]:nth-child(2) .stButton > button * {
        color: #111111 !important;
        font-weight: 900 !important;
    }
    div[data-testid="column"]:nth-child(2) .stButton > button:hover,
    div[data-testid="column"]:nth-child(2) .stButton > button:active,
    div[data-testid="column"]:nth-child(2) .stButton > button:focus {
        background-color: #FFFFFF !important;
        color: #111111 !important;
        border-color: #111111 !important;
    }

    /* CAIXA DE RESULTADO */
    .result-total-box {
        background-color: #F2C900;
        border-radius: 12px;
        padding: 16px;
        margin-top: 15px;
    }
    .result-total-box span {
        color: #111111 !important;
        font-size: 11px;
        font-weight: 800;
        letter-spacing: 1px;
        display: block;
    }
    .result-total-box h1 {
        color: #111111 !important;
        font-size: 32px;
        font-weight: 900;
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

# --- HEADER VASTO ---
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

# --- EXIBIÇÃO DO RESULTADO (USANDO COMPONENTES NATIVOS DO STREAMLIT) ---
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

        # CONTAINER NATIVO SEGURO
        with st.container():
            st.markdown(f"### 📦 Frete {res['tipo']}")
            
            c1, c2, c3 = st.columns(3)
            c1.metric("Distância", f"{dist} km")
            c2.metric("Peso", f"{int(peso)} kg")
            c3.metric("Faixa", res['faixa'])

            st.write(f"**Valor-base por peso:** R$ {v_base_str}")
            st.write(f"**Adicional de distância:** R$ {v_adic_str}")

            st.markdown(f"""
                <div class="result-total-box">
                    <span>VALOR TOTAL DO FRETE</span>
                    <h1>R$ {v_tot_str}</h1>
                </div>
            """, unsafe_allow_html=True)

# --- RODAPÉ ---
st.markdown("""
    <div class="footer-credits">
        Desenvolvido por Carol Marquezine
    </div>
""", unsafe_allow_html=True)
