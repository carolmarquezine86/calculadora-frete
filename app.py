import streamlit as st
import math
import requests

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Frete Vasto", page_icon="🚚", layout="centered")

# --- ESTILIZAÇÃO CSS AVANÇADA (LAYOUT FIEL ÀS IMAGENS) ---
st.markdown("""
    <style>
    /* Fundo geral da aplicação */
    .stApp { 
        background-color: #F4F5F7; 
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }
    
    /* Container principal responsivo */
    .block-container { 
        padding-top: 0rem !important; 
        padding-bottom: 100px !important; 
        max-width: 480px !important; 
    }
    
    /* HEADER AMARELO FIXO NO TOPO */
    .vasto-header {
        background-color: #F2C900;
        padding: 15px 20px;
        margin: 0 -2rem 20px -2rem; 
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

    /* SUBTÍTULOS E TÍTULO PRINCIPAL */
    .sub-title {
        color: #6B7280;
        font-size: 11px;
        font-weight: 800;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        margin-bottom: 2px;
    }
    .main-title {
        color: #111111;
        font-size: 24px;
        font-weight: 900;
        margin-bottom: 4px;
    }
    .description-text {
        color: #6B7280;
        font-size: 13px;
        margin-bottom: 20px;
    }

    /* CARD SAÍDA DO CD (PRETO) */
    .cd-card {
        background-color: #111111;
        border-radius: 16px;
        padding: 16px 20px;
        color: white;
        margin-bottom: 20px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .cd-label {
        color: #F2C900;
        font-size: 10px;
        font-weight: 800;
        letter-spacing: 1px;
    }
    .cd-address {
        font-size: 15px;
        font-weight: 800;
        margin-top: 2px;
        color: #FFFFFF;
    }
    .cd-city {
        font-size: 12px;
        color: #9CA3AF;
    }

    /* CARDS BRANCOS DAS SEÇÕES DE INPUT */
    .step-card {
        background-color: #FFFFFF;
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 15px;
        border: 1px solid #E5E7EB;
        box-shadow: 0 2px 8px rgba(0,0,0,0.02);
    }
    .step-header {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 15px;
    }
    .step-number {
        background-color: #F2C900;
        color: #111;
        font-weight: 900;
        font-size: 14px;
        width: 32px;
        height: 32px;
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .step-title-text h3 {
        margin: 0;
        font-size: 15px;
        font-weight: 800;
        color: #111;
    }
    .step-title-text p {
        margin: 0;
        font-size: 12px;
        color: #6B7280;
    }

    /* INPUTS ESTILIZADOS */
    .stTextInput input, .stNumberInput input {
        background-color: #F8F9FA !important;
        border: 1px solid #E5E7EB !important;
        border-radius: 10px !important;
        color: #111111 !important;
        font-weight: 600 !important;
    }

    /* CARD DE RESULTADO (PRETO COM HIGHLIGHT AMARELO) */
    .result-card {
        background-color: #111111;
        border-radius: 20px;
        padding: 24px;
        color: white;
        margin-top: 20px;
        position: relative;
    }
    .result-badge {
        position: absolute;
        top: 20px;
        right: 20px;
        background-color: #F2C900;
        color: #111;
        font-weight: 800;
        font-size: 12px;
        padding: 4px 12px;
        border-radius: 20px;
    }
    .result-grid {
        display: flex;
        justify-content: space-between;
        margin: 20px 0;
    }
    .result-grid-item label {
        font-size: 11px;
        color: #9CA3AF !important;
    }
    .result-grid-item div {
        font-size: 16px;
        font-weight: 800;
        color: #FFF;
    }
    .result-total-box {
        background-color: #F2C900;
        border-radius: 14px;
        padding: 16px 20px;
        color: #111111;
        margin-top: 15px;
    }
    .result-total-box label {
        font-size: 10px;
        font-weight: 800;
        letter-spacing: 1px;
        color: #111 !important;
    }
    .result-total-box h1 {
        margin: 0;
        font-size: 32px;
        font-weight: 900;
        color: #111;
    }

    /* AJUSTE DOS BOTÕES STREAMLIT */
    .stButton > button {
        border-radius: 10px !important;
        padding: 12px !important;
        font-weight: 800 !important;
        font-size: 15px !important;
        border: none !important;
        width: 100% !important;
    }
    /* Limpar */
    div[data-testid="column"]:nth-child(1) .stButton > button {
        background-color: #18181B !important;
        color: #FFFFFF !important;
        border: 1px solid #27272A !important;
    }
    /* Calcular */
    div[data-testid="column"]:nth-child(2) .stButton > button {
        background-color: #F2C900 !important;
        color: #111111 !important;
    }
    div[data-testid="column"]:nth-child(2) .stButton > button p {
        color: #111111 !important;
        font-weight: 900 !important;
    }

    /* FOOTER COM ASSINATURA */
    .footer-credits {
        text-align: center;
        margin-top: 30px;
        color: #888888;
        font-size: 12px;
        font-weight: 600;
    }

    /* Ocultar nativos */
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

# --- TÍTULOS ---
st.markdown("""
    <div class="sub-title">Orçamento Rápido</div>
    <div class="main-title">Calculadora de Frete</div>
    <div class="description-text">Informe o CEP e os dados da entrega para gerar o valor.</div>
""", unsafe_allow_html=True)

# --- CARD SAÍDA DO CD ---
st.markdown("""
    <div class="cd-card">
        <div>
            <div class="cd-label">SAÍDA DO CD</div>
            <div class="cd-address">🟡 Rua Paulino Nunes Esposo, 120</div>
            <div class="cd-city">São Paulo — SP</div>
        </div>
        <div style="font-size: 20px;">📍</div>
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
        base, faixa = 80.0 if lances < 3 else 120.0, "0 a 300 kg"
    elif peso_kg <= 400:
        base, faixa = 100.0 if lances < 3 else 150.0, "301 a 400 kg"
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

def buscar_cep(cep_input):
    try:
        cep = cep_input.replace("-", "").replace(".", "").strip()
        resp = requests.get(f"https://viacep.com.br/ws/{cep}/json/").json()
        if "erro" not in resp:
            return resp
    except:
        pass
    return None

def calcular_distancia(logradouro, cidade, uf):
    try:
        end = f"{logradouro}, {cidade}, {uf}, Brasil"
        geo = requests.get(f"https://nominatim.openstreetmap.org/search?format=json&q={end}", headers={'User-Agent': 'VastoApp'}).json()
        if geo:
            url = f"http://router.project-osrm.org/route/v1/driving/{ORIGEM_LON},{ORIGEM_LAT};{geo[0]['lon']},{geo[0]['lat']}?overview=false"
            dist_km = requests.get(url).json()['routes'][0]['distance'] / 1000.0
            return round(dist_km, 1)
    except:
        pass
    return 10.0  # valor padrão seguro em caso de falha

# --- PASSO 1: ENDEREÇO DO CLIENTE ---
st.markdown("""
    <div class="step-card">
        <div class="step-header">
            <div class="step-number">01</div>
            <div class="step-title-text">
                <h3>Endereço do cliente</h3>
                <p>Preencha para gerar o orçamento.</p>
            </div>
        </div>
""", unsafe_allow_html=True)

col_cep, col_busca = st.columns([3, 1])
with col_cep:
    cep_in = st.text_input("CEP", placeholder="05767-330", label_visibility="collapsed")
with col_busca:
    btn_buscar_cep = st.button("🔍")

# Auto-preenchimento
rua_val, bairro_val, cidade_val, uf_val = "", "", "", ""
if cep_in:
    dados_cep = buscar_cep(cep_in)
    if dados_cep:
        rua_val = dados_cep.get("logradouro", "")
        bairro_val = dados_cep.get("bairro", "")
        cidade_val = dados_cep.get("localidade", "")
        uf_val = dados_cep.get("uf", "")

rua = st.text_input("Rua / Logradouro", value=rua_val, placeholder="Ex: Rua Berco Udler")

col_num, col_bairro = st.columns([1, 1])
with col_num:
    numero = st.text_input("Número", placeholder="Ex: 551")
with col_bairro:
    bairro = st.text_input("Bairro", value=bairro_val, placeholder="Ex: Jd. Catanduva")

st.markdown("</div>", unsafe_allow_html=True) # Fim Step 1

# --- PASSO 2: DETALHES DA CARGA ---
st.markdown("""
    <div class="step-card">
        <div class="step-header">
            <div class="step-number">02</div>
            <div class="step-title-text">
                <h3>Detalhes do frete</h3>
                <p>Informe peso e escadas do local.</p>
            </div>
        </div>
""", unsafe_allow_html=True)

peso = st.number_input("Peso total (kg)", min_value=1.0, value=500.0, step=10.0)
escada = st.radio("Lances de escada", ["Sem escada", "1 lance", "2 lances", "3 ou mais lances"], horizontal=True)

manual = st.checkbox("Informar a distância manualmente")
distancia_manual = 0.0
if manual:
    distancia_manual = st.number_input("Distância em KM", min_value=0.0, value=5.3, step=0.1)

st.markdown("</div>", unsafe_allow_html=True) # Fim Step 2

# --- BARRA DE BOTÕES ---
col_btn1, col_btn2 = st.columns([1, 1.5])
with col_btn1:
    btn_limpar = st.button("↺ Limpar")
with col_btn2:
    btn_calcular = st.button("🖩 Calcular Frete")

if btn_limpar:
    st.rerun()

# --- RESULTADO DO ORÇAMENTO ---
if btn_calcular:
    dist = distancia_manual if manual else calcular_distancia(rua, cidade_val, uf_val)
    res = calcular_frete(peso, escada, dist)
    
    # Formatação das moedas para o formato brasileiro
    v_base_str = f"{res['base']:.2f}".replace('.', ',')
    v_adic_str = f"{res['adicional']:.2f}".replace('.', ',')
    v_tot_str  = f"{res['total']:.2f}".replace('.', ',')

    st.markdown(f"""
        <div class="result-card">
            <div class="sub-title" style="color: #9CA3AF;">RESULTADO DO ORÇAMENTO</div>
            <div class="result-badge">{res['tipo']}</div>
            <h2 style="margin: 5px 0 15px 0; font-size: 26px; font-weight: 900; color: #FFF;">Frete {res['tipo']}</h2>
            
            <div class="result-grid">
                <div class="result-grid-item">
                    <label>Distância</label>
                    <div>{dist} km</div>
                </div>
                <div class="result-grid-item">
                    <label>Peso</label>
                    <div>{int(peso)} kg</div>
                </div>
                <div class="result-grid-item">
                    <label>Faixa</label>
                    <div>{res['faixa']}</div>
                </div>
            </div>
            
            <hr style="border: none; border-top: 1px solid #27272A; margin: 15px 0;">
            
            <div style="display: flex; justify-content: space-between; font-size: 14px; margin-bottom: 8px;">
                <span style="color: #9CA3AF;">Valor-base por peso</span>
                <span style="font-weight: 700;">R$ {v_base_str}</span>
            </div>
            <div style="display: flex; justify-content: space-between; font-size: 14px; margin-bottom: 15px;">
                <span style="color: #9CA3AF;">Adicional de distância</span>
                <span style="font-weight: 700;">R$ {v_adic_str}</span>
            </div>

            <div class="result-total-box">
                <label>VALOR TOTAL DO FRETE</label>
                <h1>R$ {v_tot_str}</h1>
            </div>
            
            <p style="color: #9CA3AF; font-size: 11px; margin-top: 12px; margin-bottom: 0;">
                Frete padrão em horário comercial, até {escada if escada != 'Sem escada' else '0 lances'}.
            </p>
        </div>
    """, unsafe_allow_html=True)

# --- RODAPÉ ---
st.markdown("""
    <div class="footer-credits">
        Desenvolvido por Carol Marquezine
    </div>
""", unsafe_allow_html=True)
