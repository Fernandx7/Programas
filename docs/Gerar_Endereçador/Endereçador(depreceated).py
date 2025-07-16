import tkinter as tk
from tkinter import messagebox, filedialog
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import requests
import os
import webbrowser

VERSAO_ATUAL = "v1.0"  # NÃO ESQUECERRRRRRRRRR: Atualiza isso sempre que gerar uma nova versão
NOME_PROGRAMA = "Programa_Gerar_Endereçador"

# o comando para crianção do executavel é: pyinstaller --onefile --noconsole --icon=postcard.ico Programa_Gerar_Endereçador.py

def verificar_versao(nome_programa, versao_atual):
    try:
        url = f"https://fernandx7.github.io/Atualizador-Utilitarios/{nome_programa}/latest.txt"
        resposta = requests.get(url, timeout=5)
        if resposta.status_code == 200:
            versao_disponivel = resposta.text.strip()
            if versao_disponivel != versao_atual:
                return versao_disponivel
    except Exception as e:
        print("Erro ao verificar versão:", e)
    return None

import subprocess
import sys

def notificar_usuario_e_atualizar(nome_programa, nova_versao):
    resposta = messagebox.askyesno(
        "Atualização disponível",
        f"Uma nova versão ({nova_versao}) está disponível.\nDeseja baixar e instalar agora?"
    )
    if resposta:
        url = "https://raw.githubusercontent.com/Fernandx7/Atualizador-Utilitarios/main/docs/Programa_Gerar_Endereçador/v2.0/setup/Setup_enderecador.exe"
        arquivo_destino = "Setup_enderecador.exe"

        try:
            resposta_req = requests.get(url, stream=True)
            resposta_req.raise_for_status()
            with open(arquivo_destino, "wb") as f:
                for chunk in resposta_req.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            messagebox.showinfo("Download concluído", "Arquivo baixado com sucesso, iniciando instalador...")
            
            # Abrir o instalador (Windows)
            if sys.platform == "win32":
                subprocess.Popen([arquivo_destino], shell=True)
            else:
                # Outras plataformas podem ser adicionadas aqui
                messagebox.showinfo("Info", f"Instalador salvo em {arquivo_destino}. Execute manualmente.")

            # Fecha o programa atual para que usuário rode a nova versão
            os._exit(0)

        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao baixar a atualização: {e}")

# Função para consultar o CEP
def consultar_cep(cep):
    url = f"https://viacep.com.br/ws/{cep}/json/"
    try:
        resposta = requests.get(url)
        dados = resposta.json()
        if "erro" in dados:
            messagebox.showerror("Erro", "CEP não encontrado.")
            return None
        return {
            "endereco": dados.get("logradouro", ""),
            "bairro": dados.get("bairro", ""),
            "cidade": dados.get("localidade", ""),
            "estado": dados.get("uf", "")
        }
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao consultar o CEP: {e}")
        return None

# Função para preencher dados automaticamente ao puxar pelo CEP
def puxar_dados_remetente():
    cep = cep_remetente_var.get()
    if cep and len(cep) == 8 and cep.isdigit():
        dados = consultar_cep(cep)
        if dados:
            endereco_remetente_var.set(dados["endereco"])
            bairro_remetente_var.set(dados["bairro"])
            cidade_remetente_var.set(dados["cidade"])
            estado_remetente_var.set(dados["estado"])
        else:
            messagebox.showerror("Erro", "Não foi possível preencher os dados.")
    else:
        messagebox.showwarning("Aviso", "Digite um CEP válido.")

def puxar_dados_destinatario():
    cep = cep_destinatario_var.get()
    if cep and len(cep) == 8 and cep.isdigit():
        dados = consultar_cep(cep)
        if dados:
            endereco_destinatario_var.set(dados["endereco"])
            bairro_destinatario_var.set(dados["bairro"])
            cidade_destinatario_var.set(dados["cidade"])
            estado_destinatario_var.set(dados["estado"])
        else:
            messagebox.showerror("Erro", "Não foi possível preencher os dados.")
    else:
        messagebox.showwarning("Aviso", "Digite um CEP válido.")

# Função para coletar os dados inseridos
def coletar_dados(pessoa):
    if pessoa == "remetente":
        return {
            "nome": nome_remetente_var.get(),
            "endereco": endereco_remetente_var.get(),
            "numero": numero_remetente_var.get(),
            "bairro": bairro_remetente_var.get(),
            "cidade": cidade_remetente_var.get(),
            "estado": estado_remetente_var.get(),
        }
    else:
        return {
            "nome": nome_destinatario_var.get(),
            "endereco": endereco_destinatario_var.get(),
            "numero": numero_destinatario_var.get(),
            "bairro": bairro_destinatario_var.get(),
            "cidade": cidade_destinatario_var.get(),
            "estado": estado_destinatario_var.get(),
        }

# Função para gerar a etiqueta no formato PDF
def gerar_pdf(remetente, destinatario, caminho_arquivo):
    c = canvas.Canvas(caminho_arquivo, pagesize=letter)
    largura, altura = letter

    c.setFont("Helvetica", 10)

    # Ajustar a posição para o canto superior esquerdo
    margem_x = 20  # margem para o lado esquerdo
    margem_y = altura - 20  # margem para o topo

    # Espaço superior
    c.drawString(margem_x, margem_y, "========================================")
    c.drawString(margem_x, margem_y - 20, "                DESTINATÁRIO")
    c.drawString(margem_x, margem_y - 40, f" {destinatario['nome']}")
    c.drawString(margem_x, margem_y - 60, f" {destinatario['endereco']}, {destinatario['numero']}")
    c.drawString(margem_x, margem_y - 80, f" {destinatario['bairro']}")
    c.drawString(margem_x, margem_y - 100, f"{destinatario['cidade']}/{destinatario['estado']}")
    c.drawString(margem_x, margem_y - 120, "----------------------------------------------------------------")

    c.drawString(margem_x, margem_y - 140, "                REMETENTE")
    c.drawString(margem_x, margem_y - 160, f" {remetente['nome']}")
    c.drawString(margem_x, margem_y - 180, f" {remetente['endereco']}, {remetente['numero']}")
    c.drawString(margem_x, margem_y - 200, f" {remetente['bairro']}")
    c.drawString(margem_x, margem_y - 220, f" {remetente['cidade']}/{remetente['estado']}")
    c.drawString(margem_x, margem_y - 240, "========================================")

    # Salva o arquivo PDF
    c.save()

    return caminho_arquivo

# Função para gerar a etiqueta e salvar o PDF
def gerar_e_imprimir():
    remetente = coletar_dados("remetente")
    destinatario = coletar_dados("destinatario")

    # Escolher o caminho onde salvar o arquivo PDF
    caminho_arquivo = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")], title="Escolha o local para salvar a etiqueta")

    if not caminho_arquivo:
        messagebox.showwarning("Aviso", "Você não escolheu um local para salvar o arquivo.")
        return

    # Gerar PDF
    gerar_pdf(remetente, destinatario, caminho_arquivo)


# Função para limpar os campos
def limpar_campos():
    cep_remetente_var.set("")
    cep_destinatario_var.set("")
    nome_remetente_var.set("")
    nome_destinatario_var.set("")
    endereco_remetente_var.set("")
    endereco_destinatario_var.set("")
    numero_remetente_var.set("")
    numero_destinatario_var.set("")
    bairro_remetente_var.set("")
    bairro_destinatario_var.set("")
    cidade_remetente_var.set("")
    cidade_destinatario_var.set("")
    estado_remetente_var.set("")
    estado_destinatario_var.set("")
    
    messagebox.showinfo("Campos Limpos", "Todos os campos foram limpos!")


nova_versao = verificar_versao(NOME_PROGRAMA, VERSAO_ATUAL)
if nova_versao:
    notificar_usuario_e_atualizar(NOME_PROGRAMA, nova_versao)

root = tk.Tk()

# Interface gráfica
root.title("Sistema de Endereçamento de Correios")
root.geometry("500x800")
root.configure(bg="#f4f4f4")

# Variáveis para armazenar os dados
nome_remetente_var = tk.StringVar()
endereco_remetente_var = tk.StringVar()
numero_remetente_var = tk.StringVar()
bairro_remetente_var = tk.StringVar()
cidade_remetente_var = tk.StringVar()
estado_remetente_var = tk.StringVar()

nome_destinatario_var = tk.StringVar()
endereco_destinatario_var = tk.StringVar()
numero_destinatario_var = tk.StringVar()
bairro_destinatario_var = tk.StringVar()
cidade_destinatario_var = tk.StringVar()
estado_destinatario_var = tk.StringVar()

cep_remetente_var = tk.StringVar()
cep_destinatario_var = tk.StringVar()

# Função para estilizar os campos
def estilizar_entrada(entrada):
    entrada.config(bg="#ffffff", font=("Arial", 12), bd=2, relief="solid")

# Labels e campos de entrada para Remetente
tk.Label(root, text="Remetente", font=("Arial", 14, "bold"), bg="#f4f4f4").grid(row=0, column=0, columnspan=2, pady=10)

tk.Label(root, text="CEP", font=("Arial", 12), bg="#f4f4f4").grid(row=1, column=0)
cep_remetente_entry = tk.Entry(root, textvariable=cep_remetente_var, validate="key", width=20)
estilizar_entrada(cep_remetente_entry)
cep_remetente_entry.grid(row=1, column=1, padx=10, pady=5)
tk.Button(root, text="Puxar Dados", command=puxar_dados_remetente).grid(row=1, column=2)

tk.Label(root, text="Nome", font=("Arial", 12), bg="#f4f4f4").grid(row=2, column=0)
tk.Entry(root, textvariable=nome_remetente_var).grid(row=2, column=1, padx=10, pady=5)

tk.Label(root, text="Endereço", font=("Arial", 12), bg="#f4f4f4").grid(row=3, column=0)
tk.Entry(root, textvariable=endereco_remetente_var).grid(row=3, column=1, padx=10, pady=5)

tk.Label(root, text="Número", font=("Arial", 12), bg="#f4f4f4").grid(row=4, column=0)
tk.Entry(root, textvariable=numero_remetente_var).grid(row=4, column=1, padx=10, pady=5)

tk.Label(root, text="Bairro", font=("Arial", 12), bg="#f4f4f4").grid(row=5, column=0)
tk.Entry(root, textvariable=bairro_remetente_var).grid(row=5, column=1, padx=10, pady=5)

tk.Label(root, text="Cidade", font=("Arial", 12), bg="#f4f4f4").grid(row=6, column=0)
tk.Entry(root, textvariable=cidade_remetente_var).grid(row=6, column=1, padx=10, pady=5)

tk.Label(root, text="Estado", font=("Arial", 12), bg="#f4f4f4").grid(row=7, column=0)
tk.Entry(root, textvariable=estado_remetente_var).grid(row=7, column=1, padx=10, pady=5)

# Labels e campos de entrada para Destinatário
tk.Label(root, text="Destinatário", font=("Arial", 14, "bold"), bg="#f4f4f4").grid(row=8, column=0, columnspan=2, pady=10)

tk.Label(root, text="CEP", font=("Arial", 12), bg="#f4f4f4").grid(row=9, column=0)
cep_destinatario_entry = tk.Entry(root, textvariable=cep_destinatario_var, validate="key", width=20)
estilizar_entrada(cep_destinatario_entry)
cep_destinatario_entry.grid(row=9, column=1, padx=10, pady=5)
tk.Button(root, text="Puxar Dados", command=puxar_dados_destinatario).grid(row=9, column=2)

tk.Label(root, text="Nome", font=("Arial", 12), bg="#f4f4f4").grid(row=10, column=0)
tk.Entry(root, textvariable=nome_destinatario_var).grid(row=10, column=1, padx=10, pady=5)

tk.Label(root, text="Endereço", font=("Arial", 12), bg="#f4f4f4").grid(row=11, column=0)
tk.Entry(root, textvariable=endereco_destinatario_var).grid(row=11, column=1, padx=10, pady=5)

tk.Label(root, text="Número", font=("Arial", 12), bg="#f4f4f4").grid(row=12, column=0)
tk.Entry(root, textvariable=numero_destinatario_var).grid(row=12, column=1, padx=10, pady=5)

tk.Label(root, text="Bairro", font=("Arial", 12), bg="#f4f4f4").grid(row=13, column=0)
tk.Entry(root, textvariable=bairro_destinatario_var).grid(row=13, column=1, padx=10, pady=5)

tk.Label(root, text="Cidade", font=("Arial", 12), bg="#f4f4f4").grid(row=14, column=0)
tk.Entry(root, textvariable=cidade_destinatario_var).grid(row=14, column=1, padx=10, pady=5)

tk.Label(root, text="Estado", font=("Arial", 12), bg="#f4f4f4").grid(row=15, column=0)
tk.Entry(root, textvariable=estado_destinatario_var).grid(row=15, column=1, padx=10, pady=5)

# Botões
tk.Button(root, text="Gerar e Salvar PDF", command=gerar_e_imprimir, font=("Arial", 12, "bold"), bg="#4CAF50", fg="white").grid(row=16, column=0, columnspan=2, pady=20)

tk.Button(root, text="Limpar Campos", command=limpar_campos, font=("Arial", 12, "bold"), bg="#FF5722", fg="white").grid(row=17, column=0, columnspan=2, pady=10)

root.mainloop()