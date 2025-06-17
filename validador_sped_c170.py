import csv

# === CONFIGURAÇÃO ===
arquivo_sped = "CAMINHO/SEU_ARQUIVO.TXT"
arquivo_saida = "divergencias_c170.csv"

# === PARÂMETROS ESPERADOS ===
valor_esperado_pis = 0.64
valor_esperado_cofins = 3.08

# === PROCESSAMENTO ===
with open(arquivo_sped, 'r', encoding='utf-8') as f_in, open(arquivo_saida, 'w', newline='', encoding='utf-8') as f_out:
    writer = csv.DictWriter(f_out, fieldnames=["Linha", "VL_PIS", "VL_COFINS", "Registro"])
    writer.writeheader()

    for i, line in enumerate(f_in, start=1):
        if "|C170|" in line:
            campos = line.strip().split("|")

            try:
                if len(campos) >= 28:
                    vl_pis = float(campos[24].replace(',', '.')) if campos[24] else 0.0
                    vl_cofins = float(campos[27].replace(',', '.')) if campos[27] else 0.0

                    if round(vl_pis, 2) != valor_esperado_pis or round(vl_cofins, 2) != valor_esperado_cofins:
                        writer.writerow({
                            "Linha": i,
                            "VL_PIS": vl_pis,
                            "VL_COFINS": vl_cofins,
                            "Registro": line.strip()
                        })
            except Exception as e:
                print(f"Erro na linha {i}: {e}")

print(f"✅ Verificação concluída. Divergências salvas em: {arquivo_saida}")
