import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
import pandas as pd
from tkcalendar import DateEntry
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import ctypes
import os
import sys


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
        
        self.criar_interface()
        
    def criar_interface(self):
        # Frame principal
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # ========== CABEÇALHO ==========
        header_frame = tk.Frame(main_frame, bg='#2c3e50', height=60)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        header_frame.pack_propagate(False)
        
        # Container centralizado para título e subtítulo lado a lado
        header_content = tk.Frame(header_frame, bg='#2c3e50')
        header_content.place(relx=0.5, rely=0.5, anchor='center')
        
        # Título principal
        title_label = tk.Label(
            header_content,
            text="⚡ Zeus",
            font=('Quicksand', 24, 'bold'),
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
            font=('Quicksand', 12, 'bold'),
            bg='#2c3e50',
            fg='#ecf0f1'  # Branco suave
        )
        subtitle_label.pack(side=tk.LEFT)
        
        # ========== PAINEL DE CONTROLE ==========
        control_frame = tk.Frame(main_frame, bg='white', relief=tk.RAISED, borderwidth=2)
        control_frame.pack(fill=tk.X, pady=(0, 10), padx=5)
        
        # Linha 1: Arquivo
        file_frame = tk.Frame(control_frame, bg='white')
        file_frame.pack(fill=tk.X, padx=15, pady=10)
        
        tk.Label(
            file_frame,
            text="📂 Arquivo:",
            font=('Quicksand', 10, 'bold'),
            bg='white'
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        self.arquivo_entry = tk.Entry(file_frame, font=('Quicksand', 10), width=50)
        self.arquivo_entry.insert(0, 'simecr05.xlsx')
        self.arquivo_entry.pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Button(
            file_frame,
            text="Procurar...",
            command=self.selecionar_arquivo,
            bg='#3498db',
            fg='white',
            font=('Quicksand', 9, 'bold'),
            cursor='hand2',
            relief=tk.FLAT,
            padx=15
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Button(
            file_frame,
            text="🔄 Carregar Dados",
            command=self.carregar_dados,
            bg='#27ae60',
            fg='white',
            font=('Quicksand', 10, 'bold'),
            cursor='hand2',
            relief=tk.FLAT,
            padx=20,
            pady=5
        ).pack(side=tk.LEFT)
        
        # Linha 2: Filtros de Data
        filter_frame = tk.Frame(control_frame, bg='white')
        filter_frame.pack(fill=tk.X, padx=15, pady=(0, 10))
        
        tk.Label(
            filter_frame,
            text="📅 Filtrar por Data de Emissão:",
            font=('Quicksand', 10, 'bold'),
            bg='white'
        ).pack(side=tk.LEFT, padx=(0, 20))
        
        tk.Label(filter_frame, text="De:", font=('Quicksand', 9), bg='white').pack(side=tk.LEFT, padx=(0, 5))
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
        
        tk.Label(filter_frame, text="Até:", font=('Quicksand', 9), bg='white').pack(side=tk.LEFT, padx=(0, 5))
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
        
        tk.Button(
            filter_frame,
            text="🔍 Aplicar Filtro",
            command=self.aplicar_filtro_data,
            bg='#e67e22',
            fg='white',
            font=('Quicksand', 9, 'bold'),
            cursor='hand2',
            relief=tk.FLAT,
            padx=15
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Button(
            filter_frame,
            text="🔄 Limpar Filtro",
            command=self.limpar_filtro,
            bg='#95a5a6',
            fg='white',
            font=('Quicksand', 9, 'bold'),
            cursor='hand2',
            relief=tk.FLAT,
            padx=15
        ).pack(side=tk.LEFT)
        
        # ========== SISTEMA DE ABAS ==========
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Estilo das abas
        style = ttk.Style()
        style.configure('TNotebook.Tab', font=('Quicksand', 10, 'bold'), padding=[20, 10])
        
        # Criar abas
        self.criar_aba_dados()
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
        self.aba_dados = tk.Frame(self.notebook, bg='white')
        self.notebook.add(self.aba_dados, text='📋 Dados')
        
        # Info e exportação
        info_frame = tk.Frame(self.aba_dados, bg='white', relief=tk.RAISED, borderwidth=2)
        info_frame.pack(fill=tk.X, pady=(10, 10), padx=10)
        
        self.info_label = tk.Label(
            info_frame,
            text="📊 Nenhum dado carregado",
            font=('Quicksand', 10),
            bg='white',
            fg='#7f8c8d',
            anchor='w'
        )
        self.info_label.pack(side=tk.LEFT, padx=15, pady=8)
        
        tk.Button(
            info_frame,
            text="💾 Exportar para Excel",
            command=self.exportar_excel,
            bg='#16a085',
            fg='white',
            font=('Quicksand', 9, 'bold'),
            cursor='hand2',
            relief=tk.FLAT,
            padx=15
        ).pack(side=tk.RIGHT, padx=15, pady=5)
        
        # Título centralizado
        title_frame = tk.Frame(self.aba_dados, bg='#2c3e50', height=50)
        title_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        title_frame.pack_propagate(False)
        
        tk.Label(
            title_frame,
            text="⚡ Solicitações Pendentes",
            font=('Quicksand', 16, 'bold'),
            bg='#2c3e50',
            fg='#FFD700'
        ).pack(expand=True)
        
        # Tabela
        table_frame = tk.Frame(self.aba_dados, bg='white', relief=tk.RAISED, borderwidth=2)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        scroll_y = ttk.Scrollbar(table_frame, orient=tk.VERTICAL)
        scroll_x = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL)
        
        self.tree = ttk.Treeview(
            table_frame,
            yscrollcommand=scroll_y.set,
            xscrollcommand=scroll_x.set,
            selectmode='extended'
        )
        
        scroll_y.config(command=self.tree.yview)
        scroll_x.config(command=self.tree.xview)
        
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        self.tree.pack(fill=tk.BOTH, expand=True)
        
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
    
    # ==================== ABA 2: DASHBOARD ====================
    def criar_aba_dashboard(self):
        self.aba_dashboard = tk.Frame(self.notebook, bg='#ecf0f1')
        self.notebook.add(self.aba_dashboard, text='📈 Dashboard')
        
        # Container com scroll
        canvas = tk.Canvas(self.aba_dashboard, bg='#ecf0f1')
        scrollbar = ttk.Scrollbar(self.aba_dashboard, orient="vertical", command=canvas.yview)
        self.dashboard_frame = tk.Frame(canvas, bg='#ecf0f1')
        
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
            bg='#ecf0f1',
            fg='#7f8c8d'
        ).pack(pady=50)
    
    # ==================== ABA 3: ANÁLISE DETALHADA ====================
    def criar_aba_analise(self):
        self.aba_analise = tk.Frame(self.notebook, bg='#ecf0f1')
        self.notebook.add(self.aba_analise, text='📊 Análise Detalhada')
        
        # Container com scroll
        canvas = tk.Canvas(self.aba_analise, bg='#ecf0f1')
        scrollbar = ttk.Scrollbar(self.aba_analise, orient="vertical", command=canvas.yview)
        self.analise_frame = tk.Frame(canvas, bg='#ecf0f1')
        
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
            bg='#ecf0f1',
            fg='#7f8c8d'
        ).pack(pady=50)
    
    # ==================== ABA 4: RESUMO EXECUTIVO ====================
    def criar_aba_resumo(self):
        self.aba_resumo = tk.Frame(self.notebook, bg='white')
        self.notebook.add(self.aba_resumo, text='📄 Resumo Executivo')
        
        # Botão de exportar
        btn_frame = tk.Frame(self.aba_resumo, bg='white')
        btn_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Button(
            btn_frame,
            text="📄 Exportar Resumo (TXT)",
            command=self.exportar_resumo,
            bg='#9b59b6',
            fg='white',
            font=('Quicksand', 10, 'bold'),
            cursor='hand2',
            relief=tk.FLAT,
            padx=20,
            pady=8
        ).pack(side=tk.RIGHT)
        
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
            messagebox.showwarning("Aviso", "Por favor, selecione um arquivo!")
            return
        
        try:
            df = pd.read_excel(arquivo, sheet_name='Relatório de Controle de entr')
            
            grupos_excluir = [4003, 4037]
            df_filtrado = df[~df['Grupo'].isin(grupos_excluir)]
            
            # Filtrar 'EM APROVAÇÃO' e 'PRE-REQUISIÇÃO GERADA' (lógica da aba Dados)
            status_excluir = ['EM APROVAÇÃO', 'PRE-REQUISIÇÃO GERADA']
            df_filtrado = df_filtrado[~df_filtrado['Status'].isin(status_excluir)]
            
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
            
            df_filtrado = df_filtrado[list(colunas_mapeamento.keys())]
            df_filtrado = df_filtrado.rename(columns=colunas_mapeamento)
            
            df_filtrado['Data Emissao'] = pd.to_datetime(df_filtrado['Data Emissao'], errors='coerce')
            
            self.df_original = df_filtrado.copy()
            self.df_filtrado = df_filtrado.copy()
            
            self.atualizar_tabela(self.df_filtrado)
            self.atualizar_dashboard()
            self.atualizar_analise()
            self.atualizar_resumo()
            
            messagebox.showinfo(
                "Sucesso",
                f"✅ Dados carregados com sucesso!\n\n"
                f"Total original: {len(df)} linhas\n"
                f"Após filtros: {len(self.df_filtrado)} linhas"
            )
            
        except FileNotFoundError:
            messagebox.showerror("Erro", f"Arquivo '{arquivo}' não encontrado!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar dados:\n{str(e)}")
    
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
    
    def aplicar_filtro_data(self):
        if self.df_original is None:
            messagebox.showwarning("Aviso", "Carregue os dados primeiro!")
            return
        
        try:
            data_inicio = self.data_inicio.get_date()
            data_fim = self.data_fim.get_date()
            
            data_inicio_pd = pd.Timestamp(data_inicio)
            data_fim_pd = pd.Timestamp(data_fim)
            
            if data_inicio_pd > data_fim_pd:
                messagebox.showwarning("Aviso", "A data inicial não pode ser maior que a data final!")
                return
            
            df_filtrado = self.df_original[
                (self.df_original['Data Emissao'] >= data_inicio_pd) &
                (self.df_original['Data Emissao'] <= data_fim_pd)
            ]
            
            # Aplicar filtro de status (excluir 'EM APROVAÇÃO' e 'PRE-REQUISIÇÃO GERADA')
            status_excluir = ['EM APROVAÇÃO', 'PRE-REQUISIÇÃO GERADA']
            df_filtrado = df_filtrado[~df_filtrado['Status'].isin(status_excluir)]
            
            self.df_filtrado = df_filtrado.copy()
            self.atualizar_tabela(self.df_filtrado)
            self.atualizar_dashboard()
            self.atualizar_analise()
            self.atualizar_resumo()
            
            messagebox.showinfo(
                "Filtro Aplicado",
                f"✅ Filtro de data aplicado!\n\n"
                f"Período: {data_inicio.strftime('%d/%m/%Y')} até {data_fim.strftime('%d/%m/%Y')}\n"
                f"Solicitações encontradas: {df_filtrado['Numero SA'].nunique()}"
            )
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao aplicar filtro:\n{str(e)}")
    
    def limpar_filtro(self):
        if self.df_original is None:
            messagebox.showwarning("Aviso", "Carregue os dados primeiro!")
            return
        
        # Aplicar filtro de status (excluir 'EM APROVAÇÃO' e 'PRE-REQUISIÇÃO GERADA')
        status_excluir = ['EM APROVAÇÃO', 'PRE-REQUISIÇÃO GERADA']
        df_filtrado = self.df_original[~self.df_original['Status'].isin(status_excluir)]
        
        self.df_filtrado = df_filtrado.copy()
        self.atualizar_tabela(self.df_filtrado)
        self.atualizar_dashboard()
        self.atualizar_analise()
        self.atualizar_resumo()
        messagebox.showinfo("Filtro Limpo", "✅ Filtro de data removido. Exibindo todos os dados.")
    
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
                bg='#ecf0f1',
                fg='#7f8c8d'
            ).pack(pady=50)
            return
        
        df = self.df_filtrado
        
        # Título
        tk.Label(
            self.analise_frame,
            text="📊 Análise Detalhada",
            font=('Quicksand', 18, 'bold'),
            bg='#ecf0f1',
            fg='#2c3e50'
        ).pack(pady=20)
        
        # Apenas 1 gráfico: Distribuição por Dia da Semana
        graficos_frame = tk.Frame(self.analise_frame, bg='#ecf0f1')
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
        
        # Gerar resumo
        resumo = f"""
{'='*80}
                    RESUMO EXECUTIVO - SOLICITAÇÕES AO ARMAZÉM
{'='*80}

📅 PERÍODO ANALISADO
{'─'*80}
Data Início: {df['Data Emissao'].min().strftime('%d/%m/%Y')}
Data Fim:    {df['Data Emissao'].max().strftime('%d/%m/%Y')}
Dias úteis:  {df['Data Emissao'].dt.date.nunique()} dias

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
    
    # ==================== EXPORTAÇÕES ====================
    def exportar_excel(self):
        if self.df_filtrado is None or self.df_filtrado.empty:
            messagebox.showwarning("Aviso", "Não há dados para exportar!")
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
                
                messagebox.showinfo(
                    "Sucesso",
                    f"✅ Arquivo exportado com sucesso!\n\n"
                    f"Local: {filename}\n"
                    f"Registros: {len(df_export)}"
                )
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao exportar:\n{str(e)}")
    
    def exportar_resumo(self):
        if self.df_filtrado is None or self.df_filtrado.empty:
            messagebox.showwarning("Aviso", "Não há dados para exportar!")
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
                
                messagebox.showinfo(
                    "Sucesso",
                    f"✅ Resumo exportado com sucesso!\n\n"
                    f"Local: {filename}"
                )
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao exportar:\n{str(e)}")

if __name__ == "__main__":
    _registrar_fontes()
    root = tk.Tk()
    app = SolicitacoesAppPro(root)
    try:
        root.mainloop()
    except KeyboardInterrupt:
        pass
