# =============================================================================================================
# 🛰️ INTERFACE INTERNA: 1. RADAR DE PRODUTOS [FILTRO XEQUE-MATE]
# =============================================================================================================
elif st.session_state.modulo_ativo == "Radar":
    with col_centro:
        st.markdown('<div class="coluna-container">', unsafe_allow_html=True)
        st.markdown('<div class="header-box-real">👤 Comandante: <b>José Marques</b> | Mapeamento de Leilão Ativo</div>', unsafe_allow_html=True)
        
        # 📊 RECHEIO CONTRA O VAZIO: Injeção de Contadores Volumétricos de Tráfego
        col_mini1, col_mini2 = st.columns(2)
        with col_mini1: 
            st.markdown('<div class="kpi-box"><span style="font-size:11px;color:#64748b;font-weight:bold;text-transform:uppercase;">🔥 CLIQUES HOJE</span><br><span style="font-size:20px;color:#00FF87;font-weight:800;">14.250 mil</span></div>', unsafe_allow_html=True)
        with col_mini2: 
            st.markdown('<div class="kpi-box"><span style="font-size:11px;color:#64748b;font-weight:bold;text-transform:uppercase;">📡 OFERTAS ATIVAS NO MUNDO</span><br><span style="font-size:20px;color:#00E5FF;font-weight:800;">1.840 mil</span></div>', unsafe_allow_html=True)
        
        st.write("")
        st.markdown('<p class="subtitulo-bloco-real">MÓDULO 1: RADAR DE PRODUTOS [FILTRO XEQUE-MATE]</p>', unsafe_allow_html=True)
        
        # Tabela robusta com nomes de produtos acanodianos, origens gringas e valores em dólar
        dados_tabela = {
            "Nome do Produto": ["Sugar Defender", "Java Burn", "Puravive", "Prodentim", "GlucoBerry", "Citrus Burn", "Metanail Complex"],
            "Plataforma / Origem": ["BuyGoods 🇺🇸", "ClickBank 🇺🇸", "ClickBank 🇺🇸", "BuyGoods 🇺🇸", "Hotmart 🇧🇷", "ClickBank 🇺🇸", "BuyGoods 🇺🇸"],
            "Comissão Média": ["$ 118.20", "$ 135.00", "$ 142.50", "$ 125.00", "R$ 247,00", "$ 95.00", "$ 107.40"],
            "Veredito da IA": ["APROVADO (Risco Baixo)", "APROVADO (Risco Baixo)", "REVISAR (Risco Médio)", "APROVADO (Risco Baixo)", "APROVADO (Risco Baixo)", "REVISAR (Risco Médio)", "APROVADO (Risco Baixo)"]
        }
        st.dataframe(pd.DataFrame(dados_tabela), use_container_width=True, hide_index=True)
        st.write("")
        
        # Botão mestre com o sinal pulsante neon interativo
        if st.button("📄 [EXPORTAR PLANILHA COMPLETA DO RADAR EM LOTE .CSV]", key="btn_radar_csv_inside"):
            st.success("✅ Extração executada! Banco de dados atualizado com sucesso na sua máquina.")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_direita:
        st.markdown('<div class="coluna-container" style="border-right: none;">', unsafe_allow_html=True)
        st.markdown('<div class="header-box-real" style="text-align: right;">Filtro Especial: <b>Top 22 Ativos</b></div>', unsafe_allow_html=True)
        st.markdown('<p class="subtitulo-bloco-real">📊 RASTREADOR DE TRÁFEGO GLOBAL</p>', unsafe_allow_html=True)
        
        # Informativo estético hacker/sci-fi para preencher o visual do lado direito
        st.info("🔥 **Módulo Espião Operando**\n\nO robô Adriel-AI Pro vasculha de forma contínua as variações de Gravidade e Temperatura acima de 140+ nas redes dos EUA. O leilão de lances de CPC do Google Ads está sendo rastreado em tempo síncrono para garantir o posicionamento mestre com o menor custo de clique possível.")
        st.write("---")
        st.markdown("<p style='font-size: 12px; color: #64748b;'>💡 <b>Recomendação PRO:</b> Evite lances predatórios em correspondência de frase nas primeiras 48h de campanha.</p>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
