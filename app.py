import streamlit as st
import math
import requests

# Coordenadas do CD (Rua Paulino Nunes Esposo, 120, SP)
ORIGEM_LAT = -23.550520
ORIGEM_LON = -46.633308

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
        headers = {'User-Agent': 'CalculadoraFreteApp'}
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
        return None, f"Erro ao processar distância: {str(e)}"

# --- INTERFACE DO USUÁRIO ---
st.set_page_config(page_title="Calculadora de Frete", page_icon="🚚")
st.title("🚚 Calculadora de Frete")

peso = st.number_input("Peso total (kg)", min_value=1.0, value=150.0, step=10.0)
lances = st.number_input("Lances de escada", min_value=0, value=0, step=1)
distancia_manual = st.number_input("Distância em KM (digite se souber)", min_value=0.0, value=0.0, step=1.0)

cep = st.text_input("OU digite o CEP de Destino para calcular a distância automaticamente:", value="")

if st.button("Calcular Frete", use_container_width=True):
    distancia_final = distancia_manual

    if cep and distancia_manual == 0:
        with st.spinner("Buscando endereço e calculando rota..."):
            dist, info = obter_distancia_por_cep(cep)
            if dist:
                distancia_final = dist
                st.info(f"📍 Endereço: {info} | Distância: **{dist} km**")
            else:
                st.error(info)

    if distancia_final > 0 or (distancia_manual == 0 and not cep):
        res = calcular_frete(peso, lances, distancia_final)
        st.divider()
        st.success(f"### Valor Total: R$ {res['valor_total']:.2f}")
        st.write(f"- **Tipo de Frete:** {res['tipo_frete']}")
        st.write(f"- **Faixa de Peso:** {res['faixa_peso']}")
        st.write(f"- **Valor Base:** R$ {res['valor_base_peso']:.2f}")
        st.write(f"- **Adicional Distância (>15km):** R$ {res['adicional_distancia']:.2f}")
