# Python do Zero ao Avançado — Aprendendo com o Projeto Rubi

Este documento usa o `main.py` do sistema Rubi como base de ensino. Cada conceito é explicado
à medida que aparece no código real. Você vai entender não só o *que* cada linha faz, mas
o *porquê* de cada decisão.

---

## Índice

1. [Como ler este documento](#1-como-ler-este-documento)
2. [Antes de escrever código — como pensar num projeto](#2-antes-de-escrever-código--como-pensar-num-projeto)
3. [O ponto de partida — o bloco `if __name__ == "__main__"`](#3-o-ponto-de-partida--o-bloco-if-__name__--__main__)
4. [Imports — o que são, por que existem](#4-imports--o-que-são-por-que-existem)
5. [Funções — o bloco de construção básico](#5-funções--o-bloco-de-construção-básico)
6. [Orientação a Objetos (OOP) — o coração do Rubi](#6-orientação-a-objetos-oop--o-coração-do-rubi)
7. [A classe `Toast` — método estático e design enxuto](#7-a-classe-toast--método-estático-e-design-enxuto)
8. [A classe `SolicitacoesAppPro` — a aplicação inteira](#8-a-classe-solicitacoesapppro--a-aplicação-inteira)
9. [Tkinter — construindo janelas em Python](#9-tkinter--construindo-janelas-em-python)
10. [Pandas — análise de dados com DataFrames](#10-pandas--análise-de-dados-com-dataframes)
11. [Matplotlib — gráficos dentro da janela](#11-matplotlib--gráficos-dentro-da-janela)
12. [Sistema de Cache com parquet e hashlib](#12-sistema-de-cache-com-parquet-e-hashlib)
13. [Configurações persistentes com JSON](#13-configurações-persistentes-com-json)
14. [Tratamento de Erros — o profissional não deixa o programa travar](#14-tratamento-de-erros--o-profissional-não-deixa-o-programa-travar)
15. [Padrões avançados usados no Rubi](#15-padrões-avançados-usados-no-rubi)
16. [Exportação de dados — Excel, TXT e PDF](#16-exportação-de-dados--excel-txt-e-pdf)
17. [Como montar um projeto assim do zero](#17-como-montar-um-projeto-assim-do-zero)
18. [Mapa mental do Rubi](#18-mapa-mental-do-rubi)

---

## 1. Como ler este documento

Cada seção apresenta um conceito Python e mostra onde ele aparece no Rubi. Os blocos de código
são retirados diretamente do `main.py` — você pode abrir o arquivo ao lado e acompanhar.

Convenção usada aqui:

- **Conceito** — explicação didática do conceito Python
- **No Rubi** — como o conceito aparece no projeto real
- **Por que assim** — a decisão de design por trás da escolha

---

## 2. Antes de escrever código — como pensar num projeto

Antes de digitar a primeira linha, todo projeto profissional começa com três perguntas:

### Qual problema estou resolvendo?

O Rubi resolve um problema muito específico: o usuário precisava visualizar e analisar as
solicitações ao armazém que vinham de uma planilha Excel. Antes do Rubi, ele abria o Excel,
filtrava manualmente, e tentava entender os dados sem nenhum gráfico ou resumo automático.

A solução: uma aplicação desktop que lê o Excel, mostra os dados em tabelas, aplica filtros,
gera gráficos e exporta relatórios — tudo com um clique.

### Quem vai usar?

Um usuário não técnico. Isso determina decisões de design:
- Interface visual, não linha de comando
- Botões com rótulos claros
- Notificações amigáveis (Toast) em vez de erros técnicos
- Executável `.exe` para não precisar instalar Python

### Qual é a estrutura mínima que eu preciso?

Para um projeto desktop Python com análise de dados:

```
ControladorSA/
├── main.py          ← toda a lógica da aplicação
├── requirements.txt ← dependências
├── assets/          ← fontes, ícones
└── .venv/           ← ambiente virtual (nunca commitar)
```

Projetos simples começam em um único arquivo. Você só separa em módulos quando o arquivo
cresce além de ~1000 linhas e começa a ficar difícil de navegar. O Rubi tem ~2600 linhas
num único arquivo — isso é aceitável para uma aplicação desktop de pequeno porte.

---

## 3. O ponto de partida — o bloco `if __name__ == "__main__"`

```python
# Linha 2606 do main.py
if __name__ == "__main__":
    _registrar_fontes()
    
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")
    
    root = ctk.CTk()
    app = SolicitacoesAppPro(root)
    try:
        root.mainloop()
    except KeyboardInterrupt:
        pass
```

### O conceito

Todo arquivo Python pode ser executado diretamente (`python main.py`) ou importado por outro
arquivo (`import main`). A variável especial `__name__` vale `"__main__"` apenas quando você
executa o arquivo diretamente. Se outra parte do código importar esse arquivo, `__name__`
vale o nome do módulo (ex: `"main"`).

Esse padrão garante que o bloco de inicialização só rode quando você realmente quer iniciar
a aplicação, não quando outro arquivo importa suas classes ou funções.

### Por que isso importa

Imagine que você escreveu uma função útil em `main.py` e quer reutilizá-la em outro arquivo.
Sem o `if __name__ == "__main__"`, importar `main` abriria a janela da aplicação
automaticamente — o que é um comportamento indesejado.

### A sequência de inicialização do Rubi

1. `_registrar_fontes()` — registra as fontes Quicksand no sistema operacional
2. `ctk.set_appearance_mode("light")` — configura o tema do CustomTkinter
3. `root = ctk.CTk()` — cria a janela principal
4. `app = SolicitacoesAppPro(root)` — passa a janela para a classe da aplicação
5. `root.mainloop()` — inicia o loop de eventos (bloqueia até o usuário fechar)

---

## 4. Imports — o que são, por que existem

```python
# Linhas 0-14 do main.py
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
import numpy as np
import hashlib
```

### O conceito

Python vem com muitas funcionalidades já prontas (chamadas de **biblioteca padrão**) e permite
instalar funcionalidades extras (chamadas de **pacotes de terceiros**). Para usar qualquer uma
delas, você precisa declarar explicitamente com `import`.

### Dois estilos de import

**`import modulo`** — importa o módulo inteiro, você acessa com `modulo.funcao()`
```python
import os
os.path.exists("arquivo.txt")  # precisa do prefixo "os."
```

**`from modulo import nome`** — importa um nome específico, você acessa diretamente
```python
from datetime import datetime
datetime.now()  # sem prefixo
```

**`import modulo as apelido`** — importa com um apelido mais curto
```python
import pandas as pd
pd.read_excel(...)  # "pd" em vez de "pandas"
```

### Classificando os imports do Rubi

| Import | Tipo | Para que serve |
|--------|------|----------------|
| `tkinter` | Biblioteca padrão | Interface gráfica (janelas, botões) |
| `datetime` | Biblioteca padrão | Datas e horas |
| `os` | Biblioteca padrão | Operações de sistema (arquivos, pastas) |
| `sys` | Biblioteca padrão | Informações do interpretador Python |
| `json` | Biblioteca padrão | Ler e escrever arquivos JSON |
| `hashlib` | Biblioteca padrão | Gerar hashes criptográficos (MD5, SHA) |
| `ctypes` | Biblioteca padrão | Chamar funções do Windows (DLLs) |
| `numpy` | Terceiros | Vetorização e lógica condicional em colunas |
| `pandas` | Terceiros | Análise de dados, leitura de Excel |
| `matplotlib` | Terceiros | Geração de gráficos |
| `customtkinter` | Terceiros | Widgets modernos para Tkinter |
| `tkcalendar` | Terceiros | Widget de calendário |

### Por que importar só o que você precisa?

Importar módulos tem custo (tempo de carga, memória). Mais importante: importar nomes
específicos deixa o código mais legível — `datetime.now()` é mais claro que `from datetime
import *` e depois chamar só `now()` (de onde veio esse `now()`?).

---

## 5. Funções — o bloco de construção básico

```python
# Linhas 90-106 do main.py
def _registrar_fontes():
    """Registra as fontes empacotadas via PyInstaller antes de abrir a janela."""
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
            gdi32.AddFontResourceExW(caminho, 0x10, 0)
```

### O conceito de função

Uma função é um bloco de código com um nome, que pode ser chamado quando você precisar.
Funções resolvem dois problemas:

1. **Reuso** — escreva uma vez, use em vários lugares
2. **Organização** — dê um nome descritivo a um bloco de lógica

### Anatomia de uma função Python

```python
def nome_da_funcao(parametro1, parametro2="valor_padrao"):
    """Docstring: explica o que a função faz."""
    # corpo da função
    resultado = parametro1 + parametro2
    return resultado  # opcional: retorna um valor
```

### Convenções de nomenclatura

Python usa `snake_case` para funções e variáveis (palavras separadas por underscore).
Um underscore inicial (`_registrar_fontes`) é uma convenção que sinaliza "esta função é
de uso interno, não faz parte da API pública".

### O que `_registrar_fontes` faz

1. Verifica se o programa está rodando como executável PyInstaller (`sys._MEIPASS`)
2. Localiza a pasta de fontes (`assets/fonts`)
3. Para cada arquivo `.ttf` ou `.otf` encontrado, registra a fonte no Windows via API GDI32

`ctypes.windll.gdi32` é a forma Python de chamar diretamente a biblioteca do Windows que
gerencia fontes. `AddFontResourceExW` é uma função da API do Windows — o `W` no final
significa que aceita strings Unicode (Wide).

### `hasattr` — verificando se um atributo existe

```python
if hasattr(sys, '_MEIPASS'):
```

`hasattr(objeto, 'nome')` retorna `True` se o objeto tiver aquele atributo. Aqui, verifica
se `sys` tem `_MEIPASS` — esse atributo só existe quando rodando dentro de um executável
PyInstaller. É mais seguro que `sys._MEIPASS` diretamente (que lançaria `AttributeError`
se não existisse).

---

## 6. Orientação a Objetos (OOP) — o coração do Rubi

Orientação a objetos é o paradigma de programação mais usado em projetos reais. O Rubi usa
OOP com duas classes: `Toast` e `SolicitacoesAppPro`.

### O que é uma classe?

Uma **classe** é um molde para criar objetos. Um **objeto** (ou instância) é uma cópia
concreta criada a partir do molde.

Analogia: a planta de uma casa é a classe. Cada casa construída a partir da planta é um objeto.

```python
# Definindo a classe (o molde)
class Pessoa:
    def __init__(self, nome, idade):
        self.nome = nome      # atributo de instância
        self.idade = idade

    def saudar(self):
        return f"Olá, meu nome é {self.nome}"

# Criando objetos (instâncias)
diego = Pessoa("Diego", 25)
maria = Pessoa("Maria", 30)

print(diego.saudar())    # "Olá, meu nome é Diego"
print(maria.saudar())    # "Olá, meu nome é Maria"
```

### O método `__init__` — o construtor

`__init__` é chamado automaticamente quando você cria um objeto com `Classe(argumentos)`.
Ele é responsável por inicializar o estado inicial do objeto.

A palavra `self` é uma referência ao objeto que está sendo criado. Todo método de instância
precisa ter `self` como primeiro parâmetro — o Python passa isso automaticamente.

### Por que usar classes em vez de funções simples?

Para o Rubi, a aplicação precisa manter **estado** ao longo de toda a execução:
- Qual arquivo Excel está carregado
- Qual filtro de data está ativo
- Quais dados estão no DataFrame
- Referências para os widgets da interface

Com funções simples, você precisaria passar tudo isso como parâmetros o tempo todo.
Com uma classe, o estado fica em `self` e qualquer método pode acessá-lo diretamente.

---

## 7. A classe `Toast` — método estático e design enxuto

```python
# Linhas 17-87 do main.py
class Toast:
    """Sistema de notificações toast modernas"""
    
    @staticmethod
    def show(parent, message, tipo='info', duration=3000):
        cores = {
            'success': {'bg': '#27ae60', 'fg': 'white', 'icon': '✅'},
            'error':   {'bg': '#e74c3c', 'fg': 'white', 'icon': '❌'},
            'warning': {'bg': '#e67e22', 'fg': 'white', 'icon': '⚠️'},
            'info':    {'bg': '#3498db', 'fg': 'white', 'icon': 'ℹ️'}
        }
        
        cor = cores.get(tipo, cores['info'])
        
        toast = tk.Toplevel(parent)
        toast.overrideredirect(True)   # sem barra de título
        toast.attributes('-topmost', True)
        
        frame = tk.Frame(toast, bg=cor['bg'], relief=tk.RAISED, borderwidth=3)
        frame.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        
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
        
        toast.update_idletasks()
        width = toast.winfo_width()
        height = toast.winfo_height()
        x = parent.winfo_x() + parent.winfo_width() - width - 20
        y = parent.winfo_y() + 80
        toast.geometry(f'+{x}+{y}')
        
        def fade_out(alpha=1.0):
            if alpha > 0:
                alpha -= 0.05
                toast.attributes('-alpha', alpha)
                toast.after(50, lambda: fade_out(alpha))
            else:
                toast.destroy()
        
        toast.after(duration, fade_out)
        return toast
```

### O decorador `@staticmethod`

Um método estático pertence à classe, mas não precisa de uma instância para funcionar.
Ele não recebe `self` (nem `cls`).

Quando usar método estático: quando a lógica é relacionada à classe conceitualmente,
mas não depende de nenhum estado de instância.

```python
# Chamada: não precisa criar um objeto Toast
Toast.show(self.root, "Arquivo carregado!", tipo='success')
```

Se `show` fosse um método comum, você precisaria fazer:
```python
toast = Toast()           # criar instância
toast.show(self.root, …)  # chamar o método
```

Mas criar uma instância de `Toast` não faz sentido — ela não tem estado próprio.
O método estático é a escolha certa aqui.

### Parâmetros com valor padrão (default arguments)

```python
def show(parent, message, tipo='info', duration=3000):
```

`tipo='info'` e `duration=3000` são valores padrão. Se o chamador não passar esses
argumentos, os padrões são usados:

```python
Toast.show(self.root, "Aviso")           # tipo='info', duration=3000
Toast.show(self.root, "Erro!", tipo='error', duration=5000)  # explícito
```

**Regra importante:** parâmetros com valor padrão sempre vêm depois dos sem padrão.

### Dicionários como tabelas de decisão

```python
cores = {
    'success': {'bg': '#27ae60', 'fg': 'white', 'icon': '✅'},
    'error':   {'bg': '#e74c3c', 'fg': 'white', 'icon': '❌'},
    'warning': {'bg': '#e67e22', 'fg': 'white', 'icon': '⚠️'},
    'info':    {'bg': '#3498db', 'fg': 'white', 'icon': 'ℹ️'}
}
cor = cores.get(tipo, cores['info'])
```

Aqui `cores` é um dicionário de dicionários. Esse padrão substitui um `if/elif/else`
longo e é muito mais fácil de manter — para adicionar um novo tipo, basta adicionar
uma linha no dicionário.

`dict.get(chave, valor_padrão)` retorna o valor se a chave existir, ou o `valor_padrão`
caso contrário. Aqui, se `tipo` não existir no dicionário, usa `cores['info']`.

### Funções aninhadas (closures)

```python
def fade_out(alpha=1.0):
    if alpha > 0:
        alpha -= 0.05
        toast.attributes('-alpha', alpha)
        toast.after(50, lambda: fade_out(alpha))
    else:
        toast.destroy()

toast.after(duration, fade_out)
```

`fade_out` é uma função definida dentro de outra função (`show`). Ela tem acesso à
variável `toast` do escopo externo — isso se chama **closure**.

`toast.after(ms, funcao)` agenda a execução de `funcao` após `ms` milissegundos.
Isso cria uma animação: a cada 50ms, a opacidade (`alpha`) diminui em 0.05. Quando
chega a zero, a janela é destruída.

`lambda: fade_out(alpha)` cria uma função anônima que chama `fade_out(alpha)`.
O `lambda` é necessário porque precisamos passar o valor atual de `alpha`,
não uma referência — sem o `lambda`, o valor seria capturado apenas na última iteração.

---

## 8. A classe `SolicitacoesAppPro` — a aplicação inteira

```python
# Linha 108
class SolicitacoesAppPro:
    def __init__(self, root):
        self.root = root
        self.root.title("♦ Rubi - Sistema de Controle de Solicitações")
        self.root.geometry("1600x900")
        self.root.configure(bg='#f0f0f0')
        
        self.df_original = None
        self.df_filtrado = None
        self.filtro_data_inicio = None
        self.filtro_data_fim = None
        self.progress_bar = None

        self.filtro_armazem_var     = tk.StringVar(value="Todos")
        self.filtro_setor_var       = tk.StringVar(value="Todos")
        self.filtro_solicitante_var = tk.StringVar(value="Todos")
        # ...
        
        _app_data = os.path.join(os.environ.get('APPDATA', os.path.expanduser('~')), 'RubiApp')
        os.makedirs(_app_data, exist_ok=True)
        self.config_file = os.path.join(_app_data, 'config.json')
        self.config = self.carregar_config()

        self._save_widths_job_dados  = None
        self._save_widths_job_status = None

        self.cache_dir = os.path.join(_app_data, '.cache')
        os.makedirs(self.cache_dir, exist_ok=True)
        
        self.criar_interface()
```

### Inicializando o estado da aplicação

O `__init__` do Rubi faz seis coisas:

1. **Configura a janela** — título, tamanho, cor de fundo
2. **Inicializa DataFrames como `None`** — ainda não há dados carregados
3. **Cria variáveis Tkinter** — `tk.StringVar` é um tipo especial que notifica a UI quando muda
4. **Carrega configurações** — lê `config.json` com preferências salvas
5. **Inicializa sistema de debounce** — controla frequência de salvamento
6. **Garante que o diretório de cache existe** — `os.makedirs`

### Caminhos portáveis com `%APPDATA%`

```python
_app_data = os.path.join(os.environ.get('APPDATA', os.path.expanduser('~')), 'RubiApp')
os.makedirs(_app_data, exist_ok=True)
self.config_file = os.path.join(_app_data, 'config.json')
```

Salvar `config.json` e o cache na pasta de trabalho (`'config.json'` relativo) funciona durante o desenvolvimento, mas quebra num executável PyInstaller: o `.exe` pode estar em `C:\Program Files` onde o Windows não permite escrita por usuários comuns.

`%APPDATA%` é a pasta reservada para dados de aplicação por usuário — tipicamente `C:\Users\Diego\AppData\Roaming`. O Windows garante permissão de escrita. Para aplicações desktop Windows, sempre salve configurações e cache aqui.

`os.environ.get('APPDATA', os.path.expanduser('~'))` — o `get` com fallback garante que o código não quebra em Linux/macOS onde `APPDATA` não existe (usa o home do usuário como alternativa).

`os.makedirs(_app_data, exist_ok=True)` — cria a pasta e todas as intermediárias necessárias. O parâmetro `exist_ok=True` evita erro se a pasta já existir — sem ele, você precisaria verificar manualmente com `os.path.exists` antes.

### Por que inicializar como `None`?

```python
self.df_original = None
self.df_filtrado = None
```

Antes de o usuário carregar um arquivo, não há dados. Inicializar como `None` é uma
forma de representar "dado ainda não existe". Ao longo do código, você verifica:

```python
if self.df_filtrado is None:
    return
```

Isso é mais claro que verificar `if len(df) == 0` — um DataFrame vazio é diferente de
um DataFrame inexistente.

**`is None` vs `== None`:** Use sempre `is None`. O operador `is` verifica identidade
(o objeto *é* exatamente `None`). O `==` pode ser sobrecarregado por classes como
pandas DataFrame e lançar erros.

### `tk.StringVar` — variáveis reativas

```python
self.filtro_armazem_var = tk.StringVar(value="Todos")
```

`StringVar` é uma variável do Tkinter que pode ser "observada". Quando seu valor muda,
widgets vinculados a ela atualizam automaticamente. Aqui é usada para conectar os
dropdowns de filtro ao estado da aplicação.

Outros tipos: `IntVar`, `BooleanVar`, `DoubleVar`.

---

## 9. Tkinter — construindo janelas em Python

Tkinter é a biblioteca de interface gráfica incluída no Python. O Rubi usa Tkinter puro
e CustomTkinter (que adiciona aparência moderna).

### Os dois sistemas de layout

Tkinter tem três gerenciadores de layout:

#### `pack` — empilhamento linear

```python
# Linhas 153-159 do main.py
main_frame = tk.Frame(self.root, bg='#f0f0f0')
main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

header_frame = tk.Frame(main_frame, bg='#2c3e50', height=70)
header_frame.pack(fill=tk.X, pady=(0, 10))
```

`fill=tk.BOTH` — ocupa todo o espaço disponível horizontal e vertical
`fill=tk.X` — ocupa toda a largura
`expand=True` — cresce quando a janela é redimensionada
`padx`, `pady` — espaçamento externo (margens)

#### `grid` — grade com linhas e colunas

```python
# Linhas 560-562 do main.py
self.tree.grid(row=0, column=0, sticky='nsew')
scroll_y.grid(row=0, column=1, sticky='ns')
scroll_x.grid(row=1, column=0, sticky='ew')
```

`sticky='nsew'` — o widget se expande em todas as direções (Norte-Sul-Leste-Oeste)
Ideal para tabelas com scrollbars, porque precisa posicionar a tabela e as barras
exatamente numa grade.

#### `place` — posição absoluta ou relativa

```python
# Linha 164 do main.py
header_content.place(relx=0.5, rely=0.5, anchor='center')
```

`relx=0.5, rely=0.5` — 50% da largura e altura do pai
`anchor='center'` — o ponto de ancoragem é o centro do widget
Usado no Rubi apenas para centralizar o cabeçalho dentro da faixa escura.

### Hierarquia de widgets

Em Tkinter, cada widget tem um **pai** (parent). A hierarquia é:

```
root (CTk)
└── main_frame (Frame)
    ├── header_frame (Frame)
    │   └── header_content (Frame)
    │       ├── title_label (Label)
    │       └── subtitle_label (Label)
    ├── control_frame (CTkFrame)
    │   ├── file_frame (Frame)
    │   └── filter_frame (Frame)
    └── notebook (Notebook)
        ├── aba_dados (Frame)
        ├── aba_status (Frame)
        ├── aba_dashboard (Frame)
        ├── aba_analise (Frame)
        └── aba_resumo (Frame)
```

### O sistema de abas (Notebook)

```python
# Linhas 343-355 do main.py
self.notebook = ttk.Notebook(main_frame)
self.notebook.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

style = ttk.Style()
style.configure('TNotebook.Tab', font=('Quicksand', 12, 'bold'), padding=[20, 10])

self.criar_aba_dados()
self.criar_aba_status_atendimento()
self.criar_aba_dashboard()
self.criar_aba_analise()
self.criar_aba_resumo()
```

`ttk.Notebook` é um container que exibe abas. Cada aba é um `Frame` adicionado com
`notebook.add(frame, text='Nome da Aba')`.

`ttk.Style` permite customizar a aparência dos widgets `ttk` — neste caso, a fonte e
o espaçamento interno das abas.

### Treeview — a tabela de dados

```python
# Linhas 550-575 do main.py
self.tree = ttk.Treeview(table_frame, selectmode='extended')

scroll_y = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
scroll_x = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL, command=self.tree.xview)

self.tree.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
```

`Treeview` é o widget de tabela do Tkinter. Não é intuitivo — precisa de configuração:

1. Criar o Treeview
2. Criar Scrollbars separadas
3. Vincular: a scrollbar chama `tree.yview`, e o tree chama `scrollbar.set`

Essa ligação bidirecional é o que faz as barras de scroll funcionarem corretamente.

### Eventos e callbacks

```python
# Linha 466 do main.py
self.search_var = tk.StringVar()
self.search_var.trace('w', lambda *args: self.filtrar_tabela_busca())
```

`trace('w', callback)` chama o `callback` sempre que a variável for *escrita* (`'w'`).
Isso cria a busca em tempo real: conforme o usuário digita, `filtrar_tabela_busca()` é
chamado a cada tecla.

```python
# Linha 578 do main.py
self.tree.bind('<ButtonRelease-1>', self._on_resize_dados)
```

`bind(evento, callback)` conecta um evento ao widget. Aqui, quando o usuário solta o
botão do mouse (`ButtonRelease-1`) na tabela, `_on_resize_dados` é chamado — isso
detecta redimensionamento de colunas.

---

## 10. Pandas — análise de dados com DataFrames

Pandas é a biblioteca mais importante para análise de dados em Python.

### DataFrame — a planilha do Python

Um **DataFrame** é uma tabela bidimensional com linhas e colunas nomeadas.

```python
# Linha 1195 do main.py
df = pd.read_excel(arquivo, sheet_name='Relatório de Controle de entr')
```

`pd.read_excel()` lê um arquivo Excel e retorna um DataFrame. Com uma linha de código,
você tem a planilha inteira como objeto Python.

### Selecionando colunas

```python
# Linhas 1239-1241 do main.py
df_base = df_base[list(colunas_mapeamento.keys())]  # seleciona colunas específicas
df_base = df_base.rename(columns=colunas_mapeamento)  # renomeia
df_base['Data Emissao'] = pd.to_datetime(df_base['Data Emissao'], errors='coerce')
```

`df[['col1', 'col2']]` — seleciona colunas (retorna outro DataFrame)
`df.rename(columns={'antigo': 'novo'})` — renomeia colunas
`pd.to_datetime(coluna, errors='coerce')` — converte para data; valores inválidos
  viram `NaT` (Not a Time), equivalente ao `None` para datas

### Filtragem — boolean indexing

Esta é a operação mais poderosa do Pandas:

```python
# Linhas 1053-1073 do main.py
status_excluir = ['EM APROVAÇÃO', 'PRE-REQUISIÇÃO GERADA']
df = self.df_filtrado[~self.df_filtrado['Status'].isin(status_excluir)].copy()

if armazem != "Todos":
    df = df[df['Armazem'].astype(str) == armazem]

if termo:
    df = df[
        df['Descricao'].str.lower().str.contains(termo, na=False) |
        df['Setor'].str.lower().str.contains(termo, na=False)    |
        df['Solicitante'].str.lower().str.contains(termo, na=False)
    ]
```

**Como funciona:**
- `df['coluna'] == valor` retorna uma Série de booleanos (True/False por linha)
- `df[série_booleana]` retorna apenas as linhas onde é True
- `~` inverte a seleção (NOT)
- `|` é o OR lógico, `&` é o AND lógico

**`isin(lista)`** — verifica se o valor está na lista (mais eficiente que múltiplos `==`)

**`str.lower().str.contains(termo)`** — busca case-insensitive dentro de strings.
O prefixo `.str` é o "accessor de string" do Pandas — aplica métodos de string em toda a coluna.

**`.copy()`** — cria uma cópia independente do DataFrame. Sem `copy()`, modificar `df`
poderia modificar o DataFrame original (comportamento chamado de "view").

### Agregações e estatísticas

```python
# Linhas 1603-1616 do main.py
total_sas  = df_kpi['Numero SA'].nunique()   # quantidade de valores únicos
total_itens = len(df_kpi)                     # total de linhas
media_itens_sa = round(total_itens / total_sas, 2)

top_setores = df['Setor'].value_counts().head(10)  # contagem por valor, top 10
```

`nunique()` — número de valores distintos
`value_counts()` — contagem de cada valor único, ordenada por frequência
`head(n)` — primeiros n elementos

### Operações com datas

```python
# Linhas 1474-1477 do main.py
df_filtrado_data = self.df_original[
    (self.df_original['Data Emissao'] >= data_inicio_pd) &
    (self.df_original['Data Emissao'] <= data_fim_pd)
]
```

Após converter a coluna para datetime com `pd.to_datetime`, você pode comparar datas
diretamente com `>=` e `<=`. O resultado é uma máscara booleana que filtra o DataFrame.

```python
# Linha 1771 do main.py
df['Dia Semana'] = df['Data Emissao'].dt.day_name()
```

`.dt` é o accessor de datetime — dá acesso a propriedades de data: `.dt.day_name()`,
`.dt.dayofweek`, `.dt.month`, `.dt.year`, etc.

### Derivando colunas com `numpy.select`

Às vezes uma coluna não existe no arquivo — ela precisa ser calculada a partir de outras.
O Rubi faz isso com a coluna `Atendimento`, que replicava uma fórmula Excel:

```
=SE(S=H; "TOTALMENTE ATENDIDA"; SE(E(S<H; S<>0); "PARCIALMENTE ATENDIDA"; SE(T=0; "NÃO ATENDIDA"; "")))
```

Em Python com `numpy.select`:

```python
import numpy as np

qtd_sol   = pd.to_numeric(df['Quantidade Solicitada'], errors='coerce').fillna(0)
qtd_ate   = pd.to_numeric(df['Qtd. Atendida'],         errors='coerce').fillna(0)
custo_tot = pd.to_numeric(df['Custo Total'],            errors='coerce').fillna(0)
status_col = df['Status'] if 'Status' in df.columns else pd.Series('', index=df.index)

df['Atendimento'] = np.select(
    [
        qtd_ate == qtd_sol,
        (qtd_ate < qtd_sol) & (qtd_ate != 0),
        (custo_tot == 0) & (status_col != 'EM APROVAÇÃO'),
    ],
    ['TOTALMENTE ATENDIDA', 'PARCIALMENTE ATENDIDA', 'NÃO ATENDIDA'],
    default=''
)
```

**`np.select(condições, valores, default)`** recebe:
- Uma lista de condições booleanas (avaliadas em ordem)
- Uma lista de valores correspondentes (mesmo tamanho)
- Um valor `default` para linhas que não atendem nenhuma condição

Para cada linha do DataFrame, aplica a primeira condição verdadeira e usa o valor
correspondente. É equivalente a um `if/elif/else` aplicado a toda a coluna de uma vez —
muito mais rápido que iterar linha por linha com `iterrows`.

**Por que não usar `apply` com uma função?**

```python
# Lento: processa linha por linha em Python puro
df['Atendimento'] = df.apply(lambda row: calcular_atendimento(row), axis=1)

# Rápido: operações vetorizadas em C via numpy
df['Atendimento'] = np.select([...], [...])
```

`apply` é conveniente mas lento — chama uma função Python para cada linha.
`np.select` opera sobre arrays inteiros de uma vez (vetorizado), podendo ser 10-100x mais
rápido em DataFrames grandes.

**`pd.to_numeric(coluna, errors='coerce').fillna(0)`** — converte a coluna para numérico,
transformando valores inválidos (texto, None) em `NaN`, e depois substitui `NaN` por `0`.
Isso evita erros de comparação quando o Excel tem células vazias nessas colunas.

**`df['Status'] if 'Status' in df.columns else pd.Series('', index=df.index)`** — se a
coluna `Status` não existir no arquivo, cria uma Série de strings vazias com o mesmo índice.
Isso torna o cálculo tolerante a planilhas que não têm a coluna.

### Iterando sobre o DataFrame

```python
# Linhas 1400-1416 do main.py
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
```

`df.iterrows()` retorna pares `(índice, linha)`. Para cada linha do DataFrame, montamos
uma lista de valores formatados e inserimos na tabela Tkinter.

`pd.isna(valor)` — verifica se é valor nulo (None, NaN, NaT)
`isinstance(valor, pd.Timestamp)` — verifica se é um objeto de data do Pandas
`valor.strftime('%d/%m/%Y')` — formata a data como string

---

## 11. Matplotlib — gráficos dentro da janela

```python
# Linhas 1661-1680 do main.py
def criar_grafico_top_setores(self, parent):
    frame = tk.Frame(parent, bg='white', relief=tk.RAISED, borderwidth=2)
    
    fig = Figure(figsize=(7, 4.5), dpi=100)
    ax = fig.add_subplot(111)
    
    top_setores = df['Setor'].value_counts().head(10).sort_values(ascending=True)
    
    ax.barh(range(len(top_setores)), top_setores.values, color='#27ae60')
    ax.set_yticks(range(len(top_setores)))
    ax.set_yticklabels([s[:40] + '...' if len(s) > 40 else s for s in top_setores.index])
    ax.set_xlabel('Número de Solicitações')
    ax.grid(True, alpha=0.3, axis='x')
    ax.xaxis.set_major_locator(plt.MaxNLocator(integer=True))
    fig.tight_layout()
    
    canvas = FigureCanvasTkAgg(fig, frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    return frame
```

### A ponte entre Matplotlib e Tkinter

Normalmente, `plt.show()` abre uma janela separada do Matplotlib. No Rubi, usamos
`FigureCanvasTkAgg` — um "canvas" que renderiza o gráfico dentro de um widget Tkinter.

Fluxo:
1. Criar `Figure` (o "papel" do gráfico)
2. Adicionar `Axes` com `fig.add_subplot(111)` (o sistema de coordenadas)
3. Plotar dados no `ax`
4. Criar `FigureCanvasTkAgg(fig, frame_tkinter)` — renderizador Tkinter
5. `canvas.draw()` — renderizar
6. `canvas.get_tk_widget()` — obter o widget Tkinter e posicioná-lo

### Tipos de gráfico usados

**`ax.barh(y, values)`** — gráfico de barras horizontal (h = horizontal)
Bom para comparar categorias com nomes longos — os rótulos ficam no eixo Y com mais espaço.

**`ax.bar(x, values)`** — gráfico de barras vertical
Usado no gráfico de dias da semana.

### List comprehension — Python idiomático

```python
ax.set_yticklabels([s[:40] + '...' if len(s) > 40 else s for s in top_setores.index])
```

Isso é uma **list comprehension** — uma forma compacta de criar uma lista:

```python
# Forma longa equivalente:
labels = []
for s in top_setores.index:
    if len(s) > 40:
        labels.append(s[:40] + '...')
    else:
        labels.append(s)
ax.set_yticklabels(labels)
```

A list comprehension é mais pythônica e ocupa uma linha. Use quando a lógica for simples.
Se ficou complicado demais para uma linha, use o `for` normal — legibilidade primeiro.

### Recriando os gráficos ao filtrar

```python
# Linhas 1579-1581 do main.py
def atualizar_dashboard(self):
    for widget in self.dashboard_frame.winfo_children():
        widget.destroy()
```

Cada vez que o filtro muda, o Rubi **destrói todos os widgets filhos** do frame do
dashboard e recria tudo do zero. Essa é a abordagem mais simples: em vez de tentar
atualizar gráficos existentes, você apaga e redesenha.

`winfo_children()` retorna todos os widgets filhos diretos de um frame.

---

## 12. Sistema de Cache com parquet e hashlib

O cache é uma das funcionalidades mais interessantes do Rubi do ponto de vista técnico.

### O problema

Ler um arquivo Excel grande demora. Se o usuário abre a aplicação, carrega o arquivo,
fecha e abre de novo, por que precisaria reler o mesmo arquivo?

### A solução

1. Na primeira leitura: processar o Excel e salvar o resultado em disco (cache)
2. Nas leituras seguintes: verificar se o arquivo mudou (hash MD5)
3. Se não mudou: carregar do cache (muito mais rápido)
4. Se mudou: reler o Excel e atualizar o cache

### Gerando o hash do arquivo

```python
def gerar_hash_arquivo(self, filepath):
    try:
        hash_md5 = hashlib.md5()
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    except Exception as e:
        print(f"Erro ao gerar hash: {e}")
        return None
```

**MD5** é um algoritmo que transforma qualquer dado em uma string de 32 caracteres (hexadecimal).
Se o arquivo mudar minimamente, o MD5 muda completamente — é uma "impressão digital" do arquivo.

**Leitura em chunks:** `f.read(4096)` lê 4096 bytes por vez. Para arquivos grandes, ler
tudo de uma vez consome muita memória. Ler em chunks usa uma quantidade fixa de memória,
independente do tamanho do arquivo.

**`iter(lambda: f.read(4096), b"")`** — cria um iterador que chama `f.read(4096)` repetidamente
até que retorne `b""` (bytes vazio = fim do arquivo). É um padrão idiomático para leitura em chunks.

### Serializando com parquet

```python
def salvar_no_cache(self, arquivo, data):
    base = self.obter_cache_path(arquivo)
    arquivo_hash = self.gerar_hash_arquivo(arquivo)
    data['df_original'].to_parquet(base + '_original.parquet', index=False)
    data['df_status_original'].to_parquet(base + '_status.parquet', index=False)
    meta = {'hash': arquivo_hash, 'timestamp': datetime.now().isoformat()}
    with open(base + '.json', 'w', encoding='utf-8') as f:
        json.dump(meta, f)
    return True

def carregar_do_cache(self, arquivo):
    base = self.obter_cache_path(arquivo)
    meta_path = base + '.json'
    df1_path  = base + '_original.parquet'
    df2_path  = base + '_status.parquet'
    if not all(os.path.exists(p) for p in (meta_path, df1_path, df2_path)):
        return None
    arquivo_hash = self.gerar_hash_arquivo(arquivo)
    with open(meta_path, 'r', encoding='utf-8') as f:
        meta = json.load(f)
    if meta.get('hash') != arquivo_hash:
        return None
    return {
        'df_original':        pd.read_parquet(df1_path),
        'df_status_original': pd.read_parquet(df2_path),
    }
```

**Parquet** é um formato de armazenamento colunar adotado em engenharia de dados. Para DataFrames,
é superior ao pickle (que era usado antes) por três razões:

1. **Segurança** — `pickle.load` pode executar código arbitrário ao ler o arquivo. Um cache
   comprometido poderia rodar código malicioso silenciosamente. Parquet é um formato de dados
   puro — sem execução de código na leitura.

2. **Interoperabilidade** — parquet é legível por Python, Spark, R e ferramentas de BI.
   Pickle só funciona em Python (e pode quebrar entre versões diferentes).

3. **Eficiência** — armazenamento colunar com compressão automática. Geralmente mais compacto
   que pickle para DataFrames com colunas repetitivas (textos, categorias).

O cache do Rubi usa três arquivos por entrada:
- `{hash}_original.parquet` — DataFrame principal (solicitações)
- `{hash}_status.parquet` — DataFrame de status de atendimento
- `{hash}.json` — metadados (hash do Excel, timestamp)

Separar os metadados em JSON é uma decisão intencional: permite verificar a validade do cache
comparando o hash *sem* ler os arquivos parquet — e JSON é legível por humanos, facilitando
depuração.

**`all(os.path.exists(p) for p in (...))`** — verifica se todos os arquivos existem antes de
tentar ler qualquer um. `all()` com um gerador é eficiente: para na primeira falha, sem construir
a lista inteira na memória.

### Gerenciador de contexto `with`

```python
with open(base + '.json', 'w', encoding='utf-8') as f:
    json.dump(meta, f)
```

O bloco `with` garante que o arquivo será fechado corretamente, mesmo que ocorra um erro.
Sem `with`, um erro dentro do bloco deixaria o arquivo aberto (vazamento de recurso).

`with objeto as nome:` funciona com qualquer objeto que implemente o protocolo de contexto
(`__enter__` e `__exit__`). Arquivos, conexões de banco de dados e travas (locks) são os casos mais comuns.

---

## 13. Configurações persistentes com JSON

```python
def carregar_config(self):
    defaults = {'ultimo_arquivo': '', 'tema': 'light', 'versao': '1.0.0'}
    try:
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r', encoding='utf-8') as f:
                dados = json.load(f)
            if not isinstance(dados, dict):
                return defaults
            for chave in ('larguras_colunas', 'larguras_colunas_status'):
                if chave in dados and isinstance(dados[chave], dict):
                    dados[chave] = {
                        k: v for k, v in dados[chave].items()
                        if isinstance(v, int) and 10 <= v <= 2000
                    }
            return {**defaults, **dados}
    except Exception as e:
        print(f"Erro ao carregar config: {e}")
    return defaults

def salvar_config(self):
    try:
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"Erro ao salvar config: {e}")
```

**JSON** (JavaScript Object Notation) é um formato de texto para representar dados estruturados.
É legível por humanos e suportado por praticamente todas as linguagens.

```json
{
    "ultimo_arquivo": "simecr05.xlsx",
    "tema": "light",
    "larguras_colunas": {
        "Numero SA": 90,
        "Descricao": 350
    }
}
```

`json.load(f)` — lê arquivo JSON e retorna dicionário Python
`json.dump(dados, f, indent=4)` — salva dicionário Python como JSON formatado com indentação
`ensure_ascii=False` — permite caracteres especiais (acentos, cedilha) no arquivo

### Padrão: valor padrão como fallback

```python
defaults = {'ultimo_arquivo': '', 'tema': 'light', 'versao': '1.0.0'}
# ...
return {**defaults, **dados}  # dados do arquivo prevalece sobre defaults
```

Se o arquivo não existe, está corrompido, ou ocorre qualquer erro, a função retorna
`defaults`. A aplicação nunca trava por falta de configuração.

`{**defaults, **dados}` é o operador de unpacking de dicionários — merge os dois em um novo
dicionário. Chaves que aparecem nos dois usam o valor de `dados` (o arquivo tem precedência).
Isso garante que novas chaves adicionadas no `defaults` de versões futuras sempre apareçam,
mesmo que o `config.json` seja de uma versão mais antiga.

### Validação defensiva: nunca confie nos dados salvos

```python
if not isinstance(dados, dict):
    return defaults

for chave in ('larguras_colunas', 'larguras_colunas_status'):
    if chave in dados and isinstance(dados[chave], dict):
        dados[chave] = {
            k: v for k, v in dados[chave].items()
            if isinstance(v, int) and 10 <= v <= 2000
        }
```

`config.json` é escrito pelo próprio Rubi, mas pode ser editado manualmente ou corrompido.
Se alguém colocar `{"larguras_colunas": "texto"}`, o Tkinter tentaria usar essa string como
largura de coluna e travaria com `TclError`.

A validação aqui faz duas coisas:
1. Verifica que o JSON é um dicionário (`isinstance(dados, dict)`), não uma lista ou string
2. Filtra as larguras de coluna: mantém apenas entradas onde o valor é um `int` entre 10 e
   2000 pixels — descarta silenciosamente qualquer entrada inválida

**`isinstance(valor, tipo)`** — verifica se o objeto é do tipo especificado.
É mais seguro que `type(valor) == int` porque funciona com subclasses também.

**`10 <= v <= 2000`** — Python permite encadear comparações assim (operador ternário de faixa).
Equivale a `v >= 10 and v <= 2000`, mas mais legível.

---

## 14. Tratamento de Erros — o profissional não deixa o programa travar

```python
# Linhas 1302-1350 do main.py
except FileNotFoundError:
    self.progress_bar.pack_forget()
    self.info_label.config(text="❌ Arquivo não encontrado", fg='#e74c3c')
    Toast.show(self.root, f"Arquivo não encontrado: {os.path.basename(arquivo)}", tipo='error')

except PermissionError:
    Toast.show(self.root, "Feche o arquivo Excel e tente novamente", tipo='warning')

except pd.errors.ParserError:
    Toast.show(self.root, "Formato do arquivo Excel inválido", tipo='error')

except KeyError as e:
    Toast.show(self.root, f"Coluna esperada não encontrada: {str(e)}", tipo='error')

except Exception as e:
    error_msg = str(e)
    if len(error_msg) > 100:
        error_msg = error_msg[:100] + "..."
    Toast.show(self.root, f"Erro: {error_msg}", tipo='error')
    print(f"Erro detalhado: {e}")  # Log completo no console
```

### Hierarquia de exceções

Python tem uma hierarquia de exceções. Do mais específico ao mais genérico:

```
BaseException
└── Exception
    ├── OSError
    │   ├── FileNotFoundError  ← arquivo não existe
    │   └── PermissionError    ← sem permissão
    ├── ValueError
    ├── KeyError               ← chave não existe em dicionário/DataFrame
    └── ... (centenas de tipos)
```

**Regra:** trate primeiro as exceções mais específicas, depois as mais genéricas.
Um `except Exception` no início capturaria tudo e você perderia informação sobre
o tipo de erro.

### `finally` — sempre executa

```python
# Linhas 2113-2116 do main.py
finally:
    self.root.config(cursor='')
```

O bloco `finally` executa independente de sucesso ou erro. Aqui, garante que o cursor
de "carregando" (`cursor='wait'`) sempre seja restaurado ao normal, mesmo que a exportação
falhe.

### Capturando múltiplas exceções com uma tupla

```python
elif col == 'Quantidade':
    try:
        int_val = int(valor)
        valores.append(str(int_val) if valor == int_val else str(valor))
    except (ValueError, OverflowError):
        valores.append(str(valor))
```

`except (TipoA, TipoB):` captura qualquer um dos tipos listados — a tupla agrupa exceções
sem precisar duplicar o bloco `except`.

Por que `OverflowError` aqui? `int(float('inf'))` levanta `OverflowError` — e DataFrames
podem conter `float('inf')` em colunas numéricas quando há divisão por zero ou importação
de dados inconsistentes. Sem proteger contra isso, a tabela travaria ao tentar renderizar
uma linha com infinito.

### Protegendo contra `NaT` em operações de data

```python
dt_min = df['Data Emissao'].min()
dt_max = df['Data Emissao'].max()
data_inicio_str = dt_min.strftime('%d/%m/%Y') if pd.notna(dt_min) else 'N/D'
data_fim_str    = dt_max.strftime('%d/%m/%Y') if pd.notna(dt_max) else 'N/D'
```

`NaT` (Not a Time) é o equivalente de `NaN` para datas no Pandas. Se uma coluna de datas
tiver todos os valores nulos, `.min()` e `.max()` retornam `NaT`. Chamar `.strftime()`
em `NaT` lança `ValueError`.

`pd.notna(valor)` retorna `True` para qualquer valor que não seja `None`, `NaN` ou `NaT`.
É mais seguro que `valor is not None` porque cobre os casos específicos do Pandas.

### Validando entrada antes de processar

```python
arquivo = self.arquivo_entry.get().strip()
if not arquivo:
    Toast.show(self.root, "Selecione um arquivo Excel primeiro", tipo='warning')
    return
if os.path.splitext(arquivo)[1].lower() not in ('.xlsx', '.xls'):
    Toast.show(self.root, "Selecione um arquivo Excel válido (.xlsx ou .xls)", tipo='warning')
    return
if not os.path.isfile(arquivo):
    Toast.show(self.root, f"Arquivo não encontrado: {os.path.basename(arquivo)}", tipo='error')
    return
```

Validar a entrada *antes* de processar é mais limpo que capturar exceções depois. Aqui, três
verificações bloqueiam caminhos inválidos cedo:

1. Campo vazio — o usuário não selecionou nada
2. Extensão errada — alguém pode ter digitado o caminho manualmente
3. Arquivo não existe — o arquivo foi movido ou deletado após ser selecionado

`os.path.splitext(arquivo)` retorna `(nome_sem_extensao, extensao)`. Verificar a extensão
não garante que o conteúdo é válido, mas filtra erros óbvios antes mesmo de tentar abrir
o arquivo com openpyxl.

### Por que não usar `except Exception` para tudo?

Usar apenas `except Exception` é válido como último recurso, mas capturar exceções específicas
te permite:
- Dar mensagens de erro mais úteis ao usuário
- Tomar ações diferentes para cada tipo de erro
- Deixar claro no código quais erros você espera que possam ocorrer

---

## 15. Padrões avançados usados no Rubi

### Pipeline de filtros — separação de responsabilidades

```python
# Linhas 1047-1084 do main.py
def _refresh_tabela_dados(self):
    """Pipeline unificado: aplica todos os filtros e atualiza a tabela da aba Dados."""
    if self.df_filtrado is None:
        return

    # 1. Filtro de status (fixo — status administrativos excluídos)
    status_excluir = ['EM APROVAÇÃO', 'PRE-REQUISIÇÃO GERADA']
    df = self.df_filtrado[~self.df_filtrado['Status'].isin(status_excluir)].copy()

    # 2. Filtros do usuário (armazém, setor, solicitante)
    armazem = self.filtro_armazem_var.get()
    if armazem != "Todos":
        df = df[df['Armazem'].astype(str) == armazem]

    # 3. Busca textual
    termo = self.search_var.get().strip().lower()
    if termo:
        df = df[df['Descricao'].str.lower().str.contains(termo, na=False) | ...]

    # 4. Atualizar UI
    self.atualizar_tabela(df)
```

Antes do pipeline, cada filtro era aplicado separadamente em pontos diferentes do código.
O pipeline centraliza todos os filtros em um único lugar: qualquer filtro que mudar
chama `_refresh_tabela_dados()`, que reaplica tudo do zero.

Essa é a diferença entre código que *funciona* e código que é *manutenível*.

### Debounce — evitando chamadas em excesso

```python
# Linhas 1017-1021 do main.py
def _on_resize_dados(self, _event):
    """Debounce: agenda salvamento das larguras da tabela Dados."""
    if self._save_widths_job_dados:
        self.root.after_cancel(self._save_widths_job_dados)
    self._save_widths_job_dados = self.root.after(500, self._salvar_larguras_dados)
```

**Debounce** é uma técnica que limita a frequência de execução de uma função.

O problema: quando o usuário arrasta o separador de coluna, o evento `ButtonRelease-1`
dispara dezenas de vezes. Salvar o config.json dezenas de vezes por segundo é desnecessário
e pode causar lentidão.

A solução:
1. Ao receber o evento, cancelar qualquer salvamento pendente
2. Agendar um novo salvamento para daqui a 500ms
3. Se o evento disparar novamente antes dos 500ms, cancela e reagenda
4. O salvamento só acontece 500ms após o *último* evento

`root.after(ms, func)` — agenda execução de `func` após `ms` milissegundos, retorna um ID
`root.after_cancel(id)` — cancela um agendamento pendente

### Lazy import — importar quando precisar

```python
# Linha 2322 do main.py
def exportar_pdf(self):
    try:
        from fpdf import FPDF
    except ImportError:
        Toast.show(self.root, "Dependência ausente. Execute: pip install fpdf2", tipo='error')
        return
```

Em vez de importar `fpdf` no topo do arquivo, o Rubi importa apenas quando o usuário
clica em "Exportar PDF". Vantagens:
- Se `fpdf2` não estiver instalado, a aplicação inicia normalmente (erro só ao tentar usar)
- O tempo de inicialização é menor (uma biblioteca a menos para carregar)
- A mensagem de erro é acionável: diz exatamente o que fazer

### Geração de arquivos temporários

```python
import tempfile
tmp = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
fig.savefig(tmp.name, dpi=150, bbox_inches='tight')
plt.close(fig)
tmp.close()
figuras.append(("Top 10 Setores", tmp.name))
```

Para incluir gráficos no PDF, o Rubi precisa salvá-los como imagens. Usa-se `tempfile`
para criar arquivos temporários — o sistema operacional sabe onde colocá-los e você
não precisa gerenciar o caminho.

`delete=False` é necessário porque o arquivo precisa existir depois que você fechar.
O Rubi limpa os temporários no bloco `finally`:

```python
finally:
    for _, path in temp_files:
        try:
            os.remove(path)
        except Exception:
            pass
```

### Acumulador mutável como parâmetro

```python
def _gerar_figuras_pdf(self, figuras: list):
    def _salvar_fig(fig, titulo):
        tmp = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
        fig.savefig(tmp.name, dpi=150, bbox_inches='tight')
        plt.close(fig)
        tmp.close()
        figuras.append((titulo, tmp.name))  # modifica a lista do chamador
    
    _salvar_fig(criar_grafico_setores(), "Top 10 Setores")
    _salvar_fig(criar_grafico_materiais(), "Top 10 Materiais")
    # ...

# No chamador:
temp_files = []
self._gerar_figuras_pdf(temp_files)
# temp_files agora contém todos os PNGs gerados
```

Em Python, listas são passadas **por referência** — o método não precisa retornar nada,
ele modifica a lista que recebeu. Esse padrão é chamado de *acumulador mutável*.

Por que não retornar a lista? Porque `temp_files` precisa existir *antes* da chamada para
poder ser passado ao bloco `finally`, que limpa os temporários mesmo que `_gerar_figuras_pdf`
lance uma exceção no meio do processo.

```python
temp_files = []        # criado antes do try
try:
    self._gerar_figuras_pdf(temp_files)
    # ... geração do PDF usando temp_files
finally:
    for _, path in temp_files:
        try:
            os.remove(path)
        except Exception:
            pass
```

Se a função retornasse a lista (`temp_files = self._gerar_figuras_pdf()`), qualquer
exceção antes do `return` deixaria os arquivos temporários em disco — vazamento de recurso.
Com o acumulador, cada PNG adicionado à lista já está "registrado para limpeza".

---

## 16. Exportação de dados — Excel, TXT e PDF

### Excel com Pandas

```python
# Linhas 2139-2143 do main.py
df_export = self.df_filtrado.copy()
df_export['Data Emissao'] = df_export['Data Emissao'].dt.strftime('%d/%m/%Y')
df_export.to_excel(filename, index=False, sheet_name='Solicitações')
```

`df.to_excel(path, index=False)` — salva DataFrame como Excel.
`index=False` — não inclui o índice numérico do DataFrame como coluna extra.
Antes de exportar, converte a coluna de data para string formatada — Excel receberia
um timestamp interno que não ficaria legível.

### TXT simples

```python
# Linhas 2289-2290 do main.py
with open(filename, 'w', encoding='utf-8') as f:
    f.write(self.resumo_text.get('1.0', tk.END))
```

`'1.0'` no Tkinter significa "linha 1, caractere 0" (início do texto).
`tk.END` é o fim do texto.
`get('1.0', tk.END)` retorna todo o conteúdo do widget Text como string.

### PDF com fpdf2

```python
# Linhas 2381-2397 do main.py
pdf = FPDF()
pdf.set_auto_page_break(auto=True, margin=15)
pdf.add_font("Quicksand", style="",  fname=font_regular)
pdf.add_font("Quicksand", style="B", fname=font_bold)

pdf.add_page()

pdf.set_fill_color(220, 20, 60)    # cor de fundo RGB
pdf.rect(0, 0, 210, 30, 'F')      # retângulo preenchido (cabeçalho carmesim)

pdf.set_xy(15, 7)                  # posicionar cursor
pdf.set_text_color(255, 255, 255)  # cor branca
pdf.set_font("Quicksand", "B", 17)
pdf.cell(0, 9, "RUBI - Sistema...", ln=True)

pdf.output(filename)
```

O fpdf2 é uma biblioteca de geração de PDF de baixo nível — você posiciona cada elemento
manualmente em milímetros numa página A4 (210mm × 297mm).

`pdf.cell(largura, altura, texto)` — cria uma célula com texto
`pdf.rect(x, y, w, h, 'F')` — retângulo preenchido ('F' = fill)
`pdf.image(path, x=x, w=largura)` — insere imagem PNG

---

## 17. Como montar um projeto assim do zero

Esta é a pergunta mais importante: por onde começar?

### Fase 1 — Entender o problema (1-2 dias)

Antes de código:
1. Qual dado de entrada? (Excel, banco de dados, CSV, API?)
2. Qual dado de saída? (tabela, gráfico, relatório, exportação?)
3. Quem usa? (técnico ou não técnico — determina a interface)
4. Que plataforma? (web, desktop, linha de comando?)

Para o Rubi: entrada = Excel, saída = tabelas + gráficos + PDF, usuário não técnico,
plataforma desktop Windows.

### Fase 2 — Escolher a stack (meio dia)

Com base nas respostas:
- Desktop Python + análise de dados → Tkinter + Pandas + Matplotlib
- Precisa de aparência moderna → CustomTkinter
- Exportação de relatórios → fpdf2, openpyxl

Anote as dependências no `requirements.txt` imediatamente.

### Fase 3 — Criar o esqueleto (1 dia)

Comece com o mínimo que abre e fecha sem erros:

```python
import tkinter as tk
import customtkinter as ctk

class MinhaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Minha Aplicação")
        self.root.geometry("1200x700")
        self.criar_interface()
    
    def criar_interface(self):
        label = tk.Label(self.root, text="Olá, mundo!")
        label.pack(pady=50)

if __name__ == "__main__":
    root = ctk.CTk()
    app = MinhaApp(root)
    root.mainloop()
```

Isso é a base. A partir daqui você adiciona uma coisa de cada vez.

### Fase 4 — Implementar feature por feature

Ordem recomendada para um sistema como o Rubi:

**1. Carregamento de dados**
```python
def carregar_dados(self):
    arquivo = "dados.xlsx"
    df = pd.read_excel(arquivo)
    print(df.head())  # confirmar que leu certo
```

**2. Exibição em tabela**
```python
def montar_tabela(self, df):
    self.tree['columns'] = list(df.columns)
    for col in df.columns:
        self.tree.heading(col, text=col)
        self.tree.column(col, width=100)
    for _, row in df.iterrows():
        self.tree.insert('', 'end', values=list(row))
```

**3. Filtros básicos**
```python
def filtrar(self):
    termo = self.search_var.get()
    df_filtrado = self.df[self.df['Nome'].str.contains(termo, na=False)]
    self.montar_tabela(df_filtrado)
```

**4. Gráficos**
```python
def criar_grafico(self, parent):
    fig = Figure(figsize=(8, 5))
    ax = fig.add_subplot(111)
    dados = self.df['Categoria'].value_counts()
    ax.bar(dados.index, dados.values)
    FigureCanvasTkAgg(fig, parent).get_tk_widget().pack()
```

**5. Exportações, cache, configurações** — deixe para o final

### Fase 5 — Polimento e UX

Só depois que tudo funciona:
- Notificações amigáveis (Toast)
- Progress bar durante carregamento
- Mensagens de erro claras
- Atalhos de teclado
- Salvar preferências do usuário

### Fase 6 — Empacotar para distribuição

```bash
# Instalar PyInstaller
pip install pyinstaller

# Criar executável
pyinstaller --onefile --windowed main.py
```

O executável gerado em `dist/` roda sem precisar de Python instalado.

### Onde começo? Onde termino?

**Começo:** na pergunta "o que o usuário consegue fazer com isso?". A primeira feature
deve ser a mais importante. No Rubi: carregar um Excel e ver os dados na tela. Tudo mais
é incremento.

**Termino:** quando o produto resolve o problema para o qual foi criado. Um sistema que
funciona sem bugs e que o usuário consegue usar sem ajuda está pronto. Funcionalidades
extras podem sempre ser adicionadas depois.

---

## 18. Mapa mental do Rubi

```
main.py
│
├── Imports (linhas 0-14)
│   └── tkinter, pandas, matplotlib, customtkinter, etc.
│
├── class Toast (linhas 17-87)
│   └── @staticmethod show() — notificações flutuantes
│
├── def _registrar_fontes() (linhas 90-106)
│   └── API GDI32 do Windows para registrar fontes TTF
│
├── class SolicitacoesAppPro (linhas 108-2604)
│   │
│   ├── __init__ — configuração inicial e estado da aplicação
│   ├── criar_interface — monta toda a UI
│   │
│   ├── Construtores de abas
│   │   ├── criar_aba_dados — tabela de solicitações pendentes
│   │   ├── criar_aba_status_atendimento — tabela com KPIs de atendimento
│   │   ├── criar_aba_dashboard — KPIs + gráficos gerais
│   │   ├── criar_aba_analise — gráficos detalhados
│   │   └── criar_aba_resumo — relatório textual + sidebar
│   │
│   ├── Sistema de filtros
│   │   ├── _popular_combos_dados / _popular_combos_status
│   │   ├── _refresh_tabela_dados — pipeline de filtros da aba Dados
│   │   ├── _refresh_tabela_status — pipeline de filtros da aba Status
│   │   ├── _limpar_filtros_dados / _limpar_filtros_status
│   │   ├── aplicar_filtro_data — filtro global por data de emissão
│   │   ├── aplicar_atalho_data — atalhos Hoje / Semana / Mês
│   │   └── limpar_filtro — remove filtro de data
│   │
│   ├── Carregamento de dados
│   │   ├── selecionar_arquivo — diálogo de abertura
│   │   ├── carregar_dados — lê Excel ou cache, dispara atualização de UI
│   │   ├── atualizar_tabela — popula Treeview da aba Dados
│   │   └── atualizar_tabela_status — popula Treeview da aba Status
│   │
│   ├── Atualizadores de seções
│   │   ├── atualizar_dashboard — KPIs + gráficos
│   │   ├── atualizar_analise — gráfico por dia da semana
│   │   ├── atualizar_resumo — texto do resumo executivo
│   │   └── _atualizar_resumo_sidebar — cards laterais do resumo
│   │
│   ├── Gráficos
│   │   ├── criar_kpi_card — card colorido de KPI
│   │   ├── criar_grafico_top_setores — barras horizontais
│   │   ├── criar_grafico_top_solicitantes — barras horizontais
│   │   └── criar_grafico_dias_semana — barras verticais
│   │
│   ├── Sistema de cache
│   │   ├── gerar_hash_arquivo — MD5 para detectar mudanças no Excel
│   │   ├── obter_cache_path — caminho base (hash MD5 do path do arquivo)
│   │   ├── carregar_do_cache — lê .json (metadata) + .parquet (DataFrames)
│   │   ├── salvar_no_cache — grava .parquet + .json com hash e timestamp
│   │   └── limpar_cache — remove arquivos .parquet e .json do cache
│   │
│   ├── Configurações
│   │   ├── carregar_config — lê config.json com validação defensiva de tipos
│   │   └── salvar_config — grava config.json
│   │
│   ├── Persistência de larguras de colunas
│   │   ├── _on_resize_dados / _on_resize_status — evento de redimensionamento
│   │   └── _salvar_larguras_dados / _salvar_larguras_status — grava no config
│   │
│   └── Exportações
│       ├── exportar_excel — DataFrame → .xlsx
│       ├── exportar_status_excel — DataFrame status → .xlsx
│       ├── exportar_resumo — conteúdo do Text → .txt
│       ├── exportar_pdf — relatório completo → .pdf
│       ├── _pdf_rodape — rodapé com número de página
│       └── _gerar_figuras_pdf — matplotlib → PNG temporários
│
└── if __name__ == "__main__"
    └── inicialização: fontes → ctk config → root → app → mainloop
```

---

## Conceitos Python por nível

### Básico (entender antes de mexer no Rubi)
- Variáveis e tipos (int, str, float, bool, None)
- Condicionais (if/elif/else)
- Laços (for, while)
- Listas, dicionários, tuplas
- Funções com parâmetros e retorno
- Abertura e leitura de arquivos

### Intermediário (o que você vê no Rubi)
- Classes e objetos (`__init__`, `self`, métodos)
- Herança (o CustomTkinter usa extensivamente)
- Tratamento de erros (`try/except/finally`)
- List comprehensions
- Funções aninhadas e closures
- `with` (gerenciadores de contexto)
- Módulos e imports
- Variáveis com valor padrão

### Avançado (o que torna o Rubi robusto)
- Método estático (`@staticmethod`)
- `lambda` e funções como argumentos
- `iter()` e iteradores customizados
- Serialização com parquet (`pyarrow`) — seguro e interoperável
- Hashing com `hashlib` (MD5 para detectar mudanças em arquivos)
- Chamadas de API do sistema operacional com `ctypes`
- Lazy imports (importar dentro de funções)
- Padrões de design: pipeline, debounce, observer (trace)
- Empacotamento com PyInstaller
- NumPy `select` para derivação condicional de colunas em DataFrames
- Acumulador mutável como parâmetro (padrão try/finally seguro)
- Validação defensiva de entrada e tipos (`isinstance`, `os.path.splitext`)
- Caminhos portáveis com `%APPDATA%` para aplicações desktop Windows

---

*Documento gerado para o projeto Rubi — DBSolutions Lab © 2026*
*Baseado em `main.py` — versão 2.3 (auditoria de segurança aplicada)*
