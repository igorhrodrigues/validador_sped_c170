import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Validador SPED - Bloco C170", layout="wide")
st.title("📁 Validador de Arquivo SPED (.txt) Grande - Bloco C170")

# Caminho do arquivo local
caminho = st.text_input("Digite ou cole o caminho do arquivo SPED (.txt):")

if caminho and os.path.exists(caminho):
    st.success("📄 Arquivo encontrado. Iniciando leitura...")

    registros_com_erro = []

    with open(caminho, 'r', encoding='utf-8') as f:
        for idx, line in enumerate(f, start=1):
            if "|C170|" in line:
                campos = line.strip().split("|")
                try:
                    if len(campos) >= 28:
                        valor_pis = float(campos[24].replace(',', '.')) if campos[24] else 0.0
                        valor_cofins = float(campos[27].replace(',', '.')) if campos[27] else 0.0
                        if round(valor_pis, 2) != 0.64 or round(valor_cofins, 2) != 3.08:
                            registros_com_erro.append({
                                "Linha": idx,
                                "VL_PIS": valor_pis,
                                "VL_COFINS": valor_cofins,
                                "Registro": line.strip()
                            })
                except Exception as e:
                    st.warning(f"Erro na linha {idx}: {e}")

    if registros_com_erro:
        df_erros = pd.DataFrame(registros_com_erro)
        st.error(f"🚨 {len(df_erros)} divergências encontradas.")
        st.dataframe(df_erros, use_container_width=True)
        st.download_button("📥 Baixar CSV com erros", df_erros.to_csv(index=False), "divergencias_c170.csv", "text/csv")
    else:
        st.success("✅ Nenhuma divergência encontrada.")

elif caminho:
    st.error("❌ Caminho inválido ou arquivo não encontrado.")
