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

# --- CSS LIMPO E AJUSTADO (SEM RUÍDOS E FONTES CORRIGIDAS) ---
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

    html, body, [class*="st-"] {
      font-family: "Nunito Sans", "Segoe UI", Arial, sans-serif !important;
      color: var(--ink);
    }

    html {
      background: var(--canvas);
    }

    body {
      margin: 0;
      background:
        radial-gradient(circle at 90% 3%, rgba(253, 202, 23, 0.15), transparent 22rem),
        var(--canvas);
    }

    .topbar {
      border-bottom: 1px solid #e7e7e4;
      background: rgba(255, 255, 255, 0.92);
      backdrop-filter: blur(14px);
    }

    .topbar-inner,
    .hero,
    .calculator-grid,
    .app-footer {
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

    .tool-name span {
      font-size: 0.72rem;
      letter-spacing: 0.09em;
      text-transform: uppercase;
      color: var(--muted);
    }

    .tool-name strong {
      font-size: 0.96rem;
      color: var(--ink);
    }

    .hero {
      display: flex;
      justify-content: space-between;
      align-items: end;
      gap: 48px;
      padding: 40px 0 28px;
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
      font-size: clamp(1.8rem, 3.8vw, 2.8rem);
      line-height: 1.15;
      letter-spacing: -0.03em;
    }

    .hero-copy {
      max-width: 610px;
      margin: 12px 0 0;
      font-size: 0.96rem;
      line-height: 1.5;
      color: var(--muted);
    }

    .origin-card {
      width: 360px;
      display: flex;
      align-items: center;
      gap: 14px;
      padding: 16px 18px;
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
      font-size: 0.68rem;
      text-transform: uppercase;
      letter-spacing: 0.07em;
      color: var(--muted);
    }

    .origin-card strong {
      font-size: 0.85rem;
    }

    .origin-card div span {
      color: #7c7c7c;
      font-size: 0.75rem;
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
      padding: clamp(24px, 3.5vw, 40px);
    }

    .result-card {
      min-height: 620px;
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
      margin-bottom: 24px;
    }

    .step {
      display: inline-flex;
      justify-content: center;
      min-width: 32px;
      padding-top: 4px;
      border-top: 3px solid var(--yellow);
      color: #787878;
      font-size: 0.7rem;
      font-weight: 800;
      letter-spacing: 0.08em;
    }

    .card-heading h2,
    .empty-result h2,
    .quote-result h2 {
      margin: 0;
      font-size: 1.2rem;
      letter-spacing: -0.02em;
    }

    .card-heading p {
      margin: 4px 0 0;
      font-size: 0.84rem;
      color: var(--muted);
    }

    .empty-result {
      width: 100%;
      margin: auto;
      text-align: center;
    }

    .empty-result .step {
      margin: 20px auto 14px;
    }

    .empty-result h2 {
      max-width: 300px;
      margin: 0 auto;
      color: #111;
    }

    .empty-result p {
      max-width: 310px;
      margin: 10px auto 24px;
      font-size: 0.84rem;
      line-height: 1.5;
      color: var(--muted);
    }

    .route-visual {
      position: relative;
      width: min(280px, 80%);
      height: 75px;
      margin: 0 auto;
    }

    .route-line {
      position: absolute;
      inset: 34px 30px auto;
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
      top: 30px;
      z-index: 1;
      width: 12px;
      height: 12px;
      border: 3px solid white;
      border-radius: 50%;
      background: #1c1c1c;
      box-shadow: 0 0 0 2px #1c1c1c;
    }

    .route-point.start {
      left: 20px;
    }

    .route-point.end {
      right: 15px;
      top: 10px;
      width: 42px;
      height: 42px;
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
      gap: 16px;
      padding-bottom: 20px;
      border-bottom: 1px solid #343434;
    }

    .quote-topline small {
      color: #a5a5a5;
      font-size: 0.65rem;
      letter-spacing: 0.08em;
      text-transform: uppercase;
    }

    .quote-result h2 {
      margin-top: 4px;
      font-size: 1.35rem;
      text-transform: capitalize;
      color: white;
    }

    .type-badge {
      padding: 6px 10px;
      border-radius: 999px;
      color: #111;
      background: var(--yellow);
      font-size: 0.65rem;
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
      margin: 20px 0;
      padding: 14px;
      border: 1px solid #383838;
      border-radius: 10px;
      background: #222;
    }

    .destination-box > span {
      color: var(--yellow);
      font-size: 1.2rem;
    }

    .destination-box div {
      min-width: 0;
      display: flex;
      flex-direction: column;
    }

    .destination-box small {
      color: #999;
      font-size: 0.64rem;
      text-transform: uppercase;
      letter-spacing: 0.07em;
    }

    .destination-box strong {
      margin-top: 3px;
      font-size: 0.74rem;
      line-height: 1.35;
      color: white;
    }

    .metric-row {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 12px;
      margin-bottom: 20px;
    }

    .metric-row div {
      padding: 10px 0;
      border-bottom: 1px solid #3d3d3d;
    }

    .metric-row small {
      display: block;
      color: #999;
      font-size: 0.65rem;
    }

    .metric-row strong {
      display: block;
      margin-top: 2px;
      font-size: 1rem;
      color: white;
    }

    .price-breakdown {
      display: flex;
      flex-direction: column;
      gap: 10px;
      margin-bottom: 20px;
    }

    .price-breakdown div {
      display: flex;
      justify-content: space-between;
      gap: 16px;
      color: #c1c1c1;
      font-size: 0.75rem;
    }

    .price-breakdown strong {
      color: white;
    }

    .total-box {
      margin-top: auto;
      padding: 18px;
      border-radius: 12px;
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
      font-size: 0.68rem;
      font-weight: 800;
      text-transform: uppercase;
    }

    .total-box strong {
      margin: 4px 0;
      font-size: clamp(1.8rem, 4.5vw, 2.6rem);
      line-height: 1;
      letter-spacing: -0.04em;
    }

    .total-box span {
      color: #5f4c00;
      font-size: 0.65rem;
    }

    .app-footer {
      display: flex;
      justify-content: space-between;
      padding: 20px 0 32px;
      color: #777;
      font-size: 0.7rem;
    }

    header { visibility: hidden !important; display: none !important; }
    #MainMenu { visibility: hidden !important; display: none !important; }
    footer { visibility: hidden !important; display: none !important; }
    .stDeployButton { display: none !important; }
    [data-testid="stStatusWidget"] { visibility: hidden !important; display: none !important; }
    </style>
""", unsafe_allow_html=True)

# Renderização segura da logo com fallback em texto limpo (sem sobras de tags)
if logo_b64:
    logo_html = f'<img src="data:image/png;base64,{logo_b64}" class="brand-logo" alt="Vasto Logo">'
else:
    logo_html = '<strong style="font-size:1.05rem; letter-spacing:0.04em; color:#111;">VASTO ACABAMENTOS</strong>'

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
    <div class="app-footer">
        <span>Vasto Acabamentos — Todos os direitos reservados.</span>
        <span>Desenvolvido por Carol Marquezine</span>
    </div>
""", unsafe_allow_html=True)
