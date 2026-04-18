# 📚 Explicação Passo a Passo - Interface Tkinter para Solicitações ao Armazém

**Desenvolvido por:** Diego Bernardes & Yahiko  
**Empresa:** DBSolutions Lab  
**Data:** Março 2026

---

## 📋 Índice

1. [Visão Geral](#visão-geral)
2. [Estrutura do Código](#estrutura-do-código)
3. [Componentes da Interface](#componentes-da-interface)
4. [Funções Principais](#funções-principais)
5. [Como Funciona o Filtro de Datas](#como-funciona-o-filtro-de-datas)
6. [Personalização](#personalização)

---

## 🎯 Visão Geral

Esta aplicação Tkinter permite:
- ✅ Carregar planilhas Excel de solicitações ao armazém
- ✅ Filtrar automaticamente grupos e status indesejados
- ✅ **Filtrar por intervalo de datas** (funcionalidade principal)
- ✅ Visualizar dados em tabela interativa
- ✅ Exportar resultados filtrados para Excel

---

## 🏗️ Estrutura do Código

### **Importações**

```python
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
import pandas as pd
from tkcalendar import DateEntry
```

**O que cada biblioteca faz:**

- `tkinter`: Biblioteca principal para criar interfaces gráficas
- `ttk`: Widgets modernos do Tkinter (Treeview, estilos)
- `messagebox`: Caixas de diálogo (alertas, confirmações)
- `filedialog`: Diálogos para abrir/salvar arquivos
- `datetime`: Manipulação de datas
- `pandas`: Análise e manipulação de dados
- `tkcalendar.DateEntry`: Widget de calendário para seleção de datas

---

## 🎨 Componentes da Interface

### **1. Classe Principal: `SolicitacoesApp`**

```python
class SolicitacoesApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Controlador de Solicitações ao Armazém - DBSolutions Lab")
        self.root.geometry("1400x800")
        self.root.configure(bg='#f0f0f0')
        
        self.df_original = None  # DataFrame completo (sem filtro de data)
        self.df_filtrado = None  # DataFrame com filtro de data aplicado
        
        self.criar_interface()
```

**Explicação:**
- `__init__`: Método construtor, executado quando criamos a aplicação
- `self.root`: Janela principal
- `geometry("1400x800")`: Define tamanho da janela (largura x altura)
- `df_original`: Guarda todos os dados carregados (após filtros de grupo/status)
- `df_filtrado`: Guarda dados após aplicar filtro de data

---

### **2. Cabeçalho**

```python
header_frame = tk.Frame(main_frame, bg='#2c3e50', height=80)
header_frame.pack(fill=tk.X, pady=(0, 10))
header_frame.pack_propagate(False)

title_label = tk.Label(
    header_frame,
    text="📋 Controlador de Solicitações ao Armazém",
    font=('Segoe UI', 20, 'bold'),
    bg='#2c3e50',
    fg='white'
)
title_label.pack(pady=20)
```

**Explicação:**
- `Frame`: Container para agrupar widgets
- `bg='#2c3e50'`: Cor de fundo (azul escuro)
- `pack()`: Gerenciador de layout que organiza widgets
- `fill=tk.X`: Preenche horizontalmente
- `pack_propagate(False)`: Mantém altura fixa de 80 pixels

---

### **3. Painel de Controle - Seleção de Arquivo**

```python
self.arquivo_entry = tk.Entry(file_frame, font=('Segoe UI', 10), width=50)
self.arquivo_entry.insert(0, 'simecr05.xlsx')
self.arquivo_entry.pack(side=tk.LEFT, padx=(0, 10))

tk.Button(
    file_frame,
    text="Procurar...",
    command=self.selecionar_arquivo,
    bg='#3498db',
    fg='white',
    font=('Segoe UI', 9, 'bold'),
    cursor='hand2',
    relief=tk.FLAT,
    padx=15
).pack(side=tk.LEFT, padx=(0, 10))
```

**Explicação:**
- `Entry`: Campo de texto para digitar o nome do arquivo
- `insert(0, 'simecr05.xlsx')`: Preenche com valor padrão
- `Button`: Botão clicável
- `command=self.selecionar_arquivo`: Função executada ao clicar
- `cursor='hand2'`: Cursor vira "mãozinha" ao passar sobre o botão
- `relief=tk.FLAT`: Botão sem borda 3D (design moderno)

---

### **4. Filtro de Datas - COMPONENTE PRINCIPAL** 🌟

```python
self.data_inicio = DateEntry(
    filter_frame,
    font=('Segoe UI', 9),
    width=12,
    background='#3498db',
    foreground='white',
    borderwidth=2,
    date_pattern='dd/mm/yyyy',
    locale='pt_BR'
)
self.data_inicio.pack(side=tk.LEFT, padx=(0, 20))
```

**Explicação:**
- `DateEntry`: Widget de calendário da biblioteca `tkcalendar`
- `date_pattern='dd/mm/yyyy'`: Formato brasileiro de data
- `locale='pt_BR'`: Calendário em português
- `get_date()`: Método para obter a data selecionada

**Por que usar DateEntry?**
- ✅ Interface visual de calendário
- ✅ Validação automática de datas
- ✅ Formato consistente
- ✅ Experiência de usuário superior

---

### **5. Tabela (Treeview)**

```python
self.tree = ttk.Treeview(
    table_frame,
    yscrollcommand=scroll_y.set,
    xscrollcommand=scroll_x.set,
    selectmode='extended'
)
```

**Explicação:**
- `Treeview`: Widget de tabela do Tkinter
- `yscrollcommand`: Conecta barra de rolagem vertical
- `selectmode='extended'`: Permite selecionar múltiplas linhas

**Configuração de colunas:**

```python
colunas = list(df.columns)
self.tree['columns'] = colunas
self.tree['show'] = 'headings'

for col in colunas:
    self.tree.heading(col, text=col)
    
    if col == 'Descricao':
        width = 300
    elif col == 'Observacao':
        width = 250
    # ...
    
    self.tree.column(col, width=width, anchor='w')
```

**Explicação:**
- `heading()`: Define o cabeçalho da coluna
- `column()`: Configura largura e alinhamento
- `anchor='w'`: Alinha texto à esquerda (west)

---

## ⚙️ Funções Principais

### **1. `selecionar_arquivo()`**

```python
def selecionar_arquivo(self):
    filename = filedialog.askopenfilename(
        title="Selecionar arquivo Excel",
        filetypes=[("Excel files", "*.xlsx *.xls"), ("All files", "*.*")]
    )
    if filename:
        self.arquivo_entry.delete(0, tk.END)
        self.arquivo_entry.insert(0, filename)
```

**O que faz:**
- Abre diálogo para selecionar arquivo
- Atualiza campo de texto com caminho completo

---

### **2. `carregar_dados()` - Função Crítica** 🔥

```python
def carregar_dados(self):
    arquivo = self.arquivo_entry.get()
    
    try:
        # 1. Carregar Excel
        df = pd.read_excel(arquivo, sheet_name='2-Relatório de Controle de en')
        
        # 2. Filtrar grupos indesejados
        grupos_excluir = [4003, 4037]
        df_filtrado = df[~df['Grupo'].isin(grupos_excluir)]
        
        # 3. Filtrar status indesejados
        status_excluir = ['EM APROVACAO', 'PRE-REQUISICAO GERADA']
        df_filtrado = df_filtrado[~df_filtrado['Status'].isin(status_excluir)]
        
        # 4. Selecionar e renomear colunas
        colunas_mapeamento = {
            'Numero SA': 'Numero SA',
            'Codigo': 'Codigo',
            'Descricao do Material': 'Descricao',
            # ... resto do mapeamento
        }
        
        df_filtrado = df_filtrado[list(colunas_mapeamento.keys())]
        df_filtrado = df_filtrado.rename(columns=colunas_mapeamento)
        
        # 5. Converter coluna de data para datetime
        df_filtrado['Data Emissao'] = pd.to_datetime(df_filtrado['Data Emissao'], errors='coerce')
        
        # 6. Guardar dados
        self.df_original = df_filtrado.copy()
        self.df_filtrado = df_filtrado.copy()
        
        # 7. Atualizar tabela
        self.atualizar_tabela(self.df_filtrado)
        
    except FileNotFoundError:
        messagebox.showerror("Erro", f"Arquivo '{arquivo}' não encontrado!")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao carregar dados:\n{str(e)}")
```

**Passo a passo:**

1. **Carregar Excel**: `pd.read_excel()` lê o arquivo
2. **Filtrar grupos**: Remove grupos 4003 e 4037
3. **Filtrar status**: Remove status indesejados
4. **Selecionar colunas**: Pega apenas colunas necessárias
5. **Converter datas**: `pd.to_datetime()` transforma texto em objeto de data
   - `errors='coerce'`: Datas inválidas viram `NaT` (Not a Time)
6. **Guardar dados**: `.copy()` cria cópia independente
7. **Atualizar interface**: Mostra dados na tabela

**Por que `errors='coerce'`?**
- Evita erro se houver data mal formatada
- Permite continuar processamento

---

### **3. `aplicar_filtro_data()` - FUNÇÃO PRINCIPAL** 🎯

```python
def aplicar_filtro_data(self):
    if self.df_original is None:
        messagebox.showwarning("Aviso", "Carregue os dados primeiro!")
        return
    
    try:
        # 1. Obter datas selecionadas
        data_inicio = self.data_inicio.get_date()
        data_fim = self.data_fim.get_date()
        
        # 2. Converter para Timestamp do pandas
        data_inicio_pd = pd.Timestamp(data_inicio)
        data_fim_pd = pd.Timestamp(data_fim)
        
        # 3. Validar intervalo
        if data_inicio_pd > data_fim_pd:
            messagebox.showwarning("Aviso", "A data inicial não pode ser maior que a data final!")
            return
        
        # 4. Filtrar DataFrame
        df_filtrado = self.df_original[
            (self.df_original['Data Emissao'] >= data_inicio_pd) &
            (self.df_original['Data Emissao'] <= data_fim_pd)
        ]
        
        # 5. Atualizar dados filtrados
        self.df_filtrado = df_filtrado
        
        # 6. Atualizar tabela
        self.atualizar_tabela(self.df_filtrado)
        
        # 7. Mostrar confirmação
        messagebox.showinfo(
            "Filtro Aplicado",
            f"✅ Filtro de data aplicado!\n\n"
            f"Período: {data_inicio.strftime('%d/%m/%Y')} até {data_fim.strftime('%d/%m/%Y')}\n"
            f"Solicitações encontradas: {len(df_filtrado)}"
        )
        
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao aplicar filtro:\n{str(e)}")
```

**Explicação detalhada:**

#### **Passo 1: Obter datas**
```python
data_inicio = self.data_inicio.get_date()
data_fim = self.data_fim.get_date()
```
- `get_date()`: Retorna objeto `datetime.date` do Python

#### **Passo 2: Converter para Timestamp**
```python
data_inicio_pd = pd.Timestamp(data_inicio)
data_fim_pd = pd.Timestamp(data_fim)
```
- `pd.Timestamp`: Tipo de data do pandas, compatível com DataFrame
- Necessário para comparação com coluna 'Data Emissao'

#### **Passo 3: Validação**
```python
if data_inicio_pd > data_fim_pd:
    messagebox.showwarning("Aviso", "...")
    return
```
- Impede que usuário selecione data inicial maior que final
- `return`: Sai da função sem executar resto do código

#### **Passo 4: Filtro com operadores lógicos** 🔥
```python
df_filtrado = self.df_original[
    (self.df_original['Data Emissao'] >= data_inicio_pd) &
    (self.df_original['Data Emissao'] <= data_fim_pd)
]
```

**Como funciona:**
- `>=`: Maior ou igual (inclui data inicial)
- `<=`: Menor ou igual (inclui data final)
- `&`: Operador "E" (ambas condições devem ser verdadeiras)
- `()`: Parênteses obrigatórios para cada condição

**Exemplo prático:**
```
Data Inicio: 15/03/2026
Data Fim: 17/03/2026

Resultado: Todas as SAs emitidas entre 15/03/2026 e 17/03/2026 (inclusive)
```

---

### **4. `limpar_filtro()`**

```python
def limpar_filtro(self):
    if self.df_original is None:
        messagebox.showwarning("Aviso", "Carregue os dados primeiro!")
        return
    
    self.df_filtrado = self.df_original.copy()
    self.atualizar_tabela(self.df_filtrado)
    messagebox.showinfo("Filtro Limpo", "✅ Filtro de data removido. Exibindo todos os dados.")
```

**O que faz:**
- Restaura `df_filtrado` para conter todos os dados
- Remove filtro de data
- Mantém filtros de grupo e status (esses são permanentes)

---

### **5. `atualizar_tabela()`**

```python
def atualizar_tabela(self, df):
    # 1. Limpar tabela
    self.tree.delete(*self.tree.get_children())
    
    if df is None or df.empty:
        self.info_label.config(text="📊 Nenhum dado para exibir")
        return
    
    # 2. Configurar colunas
    colunas = list(df.columns)
    self.tree['columns'] = colunas
    self.tree['show'] = 'headings'
    
    for col in colunas:
        self.tree.heading(col, text=col)
        # Definir largura por coluna...
    
    # 3. Inserir dados
    for idx, row in df.iterrows():
        valores = []
        for col in colunas:
            valor = row[col]
            if pd.isna(valor):
                valores.append('')
            elif col == 'Data Emissao' and isinstance(valor, pd.Timestamp):
                valores.append(valor.strftime('%d/%m/%Y'))
            else:
                valores.append(str(valor))
        
        self.tree.insert('', tk.END, values=valores)
    
    # 4. Atualizar info
    self.info_label.config(
        text=f"📊 Exibindo {len(df)} solicitações | "
             f"Quantidade total: {df['Quantidade'].sum():.0f}",
        fg='#27ae60'
    )
```

**Explicação:**

#### **Limpar tabela**
```python
self.tree.delete(*self.tree.get_children())
```
- `get_children()`: Retorna lista de todas as linhas
- `*`: Desempacota lista para passar como argumentos
- `delete()`: Remove todas as linhas

#### **Formatar valores**
```python
if pd.isna(valor):
    valores.append('')
elif col == 'Data Emissao' and isinstance(valor, pd.Timestamp):
    valores.append(valor.strftime('%d/%m/%Y'))
else:
    valores.append(str(valor))
```
- `pd.isna()`: Verifica se é NaN (valor vazio)
- `isinstance()`: Verifica tipo do objeto
- `strftime('%d/%m/%Y')`: Formata data para DD/MM/AAAA

#### **Inserir linha**
```python
self.tree.insert('', tk.END, values=valores)
```
- `''`: Inserir na raiz (sem parent)
- `tk.END`: Inserir no final
- `values`: Lista com valores de cada coluna

---

### **6. `exportar_excel()`**

```python
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
```

**Explicação:**
- `asksaveasfilename()`: Diálogo para salvar arquivo
- `defaultextension`: Adiciona `.xlsx` se usuário não especificar
- `initialfile`: Nome sugerido
- `.dt.strftime()`: Formata coluna inteira de datas
- `index=False`: Não exporta índice do DataFrame

---

## 🎨 Personalização

### **Cores**

```python
# Cabeçalho e rodapé
bg='#2c3e50'  # Azul escuro

# Botões
bg='#3498db'  # Azul claro (Procurar)
bg='#27ae60'  # Verde (Carregar)
bg='#e67e22'  # Laranja (Aplicar Filtro)
bg='#95a5a6'  # Cinza (Limpar)
bg='#16a085'  # Verde água (Exportar)
```

### **Fontes**

```python
font=('Segoe UI', 20, 'bold')  # Título
font=('Segoe UI', 10, 'bold')  # Labels
font=('Segoe UI', 9)           # Texto normal
```

### **Larguras de Colunas**

```python
if col == 'Descricao':
    width = 300
elif col == 'Observacao':
    width = 250
elif col in ['Numero SA', 'Codigo']:
    width = 80
elif col == 'Data Emissao':
    width = 100
else:
    width = 120
```

---

## 🔧 Conceitos Importantes

### **1. Gerenciadores de Layout**

**pack():**
```python
widget.pack(side=tk.LEFT, fill=tk.X, padx=10, pady=5)
```
- `side`: Lado onde posicionar (LEFT, RIGHT, TOP, BOTTOM)
- `fill`: Preencher espaço (X=horizontal, Y=vertical, BOTH=ambos)
- `padx/pady`: Espaçamento externo

### **2. Tratamento de Erros**

```python
try:
    # Código que pode dar erro
except FileNotFoundError:
    # Erro específico: arquivo não encontrado
except Exception as e:
    # Qualquer outro erro
```

### **3. DataFrames Pandas**

**Filtrar:**
```python
df[df['coluna'] > 10]  # Valores maiores que 10
df[df['coluna'].isin([1, 2, 3])]  # Valores na lista
df[~df['coluna'].isin([1, 2])]  # Valores NÃO na lista (~)
```

**Comparação de datas:**
```python
df[(df['Data'] >= inicio) & (df['Data'] <= fim)]
```

**Copiar:**
```python
df_novo = df_original.copy()  # Cópia independente
```

### **4. Timestamps do Pandas**

```python
# Converter para Timestamp
pd.Timestamp('2026-03-15')
pd.to_datetime('15/03/2026', format='%d/%m/%Y')

# Formatar para string
timestamp.strftime('%d/%m/%Y')  # 15/03/2026

# Comparar
timestamp1 >= timestamp2
```

---

## 📊 Fluxo de Dados

```
1. Usuário clica "Carregar Dados"
   ↓
2. carregar_dados() executa
   ↓
3. Excel → DataFrame
   ↓
4. Aplicar filtros de grupo/status
   ↓
5. Converter datas para Timestamp
   ↓
6. Guardar em df_original
   ↓
7. Copiar para df_filtrado
   ↓
8. atualizar_tabela() exibe dados
   ↓
9. Usuário seleciona datas e clica "Aplicar Filtro"
   ↓
10. aplicar_filtro_data() executa
   ↓
11. Filtrar df_original por intervalo de datas
   ↓
12. Atualizar df_filtrado
   ↓
13. atualizar_tabela() exibe dados filtrados
   ↓
14. Usuário clica "Exportar para Excel"
   ↓
15. exportar_excel() salva df_filtrado
```

---

## 🚀 Melhorias Futuras Possíveis

1. **Filtros adicionais:**
   - Por armazém
   - Por setor
   - Por solicitante
   - Por quantidade mínima/máxima

2. **Estatísticas:**
   - Total de quantidade
   - Top 5 armazéns
   - Top 5 setores
   - Gráficos (matplotlib)

3. **Ordenação:**
   - Clicar no cabeçalho para ordenar

4. **Busca:**
   - Campo de busca por código ou descrição

5. **Temas:**
   - Modo claro/escuro
   - Cores personalizáveis

6. **Histórico:**
   - Salvar últimos arquivos abertos
   - Salvar configurações de filtro

---

## 📝 Resumo dos Conceitos Aprendidos

### **Tkinter:**
- ✅ Criar janelas e widgets
- ✅ Gerenciadores de layout (pack)
- ✅ Eventos e callbacks (command)
- ✅ Treeview para tabelas
- ✅ Diálogos (messagebox, filedialog)

### **Pandas:**
- ✅ Carregar Excel
- ✅ Filtrar dados com condições
- ✅ Selecionar e renomear colunas
- ✅ Trabalhar com datas (Timestamp)
- ✅ Exportar para Excel

### **Python:**
- ✅ Classes e métodos
- ✅ Tratamento de erros (try/except)
- ✅ Manipulação de strings
- ✅ Listas e dicionários

### **tkcalendar:**
- ✅ Widget DateEntry
- ✅ Seleção de datas com calendário visual
- ✅ Formatação de datas

---

## 🎓 Conclusão

Esta interface demonstra:
- **Integração** entre Tkinter e Pandas
- **Filtros dinâmicos** de dados
- **Interface profissional** e intuitiva
- **Boas práticas** de programação (tratamento de erros, código organizado)

O código está **pronto para produção** e pode ser facilmente expandido com novas funcionalidades!

---

**Desenvolvido com 💙 por Diego Bernardes & Yahiko**  
**DBSolutions Lab - 2026**
