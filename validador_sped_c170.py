import tkinter as tk
from tkinter import filedialog, messagebox
import csv
import os

def processar_arquivo():
    caminho = filedialog.askopenfilename(
        title="Selecione o arquivo SPED .txt",
        filetypes=[("Arquivos TXT", "*.txt")]
    )

    if not caminho:
        return

    saida_csv = os.path.splitext(caminho)[0] + "_divergencias.csv"
    erros = 0

    try:
        with open(caminho, 'r', encoding='utf-8') as f_in, open(saida_csv, 'w', newline='', encoding='utf-8') as f_out:
            writer = csv.DictWriter(f_out, fieldnames=["Linha", "VL_PIS", "VL_COFINS", "Registro"])
            writer.writeheader()

            for idx, line in enumerate(f_in, start=1):
                if "|C170|" in line:
                    campos = line.strip().split("|")
                    try:
                        if len(campos) >= 28:
                            pis = float(campos[24].replace(",", ".")) if campos[24] else 0.0
                            cofins = float(campos[27].replace(",", ".")) if campos[27] else 0.0
                            if round(pis, 2) != 0.64 or round(cofins, 2) != 3.08:
                                writer.writerow({
                                    "Linha": idx,
                                    "VL_PIS": pis,
                                    "VL_COFINS": cofins,
                                    "Registro": line.strip()
                                })
                                erros += 1
                    except:
                        continue

        messagebox.showinfo("Concluído", f"{erros} divergências salvas em:\n{saida_csv}")
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro:\n{e}")

# Interface Gráfica
janela = tk.Tk()
janela.title("Validador SPED - C170")
janela.geometry("400x150")
janela.resizable(False, False)

label = tk.Label(janela, text="Clique no botão abaixo para selecionar o arquivo SPED (.txt):", wraplength=380)
label.pack(pady=20)

btn = tk.Button(janela, text="Selecionar Arquivo", command=processar_arquivo)
btn.pack()

janela.mainloop()
