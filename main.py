import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
import pandas as pd
from tkcalendar import DateEntry
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import customtkinter as ctk
import ctypes
import os
import sys
import json
import pickle
import hashlib


class Toast:
    """Sistema de notificações toast modernas"""
    
    @staticmethod
    def show(parent, message, tipo='info', duration=3000):
        """
        Mostra uma notificação toast
        
        Args:
            parent: Widget pai (root)
            message: Mensagem a exibir
            tipo: 'success', 'error', 'warning', 'info'
            duration: Duração em ms (padrão 3000)
        """
        # Cores por tipo
        cores = {
            'success': {'bg': '#27ae60', 'fg': 'white', 'icon': '✅'},
            'error': {'bg': '#e74c3c', 'fg': 'white', 'icon': '❌'},
            'warning': {'bg': '#e67e22', 'fg': 'white', 'icon': '⚠️'},
            'info': {'bg': '#3498db', 'fg': 'white', 'icon': 'ℹ️'}
        }
        
        cor = cores.get(tipo, cores['info'])
        
        # Criar janela toast
        toast = tk.Toplevel(parent)
        toast.overrideredirect(True)  # Sem borda
        toast.attributes('-topmost', True)  # Sempre no topo
        
        # Frame do toast
        frame = tk.Frame(
            toast,
            bg=cor['bg'],
            relief=tk.RAISED,
            borderwidth=3
        )
        frame.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        
        # Label com mensagem
        label = tk.Label(
            frame,
            text=f"{cor['icon']}  {message}",
            font=('Quicksand', 11, 'bold'),
            bg=cor['bg'],
            fg=cor['fg'],
            padx=20,
            pady=12
        )
        label.pack()
        
        # Posicionar no canto superior direito
        toast.update_idletasks()
        width = toast.winfo_width()
        height = toast.winfo_height()
        x = parent.winfo_x() + parent.winfo_width() - width - 20
        y = parent.winfo_y() + 80
        toast.geometry(f'+{x}+{y}')
        
        # Animação de fade out e destruir
        def fade_out(alpha=1.0):
            if alpha > 0:
                alpha -= 0.05
                toast.attributes('-alpha', alpha)
                toast.after(50, lambda: fade_out(alpha))
            else:
                toast.destroy()
        
        # Agendar fade out
        toast.after(duration, fade_out)
        
        return toast


def _registrar_fontes():
    """Registra as fontes empacotadas via PyInstaller antes de abrir a janela."""
    # Quando empacotado pelo PyInstaller, arquivos de dados ficam em sys._MEIPASS
    if hasattr(sys, '_MEIPASS'):
        base = os.path.join(sys._MEIPASS, 'assets', 'fonts')
    else:
        base = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets', 'fonts')

    if not os.path.isdir(base):
        return

    gdi32 = ctypes.windll.gdi32
    for arquivo in os.listdir(base):
        if arquivo.lower().endswith(('.ttf', '.otf')):
            caminho = os.path.join(base, arquivo)
            # FR_PRIVATE (0x10) — fonte disponível apenas neste processo
            gdi32.AddFontResourceExW(caminho, 0x10, 0)

class SolicitacoesAppPro:
    def __init__(self, root):
        self.root = root
        self.root.title("⚡ Zeus - Sistema Elizeus de Controle de Solicitações")
        self.root.geometry("1600x900")
        self.root.configure(bg='#f0f0f0')
        
        self.df_original = None
        self.df_filtrado = None
        self.filtro_data_inicio = None
        self.filtro_data_fim = None
        self.progress_bar = None
        
        # Configurações
        self.config_file = 'config.json'
        self.config = self.carregar_config()
        
        # Cache
        self.cache_dir = '.cache'
        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)
        
        self.criar_interface()
        
    def criar_interface(self):
        # Frame principal
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # ========== CABEÇALHO ==========
        header_frame = tk.Frame(main_frame, bg='#2c3e50', height=70)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        header_frame.pack_propagate(False)
        
        # Container centralizado para título e subtítulo lado a lado
        header_content = tk.Frame(header_frame, bg='#2c3e50')
        header_content.place(relx=0.5, rely=0.5, anchor='center')
        
        # Título principal
        title_label = tk.Label(
            header_content,
            text="⚡ Zeus",
            font=('Quicksand', 28, 'bold'),
            bg='#2c3e50',
            fg='#FFD700'  # Dourado
        )
        title_label.pack(side=tk.LEFT, padx=(0, 15))
        
        # Separador vertical
        separator = tk.Label(
            header_content,
            text="│",
            font=('Quicksand', 24, 'bold'),
            bg='#2c3e50',
            fg='#7f8c8d'  # Cinza
        )
        separator.pack(side=tk.LEFT, padx=(0, 15))
        
        # Subtítulo
        subtitle_label = tk.Label(
            header_content,
            text='Sistema Elizeus de Controle de Solicitações',
            font=('Quicksand', 14, 'bold'),
            bg='#2c3e50',
            fg='#ecf0f1'  # Branco suave
        )
        subtitle_label.pack(side=tk.LEFT)
        
        # ========== PAINEL DE CONTROLE ==========
        control_frame = ctk.CTkFrame(
            main_frame,
            corner_radius=15,
            border_width=2,
            fg_color='white',
            border_color='#bdc3c7'
        )
        control_frame.pack(fill=tk.X, pady=(0, 10), padx=5)
        
        # Linha 1: Arquivo
        file_frame = tk.Frame(control_frame, bg='white')
        file_frame.pack(fill=tk.X, padx=15, pady=10)
        
        tk.Label(
            file_frame,
            text="📂 Arquivo:",
            font=('Quicksand', 14, 'bold'),
            bg='white'
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        self.arquivo_entry = ctk.CTkEntry(
            file_frame,
            font=('Quicksand', 11),
            width=400,
            height=36,
            corner_radius=8,
            border_width=2
        )
        self.arquivo_entry.insert(0, self.config.get('ultimo_arquivo', 'simecr05.xlsx'))
        self.arquivo_entry.pack(side=tk.LEFT, padx=(0, 10))
        
        ctk.CTkButton(
            file_frame,
            text="Procurar...",
            command=self.selecionar_arquivo,
            fg_color='#3498db',
            hover_color='#2980b9',
            text_color='white',
            font=('Quicksand', 12, 'bold'),
            cursor='hand2',
            corner_radius=8,
            width=130,
            height=36
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        ctk.CTkButton(
            file_frame,
            text="🔄 Carregar Dados",
            command=self.carregar_dados,
            fg_color='#27ae60',
            hover_color='#229954',
            text_color='white',
            font=('Quicksand', 12, 'bold'),
            cursor='hand2',
            corner_radius=8,
            width=170,
            height=36
        ).pack(side=tk.LEFT)
        
        # Linha 2: Filtros de Data
        filter_frame = tk.Frame(control_frame, bg='white')
        filter_frame.pack(fill=tk.X, padx=15, pady=(0, 10))
        
        tk.Label(
            filter_frame,
            text="📅 Filtrar por Data de Emissão:",
            font=('Quicksand', 14, 'bold'),
            bg='white'
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Label(filter_frame, text="De:", font=('Quicksand', 13, 'bold'), bg='white').pack(side=tk.LEFT, padx=(0, 5))
        self.data_inicio = DateEntry(
            filter_frame,
            font=('Quicksand', 9),
            width=12,
            background='#3498db',
            foreground='white',
            borderwidth=2,
            date_pattern='dd/mm/yyyy',
            locale='pt_BR'
        )
        self.data_inicio.pack(side=tk.LEFT, padx=(0, 20))
        
        tk.Label(filter_frame, text="Até:", font=('Quicksand', 13, 'bold'), bg='white').pack(side=tk.LEFT, padx=(10, 5))
        self.data_fim = DateEntry(
            filter_frame,
            font=('Quicksand', 9),
            width=12,
            background='#3498db',
            foreground='white',
            borderwidth=2,
            date_pattern='dd/mm/yyyy',
            locale='pt_BR'
        )
        self.data_fim.pack(side=tk.LEFT, padx=(0, 20))
        
        # Atalhos de data
        tk.Label(filter_frame, text="Atalhos:", font=('Quicksand', 13, 'bold'), bg='white').pack(side=tk.LEFT, padx=(0, 5))
        
        ctk.CTkButton(
            filter_frame,
            text="Hoje",
            command=lambda: self.aplicar_atalho_data('hoje'),
            fg_color='#9b59b6',
            hover_color='#8e44ad',
            text_color='white',
            font=('Quicksand', 11, 'bold'),
            cursor='hand2',
            corner_radius=6,
            width=80,
            height=32
        ).pack(side=tk.LEFT, padx=2)
        
        ctk.CTkButton(
            filter_frame,
            text="Semana",
            command=lambda: self.aplicar_atalho_data('semana'),
            fg_color='#9b59b6',
            hover_color='#8e44ad',
            text_color='white',
            font=('Quicksand', 11, 'bold'),
            cursor='hand2',
            corner_radius=6,
            width=80,
            height=32
        ).pack(side=tk.LEFT, padx=2)
        
        ctk.CTkButton(
            filter_frame,
            text="Mês",
            command=lambda: self.aplicar_atalho_data('mes'),
            fg_color='#9b59b6',
            hover_color='#8e44ad',
            text_color='white',
            font=('Quicksand', 11, 'bold'),
            cursor='hand2',
            corner_radius=6,
            width=80,
            height=32
        ).pack(side=tk.LEFT, padx=(2, 20))
        
        ctk.CTkButton(
            filter_frame,
            text="🔍 Aplicar Filtro",
            command=self.aplicar_filtro_data,
            fg_color='#e67e22',
            hover_color='#d35400',
            text_color='white',
            font=('Quicksand', 12, 'bold'),
            cursor='hand2',
            corner_radius=8,
            width=150,
            height=36
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        ctk.CTkButton(
            filter_frame,
            text="🔄 Limpar Filtro",
            command=self.limpar_filtro,
            fg_color='#95a5a6',
            hover_color='#7f8c8d',
            text_color='white',
            font=('Quicksand', 12, 'bold'),
            cursor='hand2',
            corner_radius=8,
            width=150,
            height=36
        ).pack(side=tk.LEFT)
        
        # ========== SISTEMA DE ABAS ==========
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Estilo das abas
        style = ttk.Style()
        style.configure('TNotebook.Tab', font=('Quicksand', 12, 'bold'), padding=[20, 10])
        
        # Criar abas
        self.criar_aba_dados()
        self.criar_aba_status_atendimento()
        self.criar_aba_dashboard()
        self.criar_aba_analise()
        self.criar_aba_resumo()
        
        # ========== RODAPÉ ==========
        footer_frame = tk.Frame(main_frame, bg='#2c3e50', height=40)
        footer_frame.pack(fill=tk.X)
        footer_frame.pack_propagate(False)
        
        tk.Label(
            footer_frame,
            text="© 2026 DBSolutions Lab - Desenvolvido por Diego Bernardes",
            font=('Quicksand', 9),
            bg='#2c3e50',
            fg='white'
        ).pack(pady=10)
    
    # ==================== ABA 1: DADOS ====================
    def criar_aba_dados(self):
        self.aba_dados = tk.Frame(self.notebook, bg='#e8f4f8')  # Azul claro
        self.notebook.add(self.aba_dados, text='📋 Solicitações Pendentes')
        
        # Info e exportação
        info_frame = ctk.CTkFrame(
            self.aba_dados,
            corner_radius=12,
            border_width=2,
            fg_color='white',
            border_color='#3498db'
        )
        info_frame.pack(fill=tk.X, pady=(10, 10), padx=10)
        
        self.info_label = tk.Label(
            info_frame,
            text="📊 Nenhum dado carregado",
            font=('Quicksand', 10, 'bold'),
            bg='white',
            fg='#7f8c8d',
            anchor='w'
        )
        self.info_label.pack(side=tk.LEFT, padx=15, pady=8)
        
        # Progress bar (inicialmente oculta)
        self.progress_bar = ctk.CTkProgressBar(
            info_frame,
            width=200,
            height=8,
            corner_radius=4,
            fg_color='#ecf0f1',
            progress_color='#3498db'
        )
        
        # Badge de filtro ativo
        self.filtro_badge = tk.Label(
            info_frame,
            text="",
            font=('Quicksand', 9, 'bold'),
            bg='white',
            fg='white',
            padx=10,
            pady=3
        )
        self.filtro_badge.pack(side=tk.LEFT, padx=(0, 15))
        
        ctk.CTkButton(
            info_frame,
            text="💾 Exportar para Excel",
            command=self.exportar_excel,
            fg_color='#16a085',
            hover_color='#138d75',
            text_color='white',
            font=('Quicksand', 9, 'bold'),
            cursor='hand2',
            corner_radius=8,
            width=180
        ).pack(side=tk.RIGHT, padx=15, pady=5)
        
        # Título centralizado
        title_frame = ctk.CTkFrame(
            self.aba_dados,
            corner_radius=10,
            height=60,
            fg_color='#2c3e50'
        )
        title_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        title_frame.pack_propagate(False)
        
        tk.Label(
            title_frame,
            text="📋 Solicitações Pendentes",
            font=('Quicksand', 18, 'bold'),
            bg='#2c3e50',
            fg='#FFD700'
        ).pack(expand=True)
        
        # Campo de busca
        search_frame = ctk.CTkFrame(
            self.aba_dados,
            corner_radius=10,
            border_width=2,
            fg_color='white',
            border_color='#95a5a6'
        )
        search_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        tk.Label(
            search_frame,
            text="🔍 Buscar:",
            font=('Quicksand', 10, 'bold'),
            bg='white'
        ).pack(side=tk.LEFT, padx=(15, 5), pady=8)
        
        self.search_var = tk.StringVar()
        self.search_var.trace('w', lambda *args: self.filtrar_tabela_busca())
        
        search_entry = ctk.CTkEntry(
            search_frame,
            textvariable=self.search_var,
            font=('Quicksand', 10),
            width=400,
            height=32,
            corner_radius=8,
            border_width=2,
            placeholder_text="Digite para buscar..."
        )
        search_entry.pack(side=tk.LEFT, padx=(0, 10), pady=8)
        
        tk.Label(
            search_frame,
            text="(Busca por Descrição, Setor, Solicitante, Código)",
            font=('Quicksand', 8),
            bg='white',
            fg='#7f8c8d'
        ).pack(side=tk.LEFT, padx=(0, 15))
        
        # Tabela
        table_frame = tk.Frame(self.aba_dados, bg='white', relief=tk.RAISED, borderwidth=2)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        # Configurar grid
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)
        
        self.tree = ttk.Treeview(
            table_frame,
            selectmode='extended'
        )
        
        scroll_y = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        scroll_x = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        
        self.tree.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
        
        self.tree.grid(row=0, column=0, sticky='nsew')
        scroll_y.grid(row=0, column=1, sticky='ns')
        scroll_x.grid(row=1, column=0, sticky='ew')
        
        style = ttk.Style()
        style.theme_use('clam')
        style.configure(
            'Treeview',
            background='white',
            foreground='black',
            rowheight=25,
            fieldbackground='white',
            font=('Quicksand', 9)
        )
        style.configure('Treeview.Heading', font=('Quicksand', 10, 'bold'), background='#34495e', foreground='white')
        style.map('Treeview', background=[('selected', '#3498db')])
    
    # ==================== ABA 2: STATUS DE ATENDIMENTO ====================
    def criar_aba_status_atendimento(self):
        self.aba_status = tk.Frame(self.notebook, bg='#e8f8f5')  # Verde claro
        self.notebook.add(self.aba_status, text='✅ Status de Atendimento')
        
        # Info e KPIs
        info_frame = ctk.CTkFrame(
            self.aba_status,
            corner_radius=12,
            border_width=2,
            fg_color='white',
            border_color='#27ae60'
        )
        info_frame.pack(fill=tk.X, pady=(10, 10), padx=10)
        
        self.status_info_label = tk.Label(
            info_frame,
            text="📊 Nenhum dado carregado",
            font=('Quicksand', 10, 'bold'),
            bg='white',
            fg='#7f8c8d',
            anchor='w'
        )
        self.status_info_label.pack(side=tk.LEFT, padx=15, pady=8)
        
        # KPIs de atendimento com badges coloridos
        self.kpi_atendidas = tk.Label(
            info_frame,
            text="",
            font=('Quicksand', 10, 'bold'),
            bg='#d5f4e6',
            fg='#27ae60',
            padx=12,
            pady=6,
            relief=tk.RAISED,
            borderwidth=2
        )
        self.kpi_atendidas.pack(side=tk.LEFT, padx=10)
        
        self.kpi_parciais = tk.Label(
            info_frame,
            text="",
            font=('Quicksand', 10, 'bold'),
            bg='#fdebd0',
            fg='#e67e22',
            padx=12,
            pady=6,
            relief=tk.RAISED,
            borderwidth=2
        )
        self.kpi_parciais.pack(side=tk.LEFT, padx=10)
        
        self.kpi_nao_atendidas = tk.Label(
            info_frame,
            text="",
            font=('Quicksand', 10, 'bold'),
            bg='#fadbd8',
            fg='#e74c3c',
            padx=12,
            pady=6,
            relief=tk.RAISED,
            borderwidth=2
        )
        self.kpi_nao_atendidas.pack(side=tk.LEFT, padx=10)
        
        ctk.CTkButton(
            info_frame,
            text="💾 Exportar para Excel",
            command=self.exportar_status_excel,
            fg_color='#16a085',
            hover_color='#138d75',
            text_color='white',
            font=('Quicksand', 9, 'bold'),
            cursor='hand2',
            corner_radius=8,
            width=180
        ).pack(side=tk.RIGHT, padx=15, pady=5)
        
        # Título centralizado
        title_frame = ctk.CTkFrame(
            self.aba_status,
            corner_radius=10,
            height=60,
            fg_color='#2c3e50'
        )
        title_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        title_frame.pack_propagate(False)
        
        tk.Label(
            title_frame,
            text="✅ Controle de Atendimento das Solicitações",
            font=('Quicksand', 18, 'bold'),
            bg='#2c3e50',
            fg='#FFD700'
        ).pack(expand=True)
        
        # Filtro de Status de Atendimento
        filtro_status_frame = ctk.CTkFrame(
            self.aba_status,
            corner_radius=10,
            border_width=2,
            fg_color='white',
            border_color='#27ae60'
        )
        filtro_status_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        tk.Label(
            filtro_status_frame,
            text="🔍 Filtrar por Status:",
            font=('Quicksand', 10, 'bold'),
            bg='white'
        ).pack(side=tk.LEFT, padx=15, pady=8)
        
        self.filtro_atendimento_var = tk.StringVar(value="Todas")
        filtro_combo = ctk.CTkComboBox(
            filtro_status_frame,
            variable=self.filtro_atendimento_var,
            values=["Todas", "TOTALMENTE ATENDIDA", "PARCIALMENTE ATENDIDA", "NÃO ATENDIDA"],
            state='readonly',
            font=('Quicksand', 9),
            width=280,
            height=32,
            corner_radius=8,
            border_width=2,
            command=lambda choice: self.aplicar_filtro_atendimento()
        )
        filtro_combo.pack(side=tk.LEFT, padx=(0, 20), pady=8)
        
        # Campo de busca
        search_frame = ctk.CTkFrame(
            self.aba_status,
            corner_radius=10,
            border_width=2,
            fg_color='white',
            border_color='#95a5a6'
        )
        search_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        tk.Label(
            search_frame,
            text="🔍 Buscar:",
            font=('Quicksand', 10, 'bold'),
            bg='white'
        ).pack(side=tk.LEFT, padx=(15, 5), pady=8)
        
        self.status_search_var = tk.StringVar()
        self.status_search_var.trace('w', lambda *args: self.filtrar_status_busca())
        
        search_entry = ctk.CTkEntry(
            search_frame,
            textvariable=self.status_search_var,
            font=('Quicksand', 10),
            width=400,
            height=32,
            corner_radius=8,
            border_width=2,
            placeholder_text="Digite para buscar..."
        )
        search_entry.pack(side=tk.LEFT, padx=(0, 10), pady=8)
        
        tk.Label(
            search_frame,
            text="(Busca por Descrição, Setor, Solicitante, Código)",
            font=('Quicksand', 8),
            bg='white',
            fg='#7f8c8d'
        ).pack(side=tk.LEFT, padx=(0, 15))
        
        # Tabela
        table_frame = tk.Frame(self.aba_status, bg='white', relief=tk.RAISED, borderwidth=2)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        # Configurar grid
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)
        
        self.status_tree = ttk.Treeview(
            table_frame,
            style='Treeview'
        )
        
        scroll_y = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.status_tree.yview)
        scroll_x = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL, command=self.status_tree.xview)
        
        self.status_tree.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
        
        self.status_tree.grid(row=0, column=0, sticky='nsew')
        scroll_y.grid(row=0, column=1, sticky='ns')
        scroll_x.grid(row=1, column=0, sticky='ew')
    
    # ==================== ABA 3: DASHBOARD ====================
    def criar_aba_dashboard(self):
        self.aba_dashboard = tk.Frame(self.notebook, bg='#fef5e7')  # Amarelo claro
        self.notebook.add(self.aba_dashboard, text='📊 Dashboard')
        
        # Container com scroll
        canvas = tk.Canvas(self.aba_dashboard, bg='#fef5e7')
        scrollbar = ttk.Scrollbar(self.aba_dashboard, orient="vertical", command=canvas.yview)
        self.dashboard_frame = tk.Frame(canvas, bg='#fef5e7')
        
        self.dashboard_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.dashboard_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Placeholder
        tk.Label(
            self.dashboard_frame,
            text="📊 Dashboard será atualizado após carregar os dados",
            font=('Quicksand', 14),
            bg='#fef5e7',
            fg='#7f8c8d'
        ).pack(pady=50)
    
    # ==================== ABA 3: ANÁLISE DETALHADA ====================
    def criar_aba_analise(self):
        self.aba_analise = tk.Frame(self.notebook, bg='#f4ecf7')  # Roxo claro
        self.notebook.add(self.aba_analise, text='📈 Análise Detalhada')
        
        # Container com scroll
        canvas = tk.Canvas(self.aba_analise, bg='#f4ecf7')
        scrollbar = ttk.Scrollbar(self.aba_analise, orient="vertical", command=canvas.yview)
        self.analise_frame = tk.Frame(canvas, bg='#f4ecf7')
        
        self.analise_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.analise_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Placeholder
        tk.Label(
            self.analise_frame,
            text="📈 Análise será atualizada após carregar os dados",
            font=('Quicksand', 14),
            bg='#f4ecf7',
            fg='#7f8c8d'
        ).pack(pady=50)
    
    # ==================== ABA 4: RESUMO EXECUTIVO ====================
    def criar_aba_resumo(self):
        self.aba_resumo = tk.Frame(self.notebook, bg='#fdecea')  # Rosa claro
        self.notebook.add(self.aba_resumo, text='📄 Resumo Executivo')
        
        # Botão de exportar
        btn_frame = tk.Frame(self.aba_resumo, bg='white')
        btn_frame.pack(fill=tk.X, padx=20, pady=10)
        
        ctk.CTkButton(
            btn_frame,
            text=" Exportar Resumo (TXT)",
            command=self.exportar_resumo,
            fg_color='#16a085',
            hover_color='#138d75',
            text_color='white',
            font=('Quicksand', 10, 'bold'),
            cursor='hand2',
            corner_radius=8,
            width=220
        ).pack(side=tk.RIGHT, padx=(0, 20))

        ctk.CTkButton(
            btn_frame,
            text=" Exportar Relatório (PDF)",
            command=self.exportar_pdf,
            fg_color='#c0392b',
            hover_color='#a93226',
            text_color='white',
            font=('Quicksand', 10, 'bold'),
            cursor='hand2',
            corner_radius=8,
            width=220
        ).pack(side=tk.RIGHT, padx=(0, 10))
        
        # Área de texto com scroll
        text_frame = tk.Frame(self.aba_resumo, bg='white')
        text_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        scroll_resumo = ttk.Scrollbar(text_frame)
        scroll_resumo.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.resumo_text = tk.Text(
            text_frame,
            font=('Consolas', 10),
            bg='#f8f9fa',
            fg='#2c3e50',
            yscrollcommand=scroll_resumo.set,
            wrap=tk.WORD,
            padx=20,
            pady=20
        )
        self.resumo_text.pack(fill=tk.BOTH, expand=True)
        scroll_resumo.config(command=self.resumo_text.yview)
        
        self.resumo_text.insert('1.0', "📄 Resumo Executivo será gerado após carregar os dados")
        self.resumo_text.config(state=tk.DISABLED)
    
    # ==================== FUNÇÕES DE DADOS ====================
    def selecionar_arquivo(self):
        filename = filedialog.askopenfilename(
            title="Selecionar arquivo Excel",
            filetypes=[("Excel files", "*.xlsx *.xls"), ("All files", "*.*")]
        )
        if filename:
            self.arquivo_entry.delete(0, tk.END)
            self.arquivo_entry.insert(0, filename)
    
    def carregar_dados(self):
        arquivo = self.arquivo_entry.get()
        
        if not arquivo:
            Toast.show(
                self.root,
                "Selecione um arquivo Excel primeiro",
                tipo='warning',
                duration=3000
            )
            return
        
        # Salvar último arquivo usado
        self.config['ultimo_arquivo'] = arquivo
        self.salvar_config()
        
        # Mostrar loading state com progress bar
        self.info_label.config(
            text="⏳ Carregando dados...",
            fg='#e67e22'
        )
        self.progress_bar.set(0)
        self.progress_bar.pack(side=tk.LEFT, padx=10)
        self.root.update()
        
        try:
            # Tentar carregar do cache primeiro
            cache_data = self.carregar_do_cache(arquivo)
            
            if cache_data is not None:
                # Dados do cache
                self.df_original = cache_data['df_original']
                self.df_status_original = cache_data['df_status_original']
                self.df_filtrado = self.df_original.copy()
                self.df_status_filtrado = self.df_status_original.copy()
                self.progress_bar.set(0.5)
                self.root.update()
            else:
                # Carregar do Excel (primeira vez ou arquivo modificado)
                df = pd.read_excel(arquivo, sheet_name='Relatório de Controle de entr')
                self.progress_bar.set(0.2)
                self.root.update()
                
                # Excluir apenas grupos (df_original = base para Dashboard/Análise/Resumo)
                grupos_excluir = [4003, 4037]
                df_base = df[~df['Grupo'].isin(grupos_excluir)]
                self.progress_bar.set(0.4)
                self.root.update()
                
                # Mapeamento para aba Dados e Dashboard
                colunas_mapeamento = {
                'Numero SA': 'Numero SA',
                'Codigo': 'Codigo',
                'Descricao do Material': 'Descricao',
                'UM': 'Unidade de Medida',
                'Armazem': 'Armazem',
                'Quantidade': 'Quantidade',
                'Dt. Emissao': 'Data Emissao',
                'Status': 'Status',
                'Setor': 'Setor',
                'Solicitante': 'Solicitante',
                'Observacao': 'Observacao'
            }
            
            # Mapeamento adicional para aba Status de Atendimento
            colunas_status_mapeamento = {
                'Numero SA': 'Numero SA',
                'Codigo': 'Codigo',
                'Descricao do Material': 'Descricao',
                'UM': 'Unidade de Medida',
                'Armazem': 'Armazem',
                'Quantidade': 'Quantidade Solicitada',
                'Qtd. Atendida': 'Qtd. Atendida',
                'Atendimento': 'Atendimento',
                'Dt. Emissao': 'Data Emissao',
                'Dt. Atendido': 'Dt. Atendido',
                'Setor': 'Setor',
                'Solicitante': 'Solicitante',
                'Custo Unitario': 'Custo Unitario',
                'Custo Total': 'Custo Total'
            }
            
            # Criar df_base para abas normais
            df_base = df_base[list(colunas_mapeamento.keys())]
            df_base = df_base.rename(columns=colunas_mapeamento)
            df_base['Data Emissao'] = pd.to_datetime(df_base['Data Emissao'], errors='coerce')
            
            # Criar df_status_base para aba Status de Atendimento
            df_status_base = df[~df['Grupo'].isin(grupos_excluir)]
            df_status_base = df_status_base[list(colunas_status_mapeamento.keys())]
            df_status_base = df_status_base.rename(columns=colunas_status_mapeamento)
            df_status_base['Data Emissao'] = pd.to_datetime(df_status_base['Data Emissao'], errors='coerce')
            df_status_base['Dt. Atendido'] = pd.to_datetime(df_status_base['Dt. Atendido'], errors='coerce')
            
            # df_original = TODOS os dados (sem grupos, mas COM todos os status)
            self.df_original = df_base.copy()
            
            # df_filtrado = inicialmente igual ao df_original (Dashboard usa isso)
            self.df_filtrado = df_base.copy()
            
            # Para aba Dados: filtrar status (sem EM APROVAÇÃO e PRE-REQUISIÇÃO GERADA)
            status_excluir = ['EM APROVAÇÃO', 'PRE-REQUISIÇÃO GERADA']
            df_dados = df_base[~df_base['Status'].isin(status_excluir)].copy()
            
            # Para aba Status de Atendimento: guardar dados completos
            self.df_status_original = df_status_base.copy()
            self.df_status_filtrado = df_status_base.copy()
            
            # Salvar no cache
            self.salvar_no_cache(arquivo, {
                'df_original': self.df_original,
                'df_status_original': self.df_status_original
            })
            
            # Para aba Dados: filtrar status (sem EM APROVAÇÃO e PRE-REQUISIÇÃO GERADA)
            status_excluir = ['EM APROVAÇÃO', 'PRE-REQUISIÇÃO GERADA']
            df_dados = self.df_original[~self.df_original['Status'].isin(status_excluir)].copy()
            
            # Atualizar tabela da aba Dados (COM filtro de status)
            self.progress_bar.set(0.6)
            self.root.update()
            self.atualizar_tabela(df_dados)
            
            # Atualizar aba Status de Atendimento
            self.atualizar_tabela_status(self.df_status_filtrado)
            
            # Atualizar Dashboard/Análise/Resumo (SEM filtro de status - usa df_filtrado)
            self.progress_bar.set(0.8)
            self.root.update()
            self.atualizar_dashboard()
            self.atualizar_analise()
            self.atualizar_resumo()
            
            # Finalizar progress bar
            self.progress_bar.set(1.0)
            self.root.update()
            self.root.after(500, self.progress_bar.pack_forget)  # Esconder após 500ms
            
            # Toast de sucesso
            if cache_data is not None:
                Toast.show(
                    self.root,
                    f"⚡ Cache: {len(self.df_original)} registros carregados instantaneamente",
                    tipo='info',
                    duration=3000
                )
            else:
                Toast.show(
                    self.root,
                    f"Dados carregados! {len(self.df_original)} registros prontos",
                    tipo='success',
                    duration=3000
                )
            
        except FileNotFoundError:
            self.progress_bar.pack_forget()
            self.info_label.config(text="❌ Arquivo não encontrado", fg='#e74c3c')
            Toast.show(
                self.root,
                f"Arquivo não encontrado: {os.path.basename(arquivo)}",
                tipo='error',
                duration=4000
            )
        except PermissionError:
            self.progress_bar.pack_forget()
            self.info_label.config(text="❌ Sem permissão para ler o arquivo", fg='#e74c3c')
            Toast.show(
                self.root,
                "Feche o arquivo Excel e tente novamente",
                tipo='warning',
                duration=4000
            )
        except pd.errors.ParserError:
            self.progress_bar.pack_forget()
            self.info_label.config(text="❌ Erro ao ler Excel", fg='#e74c3c')
            Toast.show(
                self.root,
                "Formato do arquivo Excel inválido",
                tipo='error',
                duration=4000
            )
        except KeyError as e:
            self.progress_bar.pack_forget()
            self.info_label.config(text="❌ Coluna não encontrada", fg='#e74c3c')
            Toast.show(
                self.root,
                f"Coluna esperada não encontrada: {str(e)}",
                tipo='error',
                duration=4000
            )
        except Exception as e:
            self.progress_bar.pack_forget()
            self.info_label.config(text="❌ Erro ao carregar dados", fg='#e74c3c')
            error_msg = str(e)
            if len(error_msg) > 100:
                error_msg = error_msg[:100] + "..."
            Toast.show(
                self.root,
                f"Erro: {error_msg}",
                tipo='error',
                duration=5000
            )
            print(f"Erro detalhado: {e}")  # Log completo no console
    
    def atualizar_tabela(self, df):
        self.tree.delete(*self.tree.get_children())
        
        if df is None or df.empty:
            self.info_label.config(text="📊 Nenhum dado para exibir")
            return
        
        colunas = list(df.columns)
        self.tree['columns'] = colunas
        self.tree['show'] = 'headings'
        
        for col in colunas:
            self.tree.heading(col, text=col)
            
            if col == 'Descricao':
                width = 400
            elif col == 'Observacao':
                width = 200
            elif col == 'Setor':
                width = 325
            elif col == 'Solicitante':
                width = 150
            elif col == 'Status':
                width = 145
            elif col == 'Data Emissao':
                width = 70
                self.tree.heading(col, text='Dt.Emissão')
            elif col in ['Numero SA', 'Codigo']:
                width = 90
            elif col == 'Armazem':
                width = 100
            elif col == 'Quantidade':
                width = 90
            elif col == 'Unidade de Medida':
                width = 50
                self.tree.heading(col, text='U.M.')
            else:
                width = 120
            
            self.tree.column(col, width=width, anchor='w')
        
        for idx, row in df.iterrows():
            valores = []
            for col in colunas:
                valor = row[col]
                if pd.isna(valor):
                    valores.append('')
                elif col == 'Data Emissao' and isinstance(valor, pd.Timestamp):
                    valores.append(valor.strftime('%d/%m/%Y'))
                elif col == 'Quantidade':
                    if valor == int(valor):
                        valores.append(str(int(valor)))
                    else:
                        valores.append(str(valor))
                else:
                    valores.append(str(valor))
            
            self.tree.insert('', tk.END, values=valores)
        
        self.info_label.config(
            text=f"📊 Exibindo {df['Numero SA'].nunique()} solicitações | "
                 f"Quantidade total de itens: {len(df)}",
            fg='#27ae60'
        )
    
    def aplicar_atalho_data(self, tipo):
        """Aplicar atalhos de data (Hoje, Semana, Mês)"""
        from datetime import datetime, timedelta
        
        hoje = datetime.now().date()
        
        if tipo == 'hoje':
            self.data_inicio.set_date(hoje)
            self.data_fim.set_date(hoje)
        elif tipo == 'semana':
            # Início da semana (segunda-feira)
            inicio_semana = hoje - timedelta(days=hoje.weekday())
            self.data_inicio.set_date(inicio_semana)
            self.data_fim.set_date(hoje)
        elif tipo == 'mes':
            # Primeiro dia do mês
            inicio_mes = hoje.replace(day=1)
            self.data_inicio.set_date(inicio_mes)
            self.data_fim.set_date(hoje)
        
        # Aplicar filtro automaticamente
        self.aplicar_filtro_data()
    
    def aplicar_filtro_data(self):
        if self.df_original is None:
            Toast.show(
                self.root,
                "Carregue os dados primeiro",
                tipo='warning',
                duration=3000
            )
            return
        
        try:
            data_inicio = self.data_inicio.get_date()
            data_fim = self.data_fim.get_date()
            
            data_inicio_pd = pd.Timestamp(data_inicio)
            data_fim_pd = pd.Timestamp(data_fim)
            
            if data_inicio_pd > data_fim_pd:
                Toast.show(
                    self.root,
                    "Data inicial não pode ser maior que a final",
                    tipo='warning',
                    duration=3000
                )
                return
            
            # Guardar datas do filtro
            self.filtro_data_inicio = data_inicio_pd
            self.filtro_data_fim = data_fim_pd
            
            # Filtrar por data (para Dashboard/Análise/Resumo)
            df_filtrado_data = self.df_original[
                (self.df_original['Data Emissao'] >= data_inicio_pd) &
                (self.df_original['Data Emissao'] <= data_fim_pd)
            ]
            
            # Para aba Dados: aplicar filtro de status também
            status_excluir = ['EM APROVAÇÃO', 'PRE-REQUISIÇÃO GERADA']
            df_dados = df_filtrado_data[~df_filtrado_data['Status'].isin(status_excluir)]
            
            # df_filtrado = usado por Dashboard/Análise/Resumo (SEM filtro de status)
            self.df_filtrado = df_filtrado_data.copy()
            
            # Filtrar aba Status de Atendimento por data também
            if hasattr(self, 'df_status_original'):
                df_status_filtrado_data = self.df_status_original[
                    (self.df_status_original['Data Emissao'] >= data_inicio_pd) &
                    (self.df_status_original['Data Emissao'] <= data_fim_pd)
                ]
                self.df_status_filtrado = df_status_filtrado_data.copy()
            
            # Atualizar tabela da aba Dados (COM filtro de status)
            self.atualizar_tabela(df_dados)
            
            # Atualizar aba Status de Atendimento
            if hasattr(self, 'df_status_filtrado'):
                self.atualizar_tabela_status(self.df_status_filtrado)
            
            # Atualizar Dashboard/Análise/Resumo (SEM filtro de status)
            self.atualizar_dashboard()
            self.atualizar_analise()
            self.atualizar_resumo()
            
            # Atualizar badge de filtro ativo
            self.filtro_badge.config(
                text=f"🔍 FILTRO ATIVO: {data_inicio.strftime('%d/%m/%Y')} - {data_fim.strftime('%d/%m/%Y')}",
                bg='#3498db',
                fg='white'
            )
            
            # Toast de sucesso
            Toast.show(
                self.root,
                f"Filtro aplicado: {len(self.df_filtrado)} registros encontrados",
                tipo='success',
                duration=3000
            )
            
        except ValueError as e:
            Toast.show(
                self.root,
                "Data inválida selecionada",
                tipo='warning',
                duration=3000
            )
        except Exception as e:
            Toast.show(
                self.root,
                f"Erro ao aplicar filtro: {str(e)[:80]}",
                tipo='error',
                duration=4000
            )
            print(f"Erro detalhado ao filtrar: {e}")
    
    def limpar_filtro(self):
        if self.df_original is None:
            Toast.show(
                self.root,
                "Carregue os dados primeiro",
                tipo='warning',
                duration=3000
            )
            return
        
        # Limpar datas do filtro
        self.filtro_data_inicio = None
        self.filtro_data_fim = None
        
        # Para aba Dados: filtrar status (excluir 'EM APROVAÇÃO' e 'PRE-REQUISIÇÃO GERADA')
        status_excluir = ['EM APROVAÇÃO', 'PRE-REQUISIÇÃO GERADA']
        df_dados = self.df_original[~self.df_original['Status'].isin(status_excluir)]
        
        # Para Dashboard/Análise/Resumo: usar df_original completo
        self.df_filtrado = self.df_original.copy()
        
        # Restaurar dados originais da aba Status de Atendimento
        if hasattr(self, 'df_status_original'):
            self.df_status_filtrado = self.df_status_original.copy()
        
        # Atualizar apenas a tabela da aba Dados com filtro de status
        self.atualizar_tabela(df_dados)
        
        # Atualizar aba Status de Atendimento
        if hasattr(self, 'df_status_filtrado'):
            self.atualizar_tabela_status(self.df_status_filtrado)
        
        # Dashboard/Análise/Resumo usam df_filtrado (sem filtro de status)
        self.atualizar_dashboard()
        self.atualizar_analise()
        self.atualizar_resumo()
        
        # Remover badge de filtro
        self.filtro_badge.config(text="", bg='white')
        
        # Toast de info
        Toast.show(
            self.root,
            "Filtro removido. Exibindo todos os dados",
            tipo='info',
            duration=2500
        )
    
    # ==================== ATUALIZAR DASHBOARD ====================
    def atualizar_dashboard(self):
        # Limpar dashboard
        for widget in self.dashboard_frame.winfo_children():
            widget.destroy()
        
        if self.df_filtrado is None or self.df_filtrado.empty:
            tk.Label(
                self.dashboard_frame,
                text="📊 Nenhum dado para exibir",
                font=('Quicksand', 14),
                bg='#ecf0f1',
                fg='#7f8c8d'
            ).pack(pady=50)
            return
        
        df = self.df_filtrado
        
        # ========== KPIs ==========
        kpi_frame = tk.Frame(self.dashboard_frame, bg='#ecf0f1')
        kpi_frame.pack(fill=tk.X, padx=20, pady=20)
        
        # Filtrar dados excluindo 'EM APROVAÇÃO' para os KPIs
        df_kpi = df[df['Status'] != 'EM APROVAÇÃO'].copy() if 'Status' in df.columns else df.copy()
        
        # Total de Solicitações: SAs únicas (sem 'EM APROVAÇÃO')
        total_sas = df_kpi['Numero SA'].nunique()
        
        # Total de Itens: Total de linhas (códigos) sem 'EM APROVAÇÃO'
        total_itens = len(df_kpi)
        
        # Média de Itens por SA
        media_itens_sa = round(total_itens / total_sas, 2) if total_sas > 0 else 0
        
        kpis = [
            ("📦 Total de Solicitações", total_sas, "#3498db"),
            ("📊 Total de Itens", total_itens, "#27ae60"),
            ("🏢 Setores Ativos", df_kpi['Setor'].nunique(), "#e67e22"),
            ("👥 Solicitantes", df_kpi['Solicitante'].nunique(), "#9b59b6"),
            ("📈 Média Itens/SA", media_itens_sa, "#e74c3c")
        ]
        
        for titulo, valor, cor in kpis:
            self.criar_kpi_card(kpi_frame, titulo, valor, cor).pack(side=tk.LEFT, padx=10, expand=True, fill=tk.BOTH)
        
        # ========== GRÁFICOS ==========
        graficos_frame = tk.Frame(self.dashboard_frame, bg='#ecf0f1')
        graficos_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        # Apenas 2 gráficos lado a lado: Top Setores + Top Solicitantes
        self.criar_grafico_top_setores(graficos_frame).pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        self.criar_grafico_top_solicitantes(graficos_frame).pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 0))
    
    def criar_kpi_card(self, parent, titulo, valor, cor):
        card = tk.Frame(parent, bg=cor, relief=tk.RAISED, borderwidth=3)
        
        tk.Label(
            card,
            text=titulo,
            font=('Quicksand', 11, 'bold'),
            bg=cor,
            fg='white'
        ).pack(pady=(15, 5))
        
        tk.Label(
            card,
            text=f"{valor:,}".replace(',', '.'),
            font=('Quicksand', 28, 'bold'),
            bg=cor,
            fg='white'
        ).pack(pady=(5, 15))
        
        return card
    
    def criar_grafico_top_setores(self, parent):
        frame = tk.Frame(parent, bg='white', relief=tk.RAISED, borderwidth=2)
        
        tk.Label(
            frame,
            text="🏢 Top 10 Setores (por número de solicitações)",
            font=('Quicksand', 12, 'bold'),
            bg='white'
        ).pack(pady=10)
        
        fig = Figure(figsize=(7, 4), dpi=100)
        ax = fig.add_subplot(111)
        
        df = self.df_filtrado
        top_setores = df['Setor'].value_counts().head(10).sort_values(ascending=True)
        
        ax.barh(range(len(top_setores)), top_setores.values, color='#27ae60')
        ax.set_yticks(range(len(top_setores)))
        ax.set_yticklabels([s[:40] + '...' if len(s) > 40 else s for s in top_setores.index], fontsize=10)
        ax.set_xlabel('Número de Solicitações', fontsize=12, fontweight='bold')
        ax.grid(True, alpha=0.3, axis='x')
        
        # Forçar valores inteiros no eixo X
        ax.xaxis.set_major_locator(plt.MaxNLocator(integer=True))
        fig.tight_layout()
        
        canvas = FigureCanvasTkAgg(fig, frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        return frame
    
    def criar_grafico_top_solicitantes(self, parent):
        frame = tk.Frame(parent, bg='white', relief=tk.RAISED, borderwidth=2)
        
        tk.Label(
            frame,
            text="👥 Top 10 Solicitantes",
            font=('Quicksand', 12, 'bold'),
            bg='white'
        ).pack(pady=10)
        
        fig = Figure(figsize=(7, 4), dpi=100)
        ax = fig.add_subplot(111)
        
        df = self.df_filtrado
        top_solicitantes = df['Solicitante'].value_counts().head(10).sort_values(ascending=True)
        
        ax.barh(range(len(top_solicitantes)), top_solicitantes.values, color='#9b59b6')
        ax.set_yticks(range(len(top_solicitantes)))
        ax.set_yticklabels(top_solicitantes.index, fontsize=10)
        ax.set_xlabel('Número de Solicitações', fontsize=12, fontweight='bold')
        ax.grid(True, alpha=0.3, axis='x')
        
        # Forçar valores inteiros no eixo X
        ax.xaxis.set_major_locator(plt.MaxNLocator(integer=True))
        fig.tight_layout()
        
        canvas = FigureCanvasTkAgg(fig, frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        return frame
    
    # ==================== ATUALIZAR ANÁLISE ====================
    def atualizar_analise(self):
        for widget in self.analise_frame.winfo_children():
            widget.destroy()
        
        if self.df_filtrado is None or self.df_filtrado.empty:
            tk.Label(
                self.analise_frame,
                text="📈 Nenhum dado para exibir",
                font=('Quicksand', 14),
                bg='#f4ecf7',
                fg='#7f8c8d'
            ).pack(pady=50)
            return
        
        df = self.df_filtrado
        
        # Título
        tk.Label(
            self.analise_frame,
            text="📊 Análise Detalhada",
            font=('Quicksand', 18, 'bold'),
            bg='#f4ecf7',
            fg='#2c3e50'
        ).pack(pady=20)
        
        # Apenas 1 gráfico: Distribuição por Dia da Semana
        graficos_frame = tk.Frame(self.analise_frame, bg='#f4ecf7')
        graficos_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        self.criar_grafico_dias_semana(graficos_frame).pack(fill=tk.BOTH, expand=True)
    
    def criar_grafico_dias_semana(self, parent):
        frame = tk.Frame(parent, bg='white', relief=tk.RAISED, borderwidth=2)
        
        tk.Label(
            frame,
            text="📅 Distribuição por Dia da Semana",
            font=('Quicksand', 12, 'bold'),
            bg='white'
        ).pack(pady=10)
        
        fig = Figure(figsize=(12, 4), dpi=100)
        ax = fig.add_subplot(111)
        
        # Usa cópia local para não mutar self.df_filtrado com a coluna auxiliar
        df = self.df_filtrado.copy()
        df['Dia Semana'] = df['Data Emissao'].dt.day_name()
        dias_ordem = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        dias_pt = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo']
        
        # Contar SAs únicas por dia da semana (não itens)
        valores = []
        for dia in dias_ordem:
            sas_unicas = df[df['Dia Semana'] == dia]['Numero SA'].nunique()
            valores.append(sas_unicas)
        
        colors = ['#3498db', '#27ae60', '#e67e22', '#9b59b6', '#e74c3c', '#1abc9c', '#f39c12']
        ax.bar(dias_pt, valores, color=colors, width=0.6)
        ax.set_ylabel('Número de Solicitações', fontsize=14, fontweight='bold')
        ax.set_xlabel('Dia da Semana', fontsize=14, fontweight='bold')
        ax.tick_params(axis='both', labelsize=12)
        ax.grid(True, alpha=0.3, axis='y')
        fig.tight_layout()
        
        canvas = FigureCanvasTkAgg(fig, frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        return frame
    
    # ==================== ATUALIZAR RESUMO ====================
    def atualizar_resumo(self):
        self.resumo_text.config(state=tk.NORMAL)
        self.resumo_text.delete('1.0', tk.END)
        
        if self.df_filtrado is None or self.df_filtrado.empty:
            self.resumo_text.insert('1.0', "📄 Nenhum dado para exibir")
            self.resumo_text.config(state=tk.DISABLED)
            return
        
        df = self.df_filtrado
        
        # Calcular período e dias úteis
        if self.filtro_data_inicio and self.filtro_data_fim:
            # Se há filtro ativo, usar as datas do filtro
            data_inicio_str = self.filtro_data_inicio.strftime('%d/%m/%Y')
            data_fim_str = self.filtro_data_fim.strftime('%d/%m/%Y')
            
            # Calcular dias úteis (segunda a sexta)
            from datetime import timedelta
            dias_uteis = 0
            data_atual = self.filtro_data_inicio.date()
            data_fim_date = self.filtro_data_fim.date()
            
            while data_atual <= data_fim_date:
                # 0 = segunda, 6 = domingo
                if data_atual.weekday() < 5:  # Segunda a sexta
                    dias_uteis += 1
                data_atual += timedelta(days=1)
        else:
            # Sem filtro, usar min/max dos dados
            data_inicio_str = df['Data Emissao'].min().strftime('%d/%m/%Y')
            data_fim_str = df['Data Emissao'].max().strftime('%d/%m/%Y')
            
            # Calcular dias úteis baseado nas datas únicas nos dados
            from datetime import timedelta
            dias_uteis = 0
            data_min = df['Data Emissao'].min().date()
            data_max = df['Data Emissao'].max().date()
            data_atual = data_min
            
            while data_atual <= data_max:
                if data_atual.weekday() < 5:  # Segunda a sexta
                    dias_uteis += 1
                data_atual += timedelta(days=1)
        
        # Gerar resumo
        resumo = f"""
{'='*80}
                    RESUMO EXECUTIVO - SOLICITAÇÕES AO ARMAZÉM
{'='*80}

📅 PERÍODO ANALISADO
{'─'*80}
Data Início: {data_inicio_str}
Data Fim:    {data_fim_str}
Dias úteis:  {dias_uteis} dias

📊 ESTATÍSTICAS GERAIS
{'─'*80}
Total de Solicitações:        {df['Numero SA'].nunique():,}
Total de Itens Solicitados:   {len(df):,}
Setores Ativos:               {df['Setor'].nunique():,}
Solicitantes:                 {df['Solicitante'].nunique():,}

🏆 TOP 5 SETORES (por número de itens)
{'─'*80}
"""
        top_setores = df['Setor'].value_counts().head(5)
        for i, (setor, qtd) in enumerate(top_setores.items(), 1):
            resumo += f"{i}. {setor[:50]:<50} {qtd:>10,} itens\n"
        
        resumo += f"""
👥 TOP 5 SOLICITANTES (por número de solicitações)
{'─'*80}
"""
        top_solicitantes = df['Solicitante'].value_counts().head(5)
        for i, (solicitante, qtd) in enumerate(top_solicitantes.items(), 1):
            resumo += f"{i}. {solicitante:<50} {qtd:>10,} solicitações\n"
        
        resumo += f"""
🎯 TOP 10 MATERIAIS MAIS SOLICITADOS
{'─'*80}
"""
        top_materiais = df['Descricao'].value_counts().head(10)
        for i, (material, qtd) in enumerate(top_materiais.items(), 1):
            resumo += f"{i:>2}. {material[:60]:<60} {qtd:>8,}\n"
        
        resumo += f"""
📄 LISTA DE SAs ÚNICAS (sem repetição)
{'─'*80}
Total de SAs: {df['Numero SA'].nunique()}

"""
        sas_unicas = sorted(df['Numero SA'].unique())
        for i, sa in enumerate(sas_unicas, 1):
            resumo += f"{sa}  "
            if i % 10 == 0:
                resumo += "\n"
        
        resumo += f"""

{'='*80}
Relatório gerado em: {datetime.now().strftime('%d/%m/%Y às %H:%M:%S')}
DBSolutions Lab - © 2026
{'='*80}
"""
        
        self.resumo_text.insert('1.0', resumo)
        self.resumo_text.config(state=tk.DISABLED)
    
    # ==================== BUSCA RÁPIDA ====================
    def filtrar_tabela_busca(self):
        """Filtrar tabela em tempo real baseado na busca"""
        if self.df_filtrado is None or self.df_filtrado.empty:
            return
        
        termo_busca = self.search_var.get().strip().lower()
        
        if not termo_busca:
            # Se busca vazia, mostrar todos os dados filtrados
            self.atualizar_tabela(self.df_filtrado)
            return
        
        # Filtrar por Descrição, Setor, Solicitante ou Código
        df_busca = self.df_filtrado[
            self.df_filtrado['Descricao'].str.lower().str.contains(termo_busca, na=False) |
            self.df_filtrado['Setor'].str.lower().str.contains(termo_busca, na=False) |
            self.df_filtrado['Solicitante'].str.lower().str.contains(termo_busca, na=False) |
            self.df_filtrado['Codigo'].astype(str).str.lower().str.contains(termo_busca, na=False)
        ]
        
        self.atualizar_tabela(df_busca)
    
    # ==================== ABA STATUS DE ATENDIMENTO - FUNÇÕES ====================
    def atualizar_tabela_status(self, df):
        """Atualizar tabela da aba Status de Atendimento"""
        self.status_tree.delete(*self.status_tree.get_children())
        
        if df is None or df.empty:
            self.status_info_label.config(text="📊 Nenhum dado para exibir")
            self.kpi_atendidas.config(text="")
            self.kpi_parciais.config(text="")
            self.kpi_nao_atendidas.config(text="")
            return
        
        # Configurar colunas
        colunas = list(df.columns)
        self.status_tree['columns'] = colunas
        self.status_tree['show'] = 'headings'
        
        # Configurar larguras e cabeçalhos
        larguras = {
            'Numero SA': 90,
            'Codigo': 90,
            'Descricao': 350,
            'Unidade de Medida': 50,
            'Armazem': 100,
            'Quantidade Solicitada': 90,
            'Qtd. Atendida': 90,
            'Atendimento': 180,
            'Data Emissao': 90,
            'Dt. Atendido': 90,
            'Setor': 250,
            'Solicitante': 150,
            'Custo Unitario': 100,
            'Custo Total': 100
        }
        
        for col in colunas:
            width = larguras.get(col, 120)
            self.status_tree.column(col, width=width, anchor='w')
            
            # Cabeçalhos customizados
            if col == 'Unidade de Medida':
                self.status_tree.heading(col, text='U.M.')
            elif col == 'Data Emissao':
                self.status_tree.heading(col, text='Dt.Emissão')
            elif col == 'Quantidade Solicitada':
                self.status_tree.heading(col, text='Qtd.Solicitada')
            else:
                self.status_tree.heading(col, text=col)
        
        # Inserir dados
        for idx, row in df.iterrows():
            valores = []
            for col in colunas:
                valor = row[col]
                if pd.isna(valor):
                    valores.append('')
                elif col in ['Data Emissao', 'Dt. Atendido'] and isinstance(valor, pd.Timestamp):
                    valores.append(valor.strftime('%d/%m/%Y'))
                elif col in ['Quantidade Solicitada', 'Qtd. Atendida']:
                    if valor == int(valor):
                        valores.append(str(int(valor)))
                    else:
                        valores.append(str(valor))
                elif col in ['Custo Unitario', 'Custo Total']:
                    valores.append(f"R$ {valor:,.2f}" if not pd.isna(valor) else '')
                else:
                    valores.append(str(valor))
            
            self.status_tree.insert('', tk.END, values=valores)
        
        # Atualizar KPIs
        total = len(df)
        atendidas = len(df[df['Atendimento'] == 'TOTALMENTE ATENDIDA'])
        parciais = len(df[df['Atendimento'] == 'PARCIALMENTE ATENDIDA'])
        nao_atendidas = len(df[df['Atendimento'] == 'NÃO ATENDIDA'])
        
        perc_atendidas = (atendidas / total * 100) if total > 0 else 0
        perc_parciais = (parciais / total * 100) if total > 0 else 0
        perc_nao_atendidas = (nao_atendidas / total * 100) if total > 0 else 0
        
        self.status_info_label.config(
            text=f"📊 Exibindo {df['Numero SA'].nunique()} solicitações | {total} itens",
            fg='#27ae60'
        )
        
        self.kpi_atendidas.config(text=f"✅ Atendidas: {atendidas} ({perc_atendidas:.1f}%)")
        self.kpi_parciais.config(text=f"⚠️ Parciais: {parciais} ({perc_parciais:.1f}%)")
        self.kpi_nao_atendidas.config(text=f"❌ Não Atendidas: {nao_atendidas} ({perc_nao_atendidas:.1f}%)")
    
    def aplicar_filtro_atendimento(self):
        """Filtrar por status de atendimento"""
        if not hasattr(self, 'df_status_filtrado') or self.df_status_filtrado is None:
            return
        
        filtro = self.filtro_atendimento_var.get()
        
        if filtro == "Todas":
            df_filtrado = self.df_status_filtrado.copy()
        else:
            df_filtrado = self.df_status_filtrado[self.df_status_filtrado['Atendimento'] == filtro]
        
        self.atualizar_tabela_status(df_filtrado)
    
    def filtrar_status_busca(self):
        """Filtrar tabela de status em tempo real baseado na busca"""
        if not hasattr(self, 'df_status_filtrado') or self.df_status_filtrado is None or self.df_status_filtrado.empty:
            return
        
        termo_busca = self.status_search_var.get().strip().lower()
        
        # Aplicar filtro de status de atendimento primeiro
        filtro = self.filtro_atendimento_var.get()
        if filtro == "Todas":
            df_base = self.df_status_filtrado.copy()
        else:
            df_base = self.df_status_filtrado[self.df_status_filtrado['Atendimento'] == filtro]
        
        if not termo_busca:
            self.atualizar_tabela_status(df_base)
            return
        
        # Filtrar por Descrição, Setor, Solicitante ou Código
        df_busca = df_base[
            df_base['Descricao'].str.lower().str.contains(termo_busca, na=False) |
            df_base['Setor'].str.lower().str.contains(termo_busca, na=False) |
            df_base['Solicitante'].str.lower().str.contains(termo_busca, na=False) |
            df_base['Codigo'].astype(str).str.lower().str.contains(termo_busca, na=False)
        ]
        
        self.atualizar_tabela_status(df_busca)
    
    def exportar_status_excel(self):
        """Exportar dados da aba Status de Atendimento para Excel"""
        if not hasattr(self, 'df_status_filtrado') or self.df_status_filtrado is None or self.df_status_filtrado.empty:
            Toast.show(
                self.root,
                "Não há dados para exportar",
                tipo='warning',
                duration=3000
            )
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
            initialfile="status_atendimento.xlsx"
        )
        
        if filename:
            try:
                self.df_status_filtrado.to_excel(filename, index=False, sheet_name='Status Atendimento')
                Toast.show(
                    self.root,
                    "Dados exportados com sucesso!",
                    tipo='success',
                    duration=3000
                )
            except PermissionError:
                Toast.show(
                    self.root,
                    "Feche o arquivo Excel e tente novamente",
                    tipo='warning',
                    duration=4000
                )
            except Exception as e:
                Toast.show(
                    self.root,
                    f"Erro ao exportar: {str(e)[:80]}",
                    tipo='error',
                    duration=4000
                )
                print(f"Erro detalhado na exportação: {e}")
    
    # ==================== EXPORTAÇÕES ====================
    def exportar_excel(self):
        if self.df_filtrado is None or self.df_filtrado.empty:
            Toast.show(
                self.root,
                "Não há dados para exportar",
                tipo='warning',
                duration=3000
            )
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
            initialfile="solicitacoes_filtradas.xlsx"
        )
        
        if filename:
            try:
                df_export = self.df_filtrado.copy()
                df_export['Data Emissao'] = df_export['Data Emissao'].dt.strftime('%d/%m/%Y')
                
                df_export.to_excel(filename, index=False, sheet_name='Solicitações')
                
                Toast.show(
                    self.root,
                    f"Excel exportado! {len(df_export)} registros salvos",
                    tipo='success',
                    duration=3000
                )
            except PermissionError:
                Toast.show(
                    self.root,
                    "Feche o arquivo Excel e tente novamente",
                    tipo='warning',
                    duration=4000
                )
            except Exception as e:
                Toast.show(
                    self.root,
                    f"Erro ao exportar: {str(e)[:80]}",
                    tipo='error',
                    duration=4000
                )
                print(f"Erro detalhado na exportação: {e}")
    
    def gerar_hash_arquivo(self, filepath):
        """Gera hash MD5 do arquivo para detectar mudanças"""
        try:
            hash_md5 = hashlib.md5()
            with open(filepath, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
            return hash_md5.hexdigest()
        except Exception as e:
            print(f"Erro ao gerar hash: {e}")
            return None
    
    def obter_cache_path(self, arquivo):
        """Retorna o caminho do arquivo de cache"""
        arquivo_hash = hashlib.md5(arquivo.encode()).hexdigest()
        return os.path.join(self.cache_dir, f"{arquivo_hash}.pkl")
    
    def carregar_do_cache(self, arquivo):
        """Tenta carregar dados do cache"""
        try:
            cache_path = self.obter_cache_path(arquivo)
            
            if not os.path.exists(cache_path):
                return None
            
            # Verificar se o arquivo original foi modificado
            arquivo_hash = self.gerar_hash_arquivo(arquivo)
            
            with open(cache_path, 'rb') as f:
                cache_data = pickle.load(f)
            
            # Verificar se o hash corresponde
            if cache_data.get('hash') == arquivo_hash:
                print(f"✅ Cache encontrado e válido para {arquivo}")
                return cache_data.get('data')
            else:
                print(f"⚠️ Cache inválido (arquivo modificado)")
                return None
                
        except Exception as e:
            print(f"Erro ao carregar cache: {e}")
            return None
    
    def salvar_no_cache(self, arquivo, data):
        """Salva dados no cache"""
        try:
            cache_path = self.obter_cache_path(arquivo)
            arquivo_hash = self.gerar_hash_arquivo(arquivo)
            
            cache_data = {
                'hash': arquivo_hash,
                'data': data,
                'timestamp': datetime.now().isoformat()
            }
            
            with open(cache_path, 'wb') as f:
                pickle.dump(cache_data, f)
            
            print(f"💾 Cache salvo para {arquivo}")
            return True
            
        except Exception as e:
            print(f"Erro ao salvar cache: {e}")
            return False
    
    def limpar_cache(self):
        """Remove todos os arquivos de cache"""
        try:
            if os.path.exists(self.cache_dir):
                for arquivo in os.listdir(self.cache_dir):
                    os.remove(os.path.join(self.cache_dir, arquivo))
                print("🗑️ Cache limpo")
                return True
        except Exception as e:
            print(f"Erro ao limpar cache: {e}")
            return False
    
    def carregar_config(self):
        """Carrega configurações do arquivo JSON"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Erro ao carregar config: {e}")
        
        # Configuração padrão
        return {
            'ultimo_arquivo': 'simecr05.xlsx',
            'tema': 'light',
            'versao': '1.0.0'
        }
    
    def salvar_config(self):
        """Salva configurações no arquivo JSON"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Erro ao salvar config: {e}")
    
    def exportar_resumo(self):
        if self.df_filtrado is None or self.df_filtrado.empty:
            Toast.show(
                self.root,
                "Não há dados para exportar",
                tipo='warning',
                duration=3000
            )
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            initialfile="resumo_executivo.txt"
        )
        
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(self.resumo_text.get('1.0', tk.END))
                
                Toast.show(
                    self.root,
                    "Resumo exportado com sucesso!",
                    tipo='success',
                    duration=3000
                )
            except PermissionError:
                Toast.show(
                    self.root,
                    "Feche o arquivo Excel e tente novamente",
                    tipo='warning',
                    duration=4000
                )
            except Exception as e:
                Toast.show(
                    self.root,
                    f"Erro ao exportar: {str(e)[:80]}",
                    tipo='error',
                    duration=4000
                )
                print(f"Erro detalhado na exportação: {e}")

    # ==================== EXPORTAR PDF ====================
    def exportar_pdf(self):
        if self.df_filtrado is None or self.df_filtrado.empty:
            Toast.show(self.root, "Não há dados para exportar", tipo='warning', duration=3000)
            return

        try:
            from fpdf import FPDF
        except ImportError:
            Toast.show(
                self.root,
                "Dependência ausente. Execute: pip install fpdf2",
                tipo='error',
                duration=6000
            )
            return

        filename = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")],
            initialfile="relatorio_zeus.pdf"
        )
        if not filename:
            return

        import tempfile
        temp_files = []
        try:
            df = self.df_filtrado

            # Período
            if self.filtro_data_inicio and self.filtro_data_fim:
                data_inicio_str = self.filtro_data_inicio.strftime('%d/%m/%Y')
                data_fim_str    = self.filtro_data_fim.strftime('%d/%m/%Y')
            else:
                data_inicio_str = df['Data Emissao'].min().strftime('%d/%m/%Y')
                data_fim_str    = df['Data Emissao'].max().strftime('%d/%m/%Y')

            # KPIs
            total_sas     = df['Numero SA'].nunique()
            total_itens   = len(df)
            total_setores = df['Setor'].nunique()
            total_solicit = df['Solicitante'].nunique()

            top_setores      = df['Setor'].value_counts().head(5)
            top_solicitantes = df['Solicitante'].value_counts().head(5)
            top_materiais    = df['Descricao'].value_counts().head(10)

            # Gráficos como PNG temporários
            temp_files = self._gerar_figuras_pdf()

            # Fontes (funciona em dev e no executável PyInstaller)
            if hasattr(sys, '_MEIPASS'):
                font_base = os.path.join(sys._MEIPASS, 'assets', 'fonts')
            else:
                font_base = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets', 'fonts')

            font_regular = os.path.join(font_base, 'Quicksand-Regular.ttf')
            font_bold    = os.path.join(font_base, 'Quicksand-Bold.ttf')

            pdf = FPDF()
            pdf.set_auto_page_break(auto=True, margin=15)
            pdf.add_font("Quicksand", style="",  fname=font_regular)
            pdf.add_font("Quicksand", style="B", fname=font_bold)

            MARGEM  = 15
            LARGURA = 210 - 2 * MARGEM  # 180mm

            # ===== PÁGINA 1: RESUMO EXECUTIVO =====
            pdf.add_page()

            # Cabeçalho azul Zeus
            pdf.set_fill_color(52, 152, 219)
            pdf.rect(0, 0, 210, 30, 'F')
            pdf.set_xy(MARGEM, 7)
            pdf.set_text_color(255, 215, 0)
            pdf.set_font("Quicksand", "B", 17)
            pdf.cell(0, 9, "ZEUS - Sistema de Controle de Solicitacoes", ln=True)
            pdf.set_xy(MARGEM, 19)
            pdf.set_text_color(210, 230, 250)
            pdf.set_font("Quicksand", "", 9)
            pdf.cell(0, 6, "DBSolutions Lab  |  Relatorio Executivo", ln=True)

            pdf.set_y(37)
            pdf.set_text_color(44, 62, 80)

            # Período e timestamp
            pdf.set_font("Quicksand", "B", 11)
            pdf.cell(LARGURA, 7, f"Periodo: {data_inicio_str}  -  {data_fim_str}", ln=True)
            pdf.set_font("Quicksand", "", 9)
            pdf.cell(LARGURA, 5, f"Gerado em: {datetime.now().strftime('%d/%m/%Y as %H:%M')}", ln=True)
            pdf.ln(5)

            # Linha divisória
            pdf.set_draw_color(52, 152, 219)
            pdf.set_line_width(0.5)
            pdf.line(MARGEM, pdf.get_y(), MARGEM + LARGURA, pdf.get_y())
            pdf.ln(6)

            # KPI boxes coloridos
            pdf.set_font("Quicksand", "B", 11)
            pdf.set_text_color(44, 62, 80)
            pdf.cell(LARGURA, 6, "ESTATISTICAS GERAIS", ln=True)
            pdf.ln(3)

            box_w      = (LARGURA - 6) / 4
            box_y      = pdf.get_y()
            kpi_labels = ["Total de SAs", "Total de Itens", "Setores Ativos", "Solicitantes"]
            kpi_values = [f"{total_sas:,}", f"{total_itens:,}", f"{total_setores:,}", f"{total_solicit:,}"]
            kpi_cores  = [(52, 152, 219), (46, 204, 113), (155, 89, 182), (230, 126, 34)]

            for i, (label, value, cor) in enumerate(zip(kpi_labels, kpi_values, kpi_cores)):
                x = MARGEM + i * (box_w + 2)
                pdf.set_fill_color(*cor)
                pdf.rect(x, box_y, box_w, 20, 'F')
                pdf.set_xy(x, box_y + 3)
                pdf.set_text_color(255, 255, 255)
                pdf.set_font("Quicksand", "B", 14)
                pdf.cell(box_w, 8, value, align='C')
                pdf.set_xy(x, box_y + 13)
                pdf.set_font("Quicksand", "", 7)
                pdf.cell(box_w, 5, label, align='C')

            pdf.set_y(box_y + 26)
            pdf.set_text_color(44, 62, 80)
            pdf.line(MARGEM, pdf.get_y(), MARGEM + LARGURA, pdf.get_y())
            pdf.ln(6)

            # TOP 5 SETORES
            pdf.set_font("Quicksand", "B", 11)
            pdf.cell(LARGURA, 6, "TOP 5 SETORES (por numero de itens)", ln=True)
            pdf.ln(2)

            for i, (setor, qtd) in enumerate(top_setores.items(), 1):
                pdf.set_fill_color(245, 245, 245) if i % 2 == 0 else pdf.set_fill_color(255, 255, 255)
                setor_trunc = setor[:62] + "..." if len(setor) > 62 else setor
                pdf.set_font("Quicksand", "", 10)
                pdf.cell(8,   7, f"{i}.", fill=True)
                pdf.cell(148, 7, setor_trunc, fill=True)
                pdf.set_font("Quicksand", "B", 10)
                pdf.cell(0,   7, f"{qtd:,}", align='R', fill=True, ln=True)

            pdf.ln(5)

            # TOP 5 SOLICITANTES
            pdf.set_font("Quicksand", "B", 11)
            pdf.cell(LARGURA, 6, "TOP 5 SOLICITANTES", ln=True)
            pdf.ln(2)

            for i, (nome, qtd) in enumerate(top_solicitantes.items(), 1):
                pdf.set_fill_color(245, 245, 245) if i % 2 == 0 else pdf.set_fill_color(255, 255, 255)
                pdf.set_font("Quicksand", "", 10)
                pdf.cell(8,   7, f"{i}.", fill=True)
                pdf.cell(148, 7, nome[:62], fill=True)
                pdf.set_font("Quicksand", "B", 10)
                pdf.cell(0,   7, f"{qtd:,}", align='R', fill=True, ln=True)

            pdf.ln(5)

            # TOP 10 MATERIAIS
            pdf.set_font("Quicksand", "B", 11)
            pdf.cell(LARGURA, 6, "TOP 10 MATERIAIS MAIS SOLICITADOS", ln=True)
            pdf.ln(2)

            for i, (material, qtd) in enumerate(top_materiais.items(), 1):
                pdf.set_fill_color(245, 245, 245) if i % 2 == 0 else pdf.set_fill_color(255, 255, 255)
                mat_trunc = material[:72] + "..." if len(material) > 72 else material
                pdf.set_font("Quicksand", "", 9)
                pdf.cell(10,  6, f"{i:>2}.", fill=True)
                pdf.cell(146, 6, mat_trunc, fill=True)
                pdf.set_font("Quicksand", "B", 9)
                pdf.cell(0,   6, f"{qtd:,}", align='R', fill=True, ln=True)

            self._pdf_rodape(pdf, MARGEM, LARGURA)

            # ===== PÁGINAS DE GRÁFICOS =====
            for titulo, img_path in temp_files:
                pdf.add_page()

                # Mini cabeçalho azul
                pdf.set_fill_color(52, 152, 219)
                pdf.rect(0, 0, 210, 14, 'F')
                pdf.set_xy(MARGEM, 4)
                pdf.set_text_color(255, 215, 0)
                pdf.set_font("Quicksand", "B", 11)
                pdf.cell(0, 6, "ZEUS - Graficos Analiticos", ln=True)

                pdf.set_y(21)
                pdf.set_text_color(44, 62, 80)
                pdf.set_font("Quicksand", "B", 12)
                pdf.cell(LARGURA, 7, titulo, ln=True)
                pdf.ln(4)

                pdf.image(img_path, x=MARGEM, w=LARGURA)

                self._pdf_rodape(pdf, MARGEM, LARGURA)

            pdf.output(filename)
            Toast.show(self.root, "PDF exportado com sucesso!", tipo='success', duration=3000)

        except Exception as e:
            Toast.show(self.root, f"Erro ao gerar PDF: {str(e)[:80]}", tipo='error', duration=4000)
            print(f"Erro detalhado PDF: {e}")
        finally:
            for _, path in temp_files:
                try:
                    os.remove(path)
                except Exception:
                    pass

    def _pdf_rodape(self, pdf, margem, largura):
        """Adiciona rodapé com timestamp e número de página."""
        pdf.set_y(-12)
        pdf.set_draw_color(200, 200, 200)
        pdf.set_line_width(0.3)
        pdf.line(margem, pdf.get_y(), margem + largura, pdf.get_y())
        pdf.ln(1)
        pdf.set_font("Quicksand", "", 7)
        pdf.set_text_color(150, 150, 150)
        pdf.cell(
            largura, 5,
            f"Zeus  |  DBSolutions Lab  |  {datetime.now().strftime('%d/%m/%Y as %H:%M')}  |  Pag. {pdf.page_no()}",
            align='C'
        )

    def _gerar_figuras_pdf(self):
        """Gera figuras matplotlib como PNG temporários para o PDF. Retorna lista de (titulo, path)."""
        import tempfile
        df = self.df_filtrado
        figuras = []

        # Top 10 Setores
        dados = df['Setor'].value_counts().head(10).sort_values(ascending=True)
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.barh(range(len(dados)), dados.values, color='#27ae60')
        ax.set_yticks(range(len(dados)))
        ax.set_yticklabels([s[:40] + '...' if len(s) > 40 else s for s in dados.index], fontsize=9)
        ax.set_xlabel('Numero de Itens', fontsize=11)
        ax.grid(True, alpha=0.3, axis='x')
        ax.xaxis.set_major_locator(plt.MaxNLocator(integer=True))
        fig.tight_layout()
        tmp = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
        fig.savefig(tmp.name, dpi=150, bbox_inches='tight')
        plt.close(fig)
        tmp.close()
        figuras.append(("Top 10 Setores por Numero de Itens", tmp.name))

        # Top 10 Solicitantes
        dados = df['Solicitante'].value_counts().head(10).sort_values(ascending=True)
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.barh(range(len(dados)), dados.values, color='#9b59b6')
        ax.set_yticks(range(len(dados)))
        ax.set_yticklabels(dados.index, fontsize=9)
        ax.set_xlabel('Numero de Solicitacoes', fontsize=11)
        ax.grid(True, alpha=0.3, axis='x')
        ax.xaxis.set_major_locator(plt.MaxNLocator(integer=True))
        fig.tight_layout()
        tmp = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
        fig.savefig(tmp.name, dpi=150, bbox_inches='tight')
        plt.close(fig)
        tmp.close()
        figuras.append(("Top 10 Solicitantes", tmp.name))

        # Distribuição por dia da semana
        dias_map  = {0: 'Seg', 1: 'Ter', 2: 'Qua', 3: 'Qui', 4: 'Sex', 5: 'Sab', 6: 'Dom'}
        ordem     = ['Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sab', 'Dom']
        dias_serie = df['Data Emissao'].dt.dayofweek.map(dias_map).value_counts()
        dias_serie = dias_serie.reindex([d for d in ordem if d in dias_serie.index])
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.bar(range(len(dias_serie)), dias_serie.values, color='#3498db')
        ax.set_xticks(range(len(dias_serie)))
        ax.set_xticklabels(dias_serie.index, fontsize=10)
        ax.set_ylabel('Numero de Solicitacoes', fontsize=11)
        ax.grid(True, alpha=0.3, axis='y')
        ax.yaxis.set_major_locator(plt.MaxNLocator(integer=True))
        fig.tight_layout()
        tmp = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
        fig.savefig(tmp.name, dpi=150, bbox_inches='tight')
        plt.close(fig)
        tmp.close()
        figuras.append(("Distribuicao por Dia da Semana", tmp.name))

        return figuras

if __name__ == "__main__":
    _registrar_fontes()
    
    # Configurar tema do CustomTkinter
    ctk.set_appearance_mode("light")  # Modo claro fixo
    ctk.set_default_color_theme("blue")  # Tema azul
    
    root = ctk.CTk()  # Usar CTk ao invés de tk.Tk()
    app = SolicitacoesAppPro(root)
    try:
        root.mainloop()
    except KeyboardInterrupt:
        pass
