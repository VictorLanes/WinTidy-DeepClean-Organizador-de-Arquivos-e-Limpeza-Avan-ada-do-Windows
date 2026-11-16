import os
import sys
import shutil
import zipfile
import tempfile
import subprocess
import ctypes
from datetime import datetime
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext

# ==========================================================
# SOLICITA PRIVILÉGIOS DE ADMINISTRADOR AUTOMATICAMENTE
# ==========================================================
def verificar_e_elevar_admin():
    try:
        is_admin = ctypes.windll.shell32.IsUserAnAdmin()
    except Exception:
        is_admin = False

    if not is_admin:
        script = os.path.abspath(sys.argv[0])
        params = " ".join([f'"{arg}"' for arg in sys.argv[1:]])
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, f'"{script}" {params}', None, 1)
        sys.exit()

# Dicionário de categorias e suas respectivas extensões
CATEGORIAS = {
    "Imagens": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp", ".ico", ".tiff"],
    "Documentos": [".pdf", ".doc", ".docx", ".txt", ".odt", ".rtf", ".ppt", ".pptx", ".epub"],
    "Planilhas_e_Dados": [".xls", ".xlsx", ".csv", ".json", ".xml", ".sql", ".db"],
    "Videos": [".mp4", ".mkv", ".avi", ".mov", ".wmv", ".flv", ".webm"],
    "Audios": [".mp3", ".wav", ".aac", ".flac", ".ogg", ".wma", ".m4a"],
    "Compactados": [".zip", ".rar", ".7z", ".tar", ".gz", ".iso"],
    "Executaveis_e_Codigo": [".exe", ".msi", ".bat", ".sh", ".py", ".js", ".html", ".css", ".apk"]
}

class SistemaOrganizadorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Organizador de Arquivos & Limpeza Completa [ADMIN]")
        self.root.geometry("690x720")
        self.root.resizable(False, False)
        self.root.configure(bg="#f4f4f9")

        # Variáveis do Organizador
        self.pasta_selecionada = tk.StringVar()
        self.fazer_backup = tk.BooleanVar(value=True)

        # Variáveis das 10 Opções de Limpeza
        self.opt_temp = tk.BooleanVar(value=True)
        self.opt_prefetch = tk.BooleanVar(value=True)
        self.opt_thumbs = tk.BooleanVar(value=True)
        self.opt_shaders = tk.BooleanVar(value=True)
        self.opt_wer = tk.BooleanVar(value=True)

        self.opt_dns = tk.BooleanVar(value=True)
        self.opt_lixeira = tk.BooleanVar(value=False)
        self.opt_win_update = tk.BooleanVar(value=False)
        self.opt_delivery = tk.BooleanVar(value=True)
        self.opt_dism = tk.BooleanVar(value=False)

        self.criar_interface()

    def criar_interface(self):
        lbl_titulo = tk.Label(
            self.root, text="Gerenciador de Arquivos e Limpeza do Sistema", 
            font=("Segoe UI", 15, "bold"), bg="#f4f4f9", fg="#2c3e50"
        )
        lbl_titulo.pack(pady=10)

        # --- SEÇÃO 1: ORGANIZADOR DE ARQUIVOS ---
        frame_org = tk.LabelFrame(
            self.root, text=" 1. Organizar Pasta por Categorias ", 
            font=("Segoe UI", 10, "bold"), bg="#f4f4f9", fg="#34495e", padx=15, pady=10
        )
        frame_org.pack(fill="x", padx=20, pady=5)

        frame_dir = tk.Frame(frame_org, bg="#f4f4f9")
        frame_dir.pack(fill="x", pady=5)

        entry_pasta = tk.Entry(frame_dir, textvariable=self.pasta_selecionada, width=60, font=("Segoe UI", 9))
        entry_pasta.pack(side="left", padx=(0, 10), ipady=3)

        btn_procurar = tk.Button(
            frame_dir, text="Selecionar Pasta...", command=self.selecionar_pasta,
            bg="#3498db", fg="white", font=("Segoe UI", 9, "bold"), relief="flat", padx=10, cursor="hand2"
        )
        btn_procurar.pack(side="left")

        chk_backup = tk.Checkbutton(
            frame_org, text="Criar backup (.zip) da pasta antes de organizar", 
            variable=self.fazer_backup, bg="#f4f4f9", font=("Segoe UI", 9), cursor="hand2"
        )
        chk_backup.pack(anchor="w", pady=4)

        btn_organizar = tk.Button(
            frame_org, text="Iniciar Organização", command=self.executar_organizacao,
            bg="#27ae60", fg="white", font=("Segoe UI", 10, "bold"), relief="flat", pady=6, cursor="hand2"
        )
        btn_organizar.pack(fill="x", pady=2)

        # --- SEÇÃO 2: LIMPEZA AVANÇADA DO SISTEMA ---
        frame_limpeza = tk.LabelFrame(
            self.root, text=" 2. Limpeza Profunda da Máquina (Selecione os módulos) ", 
            font=("Segoe UI", 10, "bold"), bg="#f4f4f9", fg="#34495e", padx=15, pady=10
        )
        frame_limpeza.pack(fill="x", padx=20, pady=8)

        grid_opcoes = tk.Frame(frame_limpeza, bg="#f4f4f9")
        grid_opcoes.pack(fill="x", pady=(0, 8))

        # Coluna 1
        tk.Checkbutton(grid_opcoes, text="Arquivos Temporários (Temp e %Temp%)", variable=self.opt_temp, bg="#f4f4f9", font=("Segoe UI", 9), cursor="hand2").grid(row=0, column=0, sticky="w", padx=(0, 25), pady=2)
        tk.Checkbutton(grid_opcoes, text="Cache de Pré-busca (Prefetch)", variable=self.opt_prefetch, bg="#f4f4f9", font=("Segoe UI", 9), cursor="hand2").grid(row=1, column=0, sticky="w", padx=(0, 25), pady=2)
        tk.Checkbutton(grid_opcoes, text="Cache de Miniaturas (Thumbnails)", variable=self.opt_thumbs, bg="#f4f4f9", font=("Segoe UI", 9), cursor="hand2").grid(row=2, column=0, sticky="w", padx=(0, 25), pady=2)
        tk.Checkbutton(grid_opcoes, text="Cache de Shaders DirectX (Jogos/GPU)", variable=self.opt_shaders, bg="#f4f4f9", font=("Segoe UI", 9), cursor="hand2").grid(row=3, column=0, sticky="w", padx=(0, 25), pady=2)
        tk.Checkbutton(grid_opcoes, text="Relatórios de Erros do Windows (WER)", variable=self.opt_wer, bg="#f4f4f9", font=("Segoe UI", 9), cursor="hand2").grid(row=4, column=0, sticky="w", padx=(0, 25), pady=2)

        # Coluna 2
        tk.Checkbutton(grid_opcoes, text="Limpar Cache DNS (flushdns)", variable=self.opt_dns, bg="#f4f4f9", font=("Segoe UI", 9), cursor="hand2").grid(row=0, column=1, sticky="w", pady=2)
        tk.Checkbutton(grid_opcoes, text="Esvaziar Lixeira do Windows", variable=self.opt_lixeira, bg="#f4f4f9", font=("Segoe UI", 9), cursor="hand2").grid(row=1, column=1, sticky="w", pady=2)
        tk.Checkbutton(grid_opcoes, text="Otimização de Entrega (Cache P2P)", variable=self.opt_delivery, bg="#f4f4f9", font=("Segoe UI", 9), cursor="hand2").grid(row=2, column=1, sticky="w", pady=2)
        tk.Checkbutton(grid_opcoes, text="Cache do Windows Update (Download)", variable=self.opt_win_update, bg="#f4f4f9", font=("Segoe UI", 9), cursor="hand2").grid(row=3, column=1, sticky="w", pady=2)
        tk.Checkbutton(grid_opcoes, text="Limpeza de Componentes (DISM - Lento)", variable=self.opt_dism, bg="#f4f4f9", font=("Segoe UI", 9), cursor="hand2").grid(row=4, column=1, sticky="w", pady=2)

        btn_limpar = tk.Button(
            frame_limpeza, text="Executar Limpeza Selecionada", command=self.executar_limpeza,
            bg="#e67e22", fg="white", font=("Segoe UI", 10, "bold"), relief="flat", pady=6, cursor="hand2"
        )
        btn_limpar.pack(fill="x")

        # --- SEÇÃO 3: LOG DE ATIVIDADES ---
        frame_log = tk.LabelFrame(
            self.root, text=" Log de Execução ", 
            font=("Segoe UI", 9, "bold"), bg="#f4f4f9", fg="#34495e", padx=10, pady=5
        )
        frame_log.pack(fill="both", expand=True, padx=20, pady=(0, 15))

        self.txt_log = scrolledtext.ScrolledText(frame_log, height=11, font=("Consolas", 8), state="disabled", bg="#ffffff")
        self.txt_log.pack(fill="both", expand=True)

    def log(self, mensagem):
        self.txt_log.configure(state="normal")
        hora = datetime.now().strftime("%H:%M:%S")
        self.txt_log.insert(tk.END, f"[{hora}] {mensagem}\n")
        self.txt_log.see(tk.END)
        self.txt_log.configure(state="disabled")
        self.root.update_idletasks()

    # ==========================================
    # MÉTODOS DO ORGANIZADOR DE ARQUIVOS
    # ==========================================
    def selecionar_pasta(self):
        caminho = filedialog.askdirectory(title="Selecione a pasta que deseja organizar")
        if caminho:
            self.pasta_selecionada.set(caminho)
            self.log(f"Pasta selecionada: {caminho}")

    def criar_backup(self, pasta_origem):
        try:
            pasta_pai = os.path.dirname(pasta_origem)
            nome_pasta = os.path.basename(pasta_origem)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nome_zip = os.path.join(pasta_pai, f"Backup_{nome_pasta}_{timestamp}.zip")

            self.log("Criando backup ZIP... Aguarde.")
            with zipfile.ZipFile(nome_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for raiz, _, arquivos in os.walk(pasta_origem):
                    for arquivo in arquivos:
                        caminho_completo = os.path.join(raiz, arquivo)
                        caminho_relativo = os.path.relpath(caminho_completo, pasta_origem)
                        zipf.write(caminho_completo, caminho_relativo)

            self.log(f"Backup salvo em: {nome_zip}")
            return True
        except Exception as e:
            self.log(f"ERRO ao criar backup: {e}")
            messagebox.showerror("Erro de Backup", f"Não foi possível criar o backup:\n{e}")
            return False

    def obter_categoria(self, extensao):
        extensao = extensao.lower()
        for categoria, lista_ext in CATEGORIAS.items():
            if extensao in lista_ext:
                return categoria
        return "Outros"

    def gerar_nome_unico(self, destino_pasta, nome_arquivo):
        base, ext = os.path.splitext(nome_arquivo)
        contador = 1
        novo_nome = nome_arquivo
        while os.path.exists(os.path.join(destino_pasta, novo_nome)):
            novo_nome = f"{base}_{contador}{ext}"
            contador += 1
        return novo_nome

    def executar_organizacao(self):
        pasta = self.pasta_selecionada.get()
        if not pasta or not os.path.exists(pasta):
            messagebox.showwarning("Aviso", "Por favor, selecione uma pasta válida primeiro.")
            return

        if self.fazer_backup.get():
            if not self.criar_backup(pasta):
                return

        self.log("Iniciando organização dos arquivos...")
        arquivos_movidos = 0

        for item in os.listdir(pasta):
            caminho_item = os.path.join(pasta, item)
            if os.path.isfile(caminho_item):
                _, extensao = os.path.splitext(item)
                categoria = self.obter_categoria(extensao)

                pasta_destino = os.path.join(pasta, categoria)
                os.makedirs(pasta_destino, exist_ok=True)

                nome_final = self.gerar_nome_unico(pasta_destino, item)
                caminho_final = os.path.join(pasta_destino, nome_final)

                try:
                    shutil.move(caminho_item, caminho_final)
                    arquivos_movidos += 1
                    self.log(f"Movido: {item} -> [{categoria}]")
                except Exception as e:
                    self.log(f"Erro ao mover '{item}': {e}")

        self.log(f"Organização finalizada! {arquivos_movidos} arquivos movidos.")
        messagebox.showinfo("Sucesso", f"Organização concluída!\n{arquivos_movidos} arquivos foram organizados.")

    # ==========================================
    # MÉTODOS DE LIMPEZA DO SISTEMA
    # ==========================================
    def obter_tamanho_caminho(self, caminho):
        """Calcula o tamanho em bytes de um arquivo ou pasta."""
        total = 0
        try:
            if os.path.isfile(caminho):
                return os.path.getsize(caminho)
            for raiz, _, arquivos in os.walk(caminho):
                for f in arquivos:
                    fp = os.path.join(raiz, f)
                    if not os.path.islink(fp):
                        total += os.path.getsize(fp)
        except Exception:
            pass
        return total

    def limpar_pasta_alvo(self, caminho_pasta, filtro_prefixo=None):
        removidos = 0
        ignorados = 0
        bytes_liberados = 0

        if not os.path.exists(caminho_pasta):
            return 0, 0, 0

        try:
            itens = os.listdir(caminho_pasta)
        except PermissionError:
            self.log(f"ACESSO NEGADO em {caminho_pasta}")
            return 0, 0, 0

        for item in itens:
            if filtro_prefixo and not item.lower().startswith(filtro_prefixo.lower()):
                continue

            caminho_completo = os.path.join(caminho_pasta, item)
            tamanho_item = self.obter_tamanho_caminho(caminho_completo)

            try:
                if os.path.isfile(caminho_completo) or os.path.islink(caminho_completo):
                    os.unlink(caminho_completo)
                    removidos += 1
                    bytes_liberados += tamanho_item
                elif os.path.isdir(caminho_completo):
                    shutil.rmtree(caminho_completo)
                    removidos += 1
                    bytes_liberados += tamanho_item
            except Exception:
                ignorados += 1

        return removidos, ignorados, bytes_liberados

    def limpar_dns(self):
        try:
            subprocess.run(["ipconfig", "/flushdns"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, creationflags=subprocess.CREATE_NO_WINDOW)
            self.log("DNS: Cache de resolução DNS limpo.")
        except Exception as e:
            self.log(f"DNS: Falha ao limpar ({e}).")

    def esvaziar_lixeira(self):
        try:
            resultado = ctypes.windll.shell32.SHEmptyRecycleBinW(None, None, 7)
            if resultado == 0:
                self.log("Lixeira: Esvaziada com sucesso.")
            else:
                self.log("Lixeira: Já estava vazia.")
        except Exception as e:
            self.log(f"Lixeira: Erro ao esvaziar ({e}).")

    def executar_dism(self):
        self.log("DISM: Iniciando limpeza de componentes do Windows (pode levar 1-3 min)...")
        try:
            subprocess.run(
                ["Dism.exe", "/online", "/Cleanup-Image", "/StartComponentCleanup"],
                check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, creationflags=subprocess.CREATE_NO_WINDOW
            )
            self.log("DISM: Componentes antigos do sistema limpos com sucesso.")
        except Exception as e:
            self.log(f"DISM: Falha na execução ({e}).")

    def executar_limpeza(self):
        opcoes = [
            self.opt_temp.get(), self.opt_prefetch.get(), self.opt_thumbs.get(),
            self.opt_shaders.get(), self.opt_wer.get(), self.opt_dns.get(),
            self.opt_lixeira.get(), self.opt_delivery.get(), self.opt_win_update.get(),
            self.opt_dism.get()
        ]
        if not any(opcoes):
            messagebox.showwarning("Aviso", "Selecione pelo menos uma opção de limpeza.")
            return

        confirmar = messagebox.askyesno(
            "Confirmar Limpeza", 
            "Deseja executar os módulos de limpeza selecionados?\n\nArquivos em uso pelo Windows serão ignorados com segurança."
        )
        if not confirmar:
            return

        self.log("=== INICIANDO LIMPEZA PROFUNDA ===")
        win_dir = os.environ.get("SystemRoot", "C:\\Windows")
        local_appdata = os.environ.get("LOCALAPPDATA", "")
        program_data = os.environ.get("ProgramData", "C:\\ProgramData")

        total_removidos = 0
        total_bytes = 0

        # 1. Temp e %Temp%
        if self.opt_temp.get():
            r1, i1, b1 = self.limpar_pasta_alvo(tempfile.gettempdir())
            r2, i2, b2 = self.limpar_pasta_alvo(os.path.join(win_dir, "Temp"))
            total_removidos += (r1 + r2)
            total_bytes += (b1 + b2)
            self.log(f"TEMP/%TEMP%: {r1 + r2} itens removidos ({i1 + i2} em uso).")

        # 2. Prefetch
        if self.opt_prefetch.get():
            r, i, b = self.limpar_pasta_alvo(os.path.join(win_dir, "Prefetch"))
            total_removidos += r
            total_bytes += b
            self.log(f"Prefetch: {r} itens removidos ({i} em uso).")

        # 3. Miniaturas (Thumbnails)
        if self.opt_thumbs.get() and local_appdata:
            caminho_exp = os.path.join(local_appdata, "Microsoft", "Windows", "Explorer")
            r, i, b = self.limpar_pasta_alvo(caminho_exp, filtro_prefixo="thumbcache_")
            total_removidos += r
            total_bytes += b
            self.log(f"Miniaturas: {r} arquivos de cache removidos ({i} em uso).")

        # 4. Cache de Shaders DirectX
        if self.opt_shaders.get() and local_appdata:
            r, i, b = self.limpar_pasta_alvo(os.path.join(local_appdata, "D3DSCache"))
            total_removidos += r
            total_bytes += b
            self.log(f"Shaders DirectX: {r} arquivos removidos ({i} em uso).")

        # 5. Relatórios de Erros (WER)
        if self.opt_wer.get():
            r1, i1, b1 = self.limpar_pasta_alvo(os.path.join(program_data, "Microsoft", "Windows", "WER", "ReportQueue"))
            r2, i2, b2 = self.limpar_pasta_alvo(os.path.join(program_data, "Microsoft", "Windows", "WER", "ReportArchive"))
            total_removidos += (r1 + r2)
            total_bytes += (b1 + b2)
            self.log(f"Relatórios de Erro (WER): {r1 + r2} relatórios removidos.")

        # 6. Otimização de Entrega (Delivery Optimization)
        if self.opt_delivery.get():
            caminho_do = os.path.join(win_dir, "ServiceProfiles", "NetworkService", "AppData", "Local", "Microsoft", "Windows", "DeliveryOptimization", "Cache")
            r, i, b = self.limpar_pasta_alvo(caminho_do)
            total_removidos += r
            total_bytes += b
            self.log(f"Otimização de Entrega (P2P): {r} itens removidos ({i} em uso).")

        # 7. Windows Update Download Cache
        if self.opt_win_update.get():
            caminho_wu = os.path.join(win_dir, "SoftwareDistribution", "Download")
            r, i, b = self.limpar_pasta_alvo(caminho_wu)
            total_removidos += r
            total_bytes += b
            self.log(f"Windows Update Cache: {r} itens removidos ({i} restritos).")

        # 8. Cache DNS
        if self.opt_dns.get():
            self.limpar_dns()

        # 9. Lixeira
        if self.opt_lixeira.get():
            self.esvaziar_lixeira()

        # 10. DISM Component Cleanup
        if self.opt_dism.get():
            self.executar_dism()

        mb_liberados = total_bytes / (1024 * 1024)
        self.log(f"=== CONCLUÍDO! Espaço liberado: {mb_liberados:.2f} MB ===")
        messagebox.showinfo(
            "Limpeza Concluída", 
            f"Limpeza finalizada com sucesso!\n\nArquivos removidos: {total_removidos}\nEspaço liberado: {mb_liberados:.2f} MB"
        )

if __name__ == "__main__":
    verificar_e_elevar_admin()
    root = tk.Tk()
    app = SistemaOrganizadorApp(root)
    root.mainloop()
