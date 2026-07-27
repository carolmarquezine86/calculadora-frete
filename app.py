import streamlit as st
import math
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

# --- FORÇAR TÍTULO E ÍCONES PARA O IPHONE ---
favicon_svg = '''data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><rect width="100" height="100" rx="20" fill="%23111111"/><text x="50%" y="58%" font-family="Arial, sans-serif" font-weight="900" font-size="52" fill="%23F2C900" text-anchor="middle" dominant-baseline="middle">VA</text></svg>'''

apple_touch_icon_html = ""
if icon_b64:
    mime = "jpeg" if icon_ext.lower() == "jpg" else icon_ext.lower()
    apple_touch_icon_html = f'<link rel="apple-touch-icon" href="data:image/{mime};base64,{icon_b64}">'

st.markdown(f"""
    <head>
        <link rel="icon" type="image/svg+xml" href="{favicon_svg}">
        {apple_touch_icon_html}
        <title>Frete Vasto</title>
    </head>
    <script>
        document.addEventListener("DOMContentLoaded", function() {{
            document.title = "Frete Vasto";
            setInterval(function() {{
                if (document.title !== "Frete Vasto") {{
                    document.title = "Frete Vasto";
                }}
                var badges = document.querySelectorAll('[class*="viewerBadge"], footer, #rooturator, [data-testid="stStatusWidget"]');
                badges.forEach(function(el) {{
                    el.style.display = 'none';
                    el.remove();
                }});
            }}, 500);
        }});
    </script>
""", unsafe_allow_html=True)

# --- SEU CSS COMPLETO E ORIGINAL ---
st.markdown("""
    <style>
    :root {
      --yellow: #fdca17;
      --yellow-soft: #fff8d8;
      --ink: #151515;
      --muted: #686868;
      --line: #dedede;
      --surface: #ffffff;
      --canvas: #f4f4f2;
      --green: #197a45;
      --red: #a13c2f;
    }

    * {
      box-sizing: border-box;
    }

    html {
      background: var(--canvas);
    }

    body {
      margin: 0;
      color: var(--ink);
      background:
        radial-gradient(circle at 90% 3%, rgba(253, 202, 23, 0.15), transparent 22rem),
        var(--canvas);
      font-family: "Nunito Sans", "Segoe UI", Arial, sans-serif;
    }

    button,
    input,
    select {
      font: inherit;
    }

    button,
    select,
    input[type="checkbox"] {
      cursor: pointer;
    }

    .app-shell {
      min-height: 100vh;
    }

    .topbar {
      border-bottom: 1px solid #e7e7e4;
      background: rgba(255, 255, 255, 0.92);
      backdrop-filter: blur(14px);
    }

    .topbar-inner,
    .hero,
    .calculator-grid,
    footer {
      width: min(1180px, calc(100% - 40px));
      margin: 0 auto;
    }

    .topbar-inner {
      min-height: 82px;
      display: flex;
      align-items: center;
      gap: 24px;
    }

    .brand-logo {
      width: 158px;
      height: auto;
      object-fit: contain;
    }

    .tool-name {
      display: flex;
      flex-direction: column;
      padding-left: 24px;
      border-left: 1px solid var(--line);
    }

    .tool-name span,
    .origin-card small,
    .field small,
    .quote-result small,
    .empty-result p,
    .hero-copy,
    .card-heading p {
      color: var(--muted);
    }

    .tool-name span {
      font-size: 0.72rem;
      letter-spacing: 0.09em;
      text-transform: uppercase;
    }

    .tool-name strong {
      font-size: 0.96rem;
    }

    .hero {
      display: flex;
      justify-content: space-between;
      align-items: end;
      gap: 48px;
      padding: 54px 0 36px;
    }

    .eyebrow {
      margin: 0 0 10px;
      color: #7e6500;
      font-size: 0.76rem;
      font-weight: 800;
      letter-spacing: 0.12em;
      text-transform: uppercase;
    }

    .hero h1 {
      max-width: 670px;
      margin: 0;
      font-size: clamp(2rem, 4.4vw, 3.55rem);
      line-height: 1.02;
      letter-spacing: -0.055em;
    }

    .hero-copy {
      max-width: 610px;
      margin: 16px 0 0;
      font-size: 1.02rem;
      line-height: 1.65;
    }

    .origin-card {
      width: 360px;
      display: flex;
      align-items: center;
      gap: 14px;
      padding: 17px 19px;
      border: 1px solid #e0dfd7;
      border-radius: 16px;
      background: rgba(255, 255, 255, 0.72);
    }

    .origin-icon {
      display: grid;
      place-items: center;
      width: 42px;
      height: 42px;
      border: 1px solid #ead27b;
      border-radius: 50%;
      color: var(--yellow);
      background: var(--yellow-soft);
      font-size: 0.8rem;
    }

    .origin-card div {
      min-width: 0;
      display: flex;
      flex-direction: column;
    }

    .origin-card small {
      margin-bottom: 2px;
      font-size: 0.7rem;
      text-transform: uppercase;
      letter-spacing: 0.07em;
    }

    .origin-card strong {
      font-size: 0.88rem;
    }

    .origin-card div span {
      color: #7c7c7c;
      font-size: 0.78rem;
    }

    .calculator-grid {
      display: grid;
      grid-template-columns: minmax(0, 1.05fr) minmax(370px, 0.75fr);
      align-items: stretch;
      border: 1px solid #dadad7;
      border-radius: 22px;
      overflow: hidden;
      background: var(--surface);
      box-shadow: 0 24px 70px rgba(32, 32, 26, 0.08);
      margin-bottom: 40px;
    }

    .form-card,
    .result-card {
      padding: clamp(26px, 4vw, 46px);
    }

    .result-card {
      min-height: 665px;
      display: flex;
      flex-direction: column;
      border-left: 1px solid var(--line);
      background:
        linear-gradient(rgba(255, 255, 255, 0.94), rgba(255, 255, 255, 0.94)),
        repeating-linear-gradient(45deg, #eee 0 1px, transparent 1px 12px);
    }

    .result-card.has-result {
      background: #171717;
      color: white;
    }

    .card-heading {
      display: flex;
      gap: 15px;
      align-items: flex-start;
      margin-bottom: 31px;
    }

    .step {
      display: inline-flex;
      justify-content: center;
      min-width: 38px;
      padding-top: 5px;
      border-top: 3px solid var(--yellow);
      color: #787878;
      font-size: 0.72rem;
      font-weight: 800;
      letter-spacing: 0.08em;
    }

    .card-heading h2,
    .empty-result h2,
    .quote-result h2 {
      margin: 0;
      font-size: 1.36rem;
      letter-spacing: -0.025em;
    }

    .card-heading p {
      margin: 5px 0 0;
      font-size: 0.88rem;
    }

    .field {
      display: block;
      margin-bottom: 22px;
    }

    .field > span {
      display: block;
      margin-bottom: 8px;
      font-size: 0.82rem;
      font-weight: 800;
      color: var(--ink);
    }

    .field small {
      display: block;
      margin-top: 7px;
      font-size: 0.72rem;
    }

    .two-columns {
      display: grid;
      grid-template-columns: 0.72fr 1.28fr;
      gap: 15px;
    }

    .empty-result {
      width: 100%;
      margin: auto;
      text-align: center;
    }

    .empty-result .step {
      margin: 30px auto 18px;
    }

    .empty-result h2 {
      max-width: 320px;
      margin: 0 auto;
      color: #111;
    }

    .empty-result p {
      max-width: 330px;
      margin: 11px auto 28px;
      font-size: 0.86rem;
      line-height: 1.6;
    }

    .route-visual {
      position: relative;
      width: min(290px, 80%);
      height: 85px;
      margin: 0 auto;
    }

    .route-line {
      position: absolute;
      inset: 38px 35px auto;
      height: 3px;
      background: repeating-linear-gradient(
        90deg,
        var(--yellow) 0 12px,
        transparent 12px 21px
      );
      transform: rotate(-7deg);
    }

    .route-point {
      position: absolute;
      top: 35px;
      z-index: 1;
      width: 12px;
      height: 12px;
      border: 3px solid white;
      border-radius: 50%;
      background: #1c1c1c;
      box-shadow: 0 0 0 2px #1c1c1c;
    }

    .route-point.start {
      left: 23px;
    }

    .route-point.end {
      right: 18px;
      top: 12px;
      width: 47px;
      height: 47px;
      display: grid;
      place-items: center;
      border: 0;
      color: #171717;
      background: var(--yellow);
      box-shadow: 0 8px 22px rgba(116, 91, 0, 0.2);
    }

    .quote-result {
      width: 100%;
      display: flex;
      flex-direction: column;
    }

    .quote-topline {
      display: flex;
      align-items: flex-start;
      justify-content: space-between;
      gap: 20px;
      padding-bottom: 24px;
      border-bottom: 1px solid #343434;
    }

    .quote-topline small {
      color: #a5a5a5;
      font-size: 0.68rem;
      letter-spacing: 0.08em;
      text-transform: uppercase;
    }

    .quote-result h2 {
      margin-top: 5px;
      font-size: 1.55rem;
      text-transform: capitalize;
      color: white;
    }

    .type-badge {
      padding: 7px 11px;
      border-radius: 999px;
      color: #111;
      background: var(--yellow);
      font-size: 0.69rem;
      font-weight: 900;
    }

    .type-badge.especial {
      color: white;
      background: #9b3d31;
    }

    .destination-box {
      display: flex;
      gap: 12px;
      align-items: flex-start;
      margin: 25px 0;
      padding: 15px;
      border: 1px solid #383838;
      border-radius: 11px;
      background: #222;
    }

    .destination-box > span {
      color: var(--yellow);
      font-size: 1.3rem;
    }

    .destination-box div {
      min-width: 0;
      display: flex;
      flex-direction: column;
    }

    .destination-box small {
      color: #999;
      font-size: 0.66rem;
      text-transform: uppercase;
      letter-spacing: 0.07em;
    }

    .destination-box strong {
      margin-top: 4px;
      font-size: 0.76rem;
      line-height: 1.4;
      color: white;
    }

    .metric-row {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 12px;
      margin-bottom: 24px;
    }

    .metric-row div {
      padding: 13px 0;
      border-bottom: 1px solid #3d3d3d;
    }

    .metric-row small {
      display: block;
      color: #999;
      font-size: 0.68rem;
    }

    .metric-row strong {
      display: block;
      margin-top: 3px;
      font-size: 1.06rem;
      color: white;
    }

    .price-breakdown {
      display: flex;
      flex-direction: column;
      gap: 12px;
      margin-bottom: 24px;
    }

    .price-breakdown div {
      display: flex;
      justify-content: space-between;
      gap: 20px;
      color: #c1c1c1;
      font-size: 0.77rem;
    }

    .price-breakdown strong {
      color: white;
    }

    .total-box {
      margin-top: auto;
      padding: 22px;
      border-radius: 14px;
      color: #111;
      background: var(--yellow);
    }

    .total-box small,
    .total-box strong,
    .total-box span {
      display: block;
    }

    .total-box small {
      color: #5f4c00;
      font-size: 0.72rem;
      font-weight: 800;
      text-transform: uppercase;
    }

    .total-box strong {
      margin: 5px 0;
      font-size: clamp(2rem, 5vw, 3rem);
      line-height: 1;
      letter-spacing: -0.05em;
    }

    .total-box span {
      color: #5f4c00;
      font-size: 0.68rem;
    }

    footer {
      display: flex;
      justify-content: space-between;
      padding: 24px 0 42px;
      color: #777;
      font-size: 0.72rem;
    }

    header { visibility: hidden !important; display: none !important; }
    #MainMenu { visibility: hidden !important; display: none !important; }
    footer { visibility: hidden !important; display: none !important; }
    .stDeployButton { display: none !important; }
    [data-testid="stStatusWidget"] { visibility: hidden !important; display: none !important; }
    </style>
""", unsafe_allow_html=True)

logo_html = f'<img src="data:image/png;base64,{logo_b64}" class="brand-logo" alt="Vasto Logo">' if logo_b64 else '<strong>VASTO ACABAMENTOS</strong>'

# --- TOPBAR ---
st.markdown(f"""
    <div class="topbar">
        <div class="topbar-inner">
            {logo_html}
            <div class="tool-name">
                <span>Ferramenta Interna</span>
                <strong>Calculadora de Frete & Logística</strong>
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)

# --- HERO ---
st.markdown("""
    <div class="hero">
        <div>
            <p class="eyebrow">Logística Vasto Acabamentos</p>
            <h1>Cálculo preciso de rotas e cubagem para entregas.</h1>
            <p class="hero-copy">Insira os dados do endereço de destino e o peso total da carga para gerar o orçamento exato do frete.</p>
        </div>
        <div class="origin-card">
            <div class="origin-icon">📍</div>
            <div>
                <small>Saída do CD Principal</small>
                <strong>Rua Paulino Nunes Esposo, 120</strong>
                <span>Jardim Marcelo — São Paulo / SP</span>
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)

# --- LÓGICA DE CÁLCULO ---
def calcular_frete(peso_kg, tipo_frete, distancia_km):
    is_especial = (tipo_frete == "Especial")

    if peso_kg <= 300:
        base, faixa = (80.0, "0 a 300 kg") if not is_especial else (120.0, "0 a 300 kg")
    elif peso_kg <= 400:
        base, faixa = (100.0, "301 a 400 kg") if not is_especial else (150.0, "301 a 400 kg")
    else:
        n = math.ceil((peso_kg - 300) / 100)
        tradicional = 100 + (n - 1) * 10
        especial = 150 + (n - 1) * 30
        base = especial if is_especial else tradicional
        faixa = f"{300 + (n - 1) * 100 + 1} a {300 + n * 100} kg"

    adicional = round((distancia_km - 15) * 6.0, 2) if distancia_km > 15 else 0.0
    total = round(base + adicional, 2)
    
    return {
        "tipo": tipo_frete,
        "faixa": faixa,
        "base": base,
        "adicional": adicional,
        "total": total
    }

def estimar_distancia_por_cep(cep_destino):
    try:
        cep_limpo = ''.join(filter(str.isdigit, cep_destino))
        if len(cep_limpo) != 8:
            return None, "CEP inválido. Digite os 8 números."
        
        prefixo = int(cep_limpo[:5])
        
        if 48000 <= prefixo <= 48499:
            return 12.0, "Região Sul Próxima (São Paulo/SP)"
        elif 48500 <= prefixo <= 48999:
            return 10.0, "Jardim Marcelo / Grajaú (São Paulo/SP)"
        elif 4000 <= prefixo <= 5999:
            return 22.0, "Zona Sul / Centro / Zona Oeste (São Paulo/SP)"
        elif 6000 <= prefixo <= 8499:
            return 28.0, "Zona Leste / Zona Norte (São Paulo/SP)"
        elif 9000 <= prefixo <= 9999:
            return 30.0, "Grande São Paulo / ABC Paulista"
        elif 10000 <= prefixo <= 19999:
            return 85.0, "Interior de São Paulo"
        else:
            return 35.0, "São Paulo e Região Metropolitana"
    except Exception:
        return 20.0, "São Paulo/SP"

# --- LAYOUT PRINCIPAL (GRID) ---
st.markdown('<div class="calculator-grid">', unsafe_allow_html=True)

col_form, col_res = st.columns([1.05, 0.75], gap="large")

with col_form:
    st.markdown("""
        <div class="form-card">
            <div class="card-heading">
                <span class="step">01</span>
                <div>
                    <h2>Parâmetros da Entrega</h2>
                    <p>Preencha os campos abaixo com as informações do cliente.</p>
                </div>
            </div>
    """, unsafe_allow_html=True)

    col_c1, col_c2 = st.columns([2, 1])
    with col_c1:
        cep = st.text_input("CEP de Destino", placeholder="Ex: 04312-040", key="input_cep")
    with col_c2:
        numero = st.text_input("Número", placeholder="Ex: 551", key="input_numero")

    peso = st.number_input("Peso total da carga (kg)", min_value=1.0, value=500.0, step=10.0, key="input_peso")
    tipo_frete_escolhido = st.radio("Tipo de Frete", ["Tradicional", "Especial"], key="input_tipo")

    st.write("")
    
    btn_col1, btn_col2 = st.columns([1, 1.5])
    with btn_col1:
        btn_limpar = st.button("↺ Limpar", use_container_width=True)
    with btn_col2:
        btn_calcular = st.button("🖩 Calcular Frete", use_container_width=True, type="primary")

    if btn_limpar:
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

with col_res:
    if not btn_calcular or not cep:
        st.markdown("""
            <div class="result-card">
                <div class="empty-result">
                    <span class="step">02</span>
                    <h2>Aguardando Dados</h2>
                    <p>Preencha o CEP e o peso ao lado e clique em calcular para visualizar o orçamento detalhado.</p>
                    <div class="route-visual">
                        <div class="route-line"></div>
                        <div class="route-point start"></div>
                        <div class="route-point end">🚚</div>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
    else:
        dist, regiao = estimar_distancia_por_cep(cep)
        if dist is not None:
            res = calcular_frete(peso, tipo_frete_escolhido, dist)
            v_base_str = f"{res['base']:.2f}".replace('.', ',')
            v_adic_str = f"{res['adicional']:.2f}".replace('.', ',')
            v_tot_str  = f"{res['total']:.2f}".replace('.', ',')
            badge_class = "especial" if tipo_frete_escolhido == "Especial" else ""

            st.markdown(f"""
                <div class="result-card has-result">
                    <div class="quote-result">
                        <div class="quote-topline">
                            <div>
                                <small>Orçamento Gerado</small>
                                <h2>Frete {res['tipo']}</h2>
                            </div>
                            <span class="type-badge {badge_class}">{res['tipo'].upper()}</span>
                        </div>
                        <div class="destination-box">
                            <span>📍</span>
                            <div>
                                <small>Localidade Destino</small>
                                <strong>{regiao} (Nº {numero if numero else 'S/N'})</strong>
                            </div>
                        </div>
                        <div class="metric-row">
                            <div>
                                <small>Distância Estimada</small>
                                <strong>{dist} km</strong>
                            </div>
                            <div>
                                <small>Peso da Carga</small>
                                <strong>{int(peso)} kg</strong>
                            </div>
                        </div>
                        <div class="price-breakdown">
                            <div>
                                <span>Faixa de Peso ({res['faixa']})</span>
                                <strong>R$ {v_base_str}</strong>
                            </div>
                            <div>
                                <span>Adicional de Distância</span>
                                <strong>R$ {v_adic_str}</strong>
                            </div>
                        </div>
                        <div class="total-box">
                            <small>Valor Total do Frete</small>
                            <strong>R$ {v_tot_str}</strong>
                            <span>Cálculo realizado com base na tabela oficial Vasto.</span>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.error(regiao)

st.markdown('</div>', unsafe_allow_html=True)

# --- RODAPÉ ---
st.markdown("""
    <footer>
        <span>Vasto Acabamentos — Todos os direitos reservados.</span>
        <span>Desenvolvido por Carol Marquezine</span>
    </footer>
""", unsafe_allow_html=True)
