import streamlit as st
import math
import requests

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Calculadora de Frete | Vasto Acabamentos",
    page_icon="🚛",
    layout="centered"
)

# --- ESTILIZAÇÃO CSS (IDENTIDADE VASTO) ---
st.markdown("""
    <style>
    /* Estilização do Botão Principal */
    div.stButton > button {
        background-color: #B89758 !important;
        color: #FFFFFF !important;
        font-weight: 600 !important;
        font-size: 16px !important;
        border-radius: 4px !important;
        border: none !important;
        padding: 0.75rem 1.5rem !important;
        width: 100% !important;
        letter-spacing: 1px !important;
        text-transform: uppercase !important;
        transition: all 0.3s ease !important;
    }
    div.stButton > button:hover {
        background-color: #967941 !important;
        box-shadow: 0 4px 12px rgba(184, 151, 88, 0.3) !important;
    }
    
    /* Inputs Estilizados */
    .stNumberInput input, .stTextInput input {
        border-radius: 4px !important;
        border: 1px solid #E0E0E0 !important;
        padding: 10px !important;
    }
    
    /* Titulos e Seções */
    .header-vasto {
        text-align: center;
        padding-bottom: 20px;
        border-bottom: 2px solid #F0F0F0;
        margin-bottom: 30px;
    }
    
    .logo-text {
        font-family: 'Helvetica Neue', sans-serif;
        font-size: 28px;
        font-weight: 700;
        letter-spacing: 4px;
        color: #1A1A1A;
        margin: 0;
    }
    
    .sub-logo {
        color: #B89758;
        font-size: 13px;
        letter-spacing: 3px;
        text-transform: uppercase;
        font-weight: 600;
        margin-top: 5px;
    }
    
    .result-card {
        background-color: #F8F9FA;
        border: 1px solid #EAEAEA;
        border-left: 5px solid #B89758;
        padding: 25px;
        border-radius: 6px;
        margin-top: 25px;
    }
    </style>
""", unsafe_allow_html=True)

# --- CABEÇALHO COM LOGO E IDENTIDADE DA LOJA ---
st.markdown("""
    <div class="header-vasto">
        <h1 class="logo-text">VASTO</h1>
        <div class="sub-logo">A C A B A M E N T O S</div>
        <p style="color: #666; font-size: 14px; margin-top: 15px;">Simulador Oficial de Frete e Entrega</p>
    </div>
""", unsafe_allow_html=True)

# --- COORDENADAS ORIGEM (CD) ---
ORIGEM_LAT = -23.550520
ORIGEM_LON = -46.633308

# --- FUNÇÕES DE CÁLCULO ---
def calcular_faixa_peso(peso_kg):
    if peso_kg <= 300:
        return 80.0, 120.0, "0 a 300 kg"
    if peso_kg <= 400:
        return 100.0, 150.0, "301 a 400 kg"
    
    n = math.ceil((peso_kg - 300) / 100)
    tradicional = 100 + (n - 1) * 10
    especial    = 150 + (n - 1) * 30
    inicio = 300 + (n - 1) * 100 + 1
    fim    = 300 + n * 100
    return float(tradicional), float(especial), f"{inicio} a {fim} kg"

def calcular_frete(peso_kg, lances_escada, distancia_km):
    tradicional, especial, faixa = calcular_faixa_peso(peso_kg)
    tipo, base = ("Especial", especial) if lances_escada >= 3 else ("Tradicional", tradicional)
    adicional = round((distancia_km - 15) * 6.0, 2) if distancia_km > 15 else 0.0
    total = round(base + adicional, 2)
    return {
        "tipo_frete": tipo, 
        "faixa_peso": faixa,
        "valor_base_peso": base,
        "adicional_distancia": adicional,
        "valor_total": total,
    }

def obter_distancia_por_cep(cep_destino):
    try:
        cep_limpo = cep_destino.replace("-", "").replace(".", "").strip()
        resp_cep = requests.get(f"https://viacep.com.br/ws/{cep_limpo}/json/").json()
        if "erro" in resp_cep:
            return None, "CEP não encontrado."
        
        endereco = f"{resp_cep['logradouro']}, {resp_cep['localidade']}, {resp_cep['uf']}, Brasil"
        headers = {'User-Agent': 'CalculadoraFreteVastoApp'}
        resp_geo = requests.get(f"https://nominatim.openstreetmap.org/search?format=json&q={endereco}", headers=headers).json()
        if not resp_geo:
            return None, "Não foi possível localizar as coordenadas do CEP."

        dest_lat = float(resp_geo[0]['lat'])
        dest_lon = float(resp_geo[0]['lon'])

        url_osrm = f"http://router.project-osrm.org/route/v1/driving/{ORIGEM_LON},{ORIGEM_LAT};{dest_lon},{dest_lat}?overview=false"
        resp_rota = requests.get(url_osrm).json()
        distancia_km = resp_rota['routes'][0]['distance'] / 1000.0
        return round(distancia_km, 2), endereco

    except Exception as e:
        return None, f"Erro ao calcular rota: {str(e)}"

# --- FORMULÁRIO DE ENTRADA ---
col1, col2 = st.columns(2)
with col1:
    peso = st.number_input("Peso total da carga (kg)", min_value=1.0, value=150.0, step=10.0)
with col2:
    lances = st.number_input("Lances de escada", min_value=0, value=0, step=1)

cep = st.text_input("Informe o CEP de Destino:", placeholder="Ex: 01001-000")
distancia_manual = st.number_input("Ou informe a distância em KM (opcional):", min_value=0.0, value=0.0, step=1.0)

st.write("")
btn_calcular = st.button("Calcular Valor do Frete")

# --- PROCESSAMENTO E EXIBIÇÃO DE RESULTADOS ---
if btn_calcular:
    distancia_final = distancia_manual

    if cep and distancia_manual == 0:
        with st.spinner("Buscando endereço e calculando frete..."):
            dist, info = obter_distancia_por_cep(cep)
            if dist:
                distancia_final = dist
                st.success(f"📍 **Endereço:** {info} | 📏 **Distância:** {dist} km")
            else:
                st.error(info)

    if distancia_final > 0 or (distancia_manual == 0 and not cep):
        res = calcular_frete(peso, lances, distancia_final)
        
        # CARD DE RESULTADO ESTILIZADO
        st.markdown(f"""
            <div class="result-card">
                <span style="color: #888; text-transform: uppercase; font-size: 12px; letter-spacing: 1px;">Valor do Frete Calculado</span>
                <h1 style="color: #B89758; margin: 5px 0 15px 0; font-size: 36px; font-weight: 700;">R$ {res['valor_total']:.2f}</h1>
                <div style="display: flex; gap: 20px; font-size: 14px; color: #444; border-top: 1px solid #E0E0E0; padding-top: 15px;">
                    <div><strong>Modalidade:</strong> {res['tipo_frete']}</div>
                    <div><strong>Faixa de Peso:</strong> {res['faixa_peso']}</div>
                    <div><strong>Excedente KM:</strong> R$ {res['adicional_distancia']:.2f}</div>
                </div>
            </div>
        """, unsafe_allow_html=True)
