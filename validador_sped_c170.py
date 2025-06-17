import streamlit as st
import pandas as pd

st.set_page_config(page_title="Validador SPED - Bloco C170", layout="wide")

st.title("🔍 Validador de SPED - Bloco C170")
st.markdown("Este validador verifica se os valores de PIS e COFINS no bloco `C170` estão corretos (esperado: **0,64** e **3,08**).")

uploaded_file = st.file_uploader("📤 Faça upload do arquivo .TXT do SPED:", type=["txt"])

if uploaded_file:
    lines = uploaded_file.readlines()
    c170_erros = []

    for idx, line in enumerate(lines):
        line_str = line.decode('utf-8').strip()
        fields = line_str.split('|')
        
        if len(fields) > 0 and fields[1] == 'C170':
            try:
                vl_pis = float(fields[24].replace(',', '.')) if len(fields) > 24 and fields[24] else 0.0
                vl_cofins = float(fields[27].replace(',', '.')) if len(fields) > 27 and fields[27] else 0.0

                if round(vl_pis, 2) != 0.64 or round(vl_cofins, 2) != 3.08:
                    c170_erros.append({
                        "Linha": idx + 1,
                        "Registro": line_str,
                        "VL_PIS": vl_pis,
                        "VL_COFINS": vl_cofins
                    })
            except ValueError:
                st.warning(f"Erro ao processar linha {idx + 1}. Verifique se o arquivo está bem formatado.")

    if c170_erros:
        df_erros = pd.DataFrame(c170_erros)
        st.error(f"🚨 Foram encontradas {len(df_erros)} divergências no bloco C170.")
        st.dataframe(df_erros, use_container_width=True)
    else:
        st.success("✅ Nenhuma divergência encontrada nos valores de PIS e COFINS do bloco C170.")
