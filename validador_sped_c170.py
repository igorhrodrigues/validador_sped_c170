import pandas as pd

# Configuração dos caminhos
txt_path = "caminho/para/seu_arquivo_sped.txt"
xlsx_path = "caminho/para/sua_planilha.xlsx"

# Leitura do Excel
real_df = pd.read_excel(xlsx_path)
real_df['CHAVEACI'] = real_df['CHAVEACI'].astype(str)

# Leitura do TXT (linha a linha)
registros = []

with open(txt_path, 'r', encoding='utf-8') as f:
    for line in f:
        if "|C170|" in line:
            campos = line.strip().split('|')
            if len(campos) >= 28:
                try:
                    chave = campos[-4]  # ajuste se necessário
                    valor_pis = float(campos[24].replace(',', '.')) if campos[24] else 0.0
                    valor_cofins = float(campos[27].replace(',', '.')) if campos[27] else 0.0

                    registros.append({
                        'CHAVEACI': chave,
                        'VALOR_PIS_SPED': round(valor_pis, 2),
                        'VALOR_COFINS_SPED': round(valor_cofins, 2),
                    })
                except Exception:
                    continue

sped_df = pd.DataFrame(registros)

# Junção e comparação
merged_df = pd.merge(sped_df, real_df, on="CHAVEACI", how="inner")
merged_df["DIF_PIS"] = merged_df["VALOR_PIS_SPED"] - merged_df["VALOR_PIS"]
merged_df["DIF_COFINS"] = merged_df["VALOR_COFINS_SPED"] - merged_df["VALOR_COFINS"]

# Filtra divergências
erros_df = merged_df[(merged_df["DIF_PIS"].abs() > 0.01) | (merged_df["DIF_COFINS"].abs() > 0.01)]

# Salva resultados
erros_df.to_csv("divergencias_pis_cofins.csv", index=False)
print(f"Divergências salvas em 'divergencias_pis_cofins.csv' ({len(erros_df)} linhas com erro)")
