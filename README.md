# 🗂️ WinTidy & DeepClean — Organizador de Arquivos e Limpeza Avançada do Windows

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)
![Platform](https://img.shields.io/badge/Plataforma-Windows%2010%20%7C%2011-0078D6?logo=windows&logoColor=white)
![Dependencies](https://img.shields.io/badge/Dependências-Nenhuma%20(StdLib)-success)
![License](https://img.shields.io/badge/Licença-MIT-green)

Uma ferramenta desktop nativa para Windows desenvolvida em **Python (`tkinter`)** que une duas rotinas essenciais de produtividade e manutenção: **organização automática de diretórios por categoria** (com sistema de backup preventivo) e **limpeza profunda de arquivos temporários e caches do sistema operacional**.

---

## 📋 Índice

- [Funcionalidades](#-funcionalidades)
- [Mapeamento de Categorias](#-mapeamento-de-categorias)
- [Módulos de Limpeza do Sistema](#-módulos-de-limpeza-do-sistema)
- [Requisitos e Instalação](#-requisitos-e-instalação)
- [Como Usar](#-como-usar)
- [Gerar Executável (.exe)](#-gerar-executável-exe)
- [Arquitetura e Segurança](#-arquitetura-e-segurança)
- [Aviso Legal](#-aviso-legal)

---

## ✨ Funcionalidades

### 1. Organizador de Arquivos Inteligente
* **Seleção Gráfica de Diretório:** Integração com o explorador de arquivos nativo do Windows.
* **Backup Automático Preventivo (`.zip`):** Compacta todo o conteúdo original da pasta selecionada em um arquivo `.zip` datado no diretório pai antes de mover qualquer arquivo.
* **Proteção Contra Sobrescrita:** Caso exista um arquivo com o mesmo nome na pasta de destino, o sistema renomeia automaticamente adicionando um sufixo numérico (`arquivo_1.pdf`, `arquivo_2.pdf`).
* **Ignora Subpastas Existentes:** Move apenas os arquivos soltos na raiz da pasta selecionada, preservando estruturas de subdiretórios já existentes.

### 2. Painel de Limpeza Profunda do Windows
* **Elevação Automática de Privilégios (UAC):** Solicita permissão de Administrador automaticamente na inicialização para acessar diretórios protegidos do Windows.
* **Execução Modular:** Caixas de seleção individuais permitem escolher exatamente quais limpezas rodar.
* **Cálculo de Espaço Liberado:** Contabiliza o tamanho em bytes de cada item removido e exibe o total liberado em **MB** ao final da operação.
* **Log em Tempo Real:** Terminal integrado na interface com registro horário (`HH:MM:SS`) de cada ação executada, arquivos movidos e itens ignorados por estarem em uso.

---

## 📂 Mapeamento de Categorias

Durante a organização, os arquivos são analisados pela extensão (case-insensitive) e distribuídos nas seguintes subpastas:

| Categoria | Extensões Suportadas |
| :--- | :--- |
| **`Imagens`** | `.jpg`, `.jpeg`, `.png`, `.gif`, `.bmp`, `.svg`, `.webp`, `.ico`, `.tiff` |
| **`Documentos`** | `.pdf`, `.doc`, `.docx`, `.txt`, `.odt`, `.rtf`, `.ppt`, `.pptx`, `.epub` |
| **`Planilhas_e_Dados`** | `.xls`, `.xlsx`, `.csv`, `.json`, `.xml`, `.sql`, `.db` |
| **`Videos`** | `.mp4`, `.mkv`, `.avi`, `.mov`, `.wmv`, `.flv`, `.webm` |
| **`Audios`** | `.mp3`, `.wav`, `.aac`, `.flac`, `.ogg`, `.wma`, `.m4a` |
| **`Compactados`** | `.zip`, `.rar`, `.7z`, `.tar`, `.gz`, `.iso` |
| **`Executaveis_e_Codigo`** | `.exe`, `.msi`, `.bat`, `.sh`, `.py`, `.js`, `.html`, `.css`, `.apk` |
| **`Outros`** | Qualquer extensão não listada acima |

---

## 🧹 Módulos de Limpeza do Sistema

| Módulo | Caminho / Comando Alvo | Descrição Técnica |
| :--- | :--- | :--- |
| **Temporários (`Temp` e `%Temp%`)** | `%LOCALAPPDATA%\Temp` e `C:\Windows\Temp` | Remove arquivos temporários de instalação e execução de aplicativos. |
| **Cache de Pré-busca (`Prefetch`)** | `C:\Windows\Prefetch` | Limpa registros antigos de inicialização rápida de programas. |
| **Miniaturas (`Thumbnails`)** | `...\Windows\Explorer\thumbcache_*` | Apaga o cache visual de pré-visualização de imagens e vídeos. |
| **Shaders DirectX (`D3DSCache`)** | `%LOCALAPPDATA%\D3DSCache` | Remove shaders compilados antigos de jogos e aplicações 3D/GPU. |
| **Relatórios de Erro (`WER`)** | `C:\ProgramData\Microsoft\Windows\WER` | Limpa logs e dumps gerados após travamentos de programas. |
| **Cache DNS** | `ipconfig /flushdns` | Redefine o cache local de resolução de nomes de domínio. |
| **Lixeira do Windows** | API Win32 (`SHEmptyRecycleBinW`) | Esvazia silenciosamente a Lixeira de todas as unidades montadas. |
| **Otimização de Entrega (P2P)** | `...\DeliveryOptimization\Cache` | Remove fragmentos de atualizações armazenados para compartilhamento em rede. |
| **Cache do Windows Update** | `C:\Windows\SoftwareDistribution\Download` | Apaga pacotes de instalação de atualizações já concluídas. |
| **Componentes do Sistema (`DISM`)** | `Dism.exe /Cleanup-Image /StartComponentCleanup` | Compacta e remove versões obsoletas de componentes na pasta `WinSxS`. |

---

## ⚙️ Requisitos e Instalação

* **Sistema Operacional:** Windows 10 ou Windows 11.
* **Python:** Versão `3.8` ou superior.
* **Dependências Externas:** **Nenhuma.** O projeto utiliza exclusivamente módulos nativos da Biblioteca Padrão do Python (`os`, `sys`, `shutil`, `zipfile`, `tempfile`, `subprocess`, `ctypes`, `datetime`, `tkinter`).

### Passo a passo para execução:

1. Clone este repositório:
   ```bash
   git clone [https://github.com/seu-usuario/wintidy-deepclean.git](https://github.com/seu-usuario/wintidy-deepclean.git)
