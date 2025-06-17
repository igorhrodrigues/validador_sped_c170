import streamlit as st
import pandas as pd
import csv
import tempfile

st.set_page_config(page_title="Validador SPED C170", layout="wide")
st.title("📄 Validador SPED - Bloco C170")
st.markdown("Detecta divergências de PIS ≠ 0,64 ou COFINS ≠ 3,08")

uploaded_file = st.file_uploader("📤 Faça upload do arquivo SPED (.txt)", type=["txt"])

if uploaded_file:
    # Escreve temporariamente o conteúdo em disco (necessário para arquivos grandes)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".txt", mode="wb") as temp:
        temp.write(uploaded_file.read())
        temp_path = temp.name

    registros_com_erro = []
    with open(temp_path, 'r', encoding='utf-8') as f:
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
        st.error(f"🚨 Foram encontradas {len(df_erros)} divergências.")
        st.dataframe(df_erros, use_container_width=True)
        st.download_button("📥 Baixar CSV com divergências", df_erros.to_csv(index=False), "divergencias_c170.csv", "text/csv")
    else:
        st.success("✅ Nenhuma divergência encontrada no bloco C170.")
