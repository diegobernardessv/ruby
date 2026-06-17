# Manual do Usuário — Rubi ♦
### Sistema de Controle de Solicitações ao Armazém

**Versão 2.3 | DBSolutions Lab**

---

## Sumário

1. [O que é o Rubi?](#1-o-que-é-o-rubi)
2. [Abrindo o programa](#2-abrindo-o-programa)
3. [Carregando os dados](#3-carregando-os-dados)
4. [Filtrando por período](#4-filtrando-por-período)
5. [Aba: Solicitações Pendentes](#5-aba-solicitações-pendentes)
6. [Aba: Status de Atendimento](#6-aba-status-de-atendimento)
7. [Aba: Dashboard](#7-aba-dashboard)
8. [Aba: Análise Detalhada](#8-aba-análise-detalhada)
9. [Aba: Resumo Executivo](#9-aba-resumo-executivo)
10. [Exportando relatórios](#10-exportando-relatórios)
11. [Dicas rápidas e perguntas frequentes](#11-dicas-rápidas-e-perguntas-frequentes)

---

## 1. O que é o Rubi?

O **Rubi** é um sistema desenvolvido especialmente para facilitar o controle e a análise das solicitações feitas ao armazém. Em vez de abrir planilhas enormes no Excel e tentar entender os números sozinho, o Rubi faz todo esse trabalho por você.

Com ele você consegue:

- Ver todas as solicitações em uma tabela organizada e fácil de navegar
- Saber o status de atendimento de cada pedido (atendido, parcial, não atendido)
- Visualizar gráficos e números prontos sobre setores, solicitantes e materiais
- Filtrar informações por data, setor, armazém ou solicitante com poucos cliques
- Gerar relatórios completos em Excel, TXT ou PDF para compartilhar com gestores

O Rubi é o seu painel de controle do almoxarifado.

---

## 2. Abrindo o programa

Clique duas vezes no arquivo **Rubi.exe** (ou no atalho na área de trabalho). A janela do programa vai abrir automaticamente.

Você vai ver a tela principal com:

- Um **cabeçalho escuro** com o nome "♦ Rubi" em carmesim no topo
- Um **painel de controle** com campos para carregar o arquivo e filtrar por data
- As **cinco abas** com as diferentes visões dos dados (elas aparecem assim que você carregar a planilha)

> **Dica:** O Rubi lembra o último arquivo que você usou. Na próxima vez que abrir o programa, o nome do arquivo já vai estar preenchido automaticamente.

---

## 3. Carregando os dados

Antes de ver qualquer informação, você precisa indicar ao Rubi qual planilha Excel ele deve ler.

### Passo a passo:

**1. Localize o campo "Arquivo"** no painel de controle (logo abaixo do cabeçalho escuro).

**2. Clique no botão "Procurar..."** (carmesim, ao lado do campo de arquivo).
   - Uma janela vai abrir para você navegar pelas pastas do computador.
   - Selecione a planilha Excel do sistema (arquivo `.xlsx` ou `.xls`) e clique em **Abrir**.

**3. Clique no botão verde "🔄 Carregar Dados"**.
   - O Rubi vai ler o arquivo e processar as informações.
   - Uma barra de progresso vai aparecer enquanto os dados são carregados.
   - Quando terminar, uma notificação verde vai aparecer no canto da tela confirmando o sucesso.

Pronto. Todas as abas serão atualizadas automaticamente com os dados da planilha.

> **Nota sobre velocidade:** O Rubi possui um sistema de cache inteligente. Se você carregar o mesmo arquivo duas vezes sem alterá-lo, a segunda carga será quase instantânea, pois os dados já estão em memória.

---

## 4. Filtrando por período

O painel de controle tem um filtro de data que funciona em todas as abas ao mesmo tempo. Isso significa que ao aplicar um filtro, a tabela de solicitações, o dashboard, a análise e o resumo executivo — tudo é atualizado para mostrar apenas o período escolhido.

### Como definir o período:

No campo **"De:"**, clique no calendário e escolha a data de início.
No campo **"Até:"**, escolha a data de fim.

Depois clique em **"🔍 Aplicar Filtro"**.

### Atalhos de data rápidos

Em vez de selecionar as datas manualmente, você pode usar os botões de atalho:

| Botão | O que faz |
|-------|-----------|
| **Hoje** | Mostra apenas as solicitações do dia de hoje |
| **Semana** | Mostra as solicitações dos últimos 7 dias |
| **Mês** | Mostra as solicitações do mês atual |

### Removendo o filtro de data:

Clique no botão **"🔄 Limpar Filtro"** (cinza). O sistema volta a mostrar todos os dados da planilha.

> **Atenção:** O filtro de data é global — ele afeta todas as abas ao mesmo tempo. Os filtros internos de cada aba (por setor, armazém etc.) funcionam de forma independente dentro do período já filtrado.

---

## 5. Aba: Solicitações Pendentes

Esta é a primeira aba e a mais usada no dia a dia. Ela mostra uma tabela completa com todas as solicitações ao armazém.

### O que você vê nesta aba:

- Uma tabela com colunas como: Número da SA, Código, Descrição, Quantidade, Data de Emissão, Setor, Solicitante, Armazém e Observação.
- Um contador no topo informando quantas linhas estão sendo exibidas.
- Um badge colorido quando algum filtro está ativo.

### Campo de busca rápida

Na parte superior da aba há um campo de busca. É como o Ctrl+F que você usa para procurar palavras em documentos.

Basta digitar qualquer coisa — parte do nome de um material, o nome de um setor, o nome de um solicitante ou um código — e a tabela vai filtrar automaticamente, em tempo real, sem precisar clicar em nada.

> Exemplo: Digite "luva" e a tabela vai mostrar apenas as solicitações que contenham a palavra "luva" na descrição.

### Filtros avançados

Abaixo do campo de busca há um painel com três filtros adicionais que podem ser combinados entre si:

| Filtro | Para que serve |
|--------|---------------|
| **Armazém** | Filtra as solicitações de um armazém específico |
| **Setor** | Filtra as solicitações de um setor específico |
| **Solicitante** | Filtra as solicitações de uma pessoa específica |

Os menus de cada filtro são preenchidos automaticamente com os valores que existem na planilha. Para remover um filtro individual, selecione a opção **"Todos"** no menu correspondente.

### Ajustando as colunas

As colunas da tabela podem ser redimensionadas arrastando as bordas entre os cabeçalhos. O Rubi salva automaticamente a largura que você definiu para a próxima vez que abrir o programa.

### Exportando esta tabela

No canto superior direito da aba há o botão **"💾 Exportar para Excel"**. Ele gera um arquivo `.xlsx` com exatamente os dados que estão sendo exibidos na tabela no momento — ou seja, com todos os filtros aplicados.

---

## 6. Aba: Status de Atendimento

Esta aba mostra a situação de cada solicitação: se ela foi completamente atendida, parcialmente atendida ou ainda não foi atendida pelo almoxarifado.

### Os três badges de KPI

No topo da aba há três indicadores coloridos que mostram o total de cada status:

- **Verde — Totalmente Atendida:** A quantidade entregue foi igual à quantidade solicitada.
- **Laranja — Parcialmente Atendida:** Uma parte da quantidade foi entregue, mas ainda falta o restante.
- **Vermelho — Não Atendida:** Ainda não houve nenhuma entrega para essa solicitação.

Esses números são atualizados automaticamente de acordo com os filtros que você aplicar.

### Filtrando por status de atendimento

Há um filtro específico para você ver apenas um tipo de situação. Por exemplo, para ver apenas as solicitações que ainda não foram atendidas, selecione **"NÃO ATENDIDA"** no filtro de status.

### Filtros avançados e busca

Da mesma forma que na aba anterior, você pode combinar o filtro de status com os filtros de **Armazém**, **Setor** e **Solicitante**, além de usar o campo de busca para localizar itens específicos.

### Exportando

O botão **"💾 Exportar para Excel"** no canto superior direito exporta exatamente o que está visível na tabela, com todos os filtros aplicados.

---

## 7. Aba: Dashboard

O Dashboard é a visão gerencial do Rubi. Ele transforma os números da planilha em indicadores e gráficos prontos, sem precisar de nenhuma configuração.

### Os 5 cartões de KPI

No topo do Dashboard você encontra cinco cartões coloridos com os principais indicadores do período selecionado:

| Indicador | O que significa |
|-----------|----------------|
| **Total de Solicitações** | Número de SAs únicas no período |
| **Total de Itens** | Número de linhas/materiais solicitados |
| **Setores Ativos** | Quantos setores diferentes fizeram pedidos |
| **Solicitantes** | Quantas pessoas diferentes fizeram pedidos |
| **Média Itens/SA** | Média de materiais por solicitação |

### Os gráficos

Abaixo dos KPIs, o Dashboard exibe dois gráficos lado a lado:

**Top 10 Setores** — Um gráfico de barras horizontais mostrando os dez setores que mais fizeram solicitações. As barras permitem comparar rapidamente qual setor demanda mais do almoxarifado.

**Top 10 Solicitantes** — O mesmo conceito, mas focado nas pessoas. Mostra quem mais fez pedidos no período.

> **Dica:** Se você aplicar um filtro de data ou de setor, o Dashboard atualiza todos os cartões e gráficos automaticamente para refletir o período filtrado.

Se o conteúdo não couber na tela, use a barra de rolagem lateral direita para descer e ver o restante.

---

## 8. Aba: Análise Detalhada

A Análise Detalhada vai além dos números principais e mostra o comportamento das solicitações ao longo do tempo.

### O gráfico de Distribuição por Dia da Semana

Este gráfico de barras verticais em roxo responde à pergunta: **"Em que dia da semana o almoxarifado recebe mais pedidos?"**

O eixo horizontal mostra os dias da semana (de segunda a domingo) e o eixo vertical mostra o número de SAs únicas emitidas em cada dia.

Isso é útil para identificar padrões, como por exemplo se as segundas-feiras costumam ter pico de solicitações, e planejar melhor a operação da semana.

---

## 9. Aba: Resumo Executivo

O Resumo Executivo é um relatório formatado e pronto para ser compartilhado com gestores, diretores ou outros departamentos. Ele consolida as principais informações em texto estruturado.

### O que o relatório contém:

- **Período analisado:** datas de início e fim, e quantidade de dias úteis no período
- **Estatísticas gerais:** total de SAs, total de itens, setores ativos, número de solicitantes
- **Top 5 Setores:** os cinco setores com mais itens solicitados, em ordem
- **Top 5 Solicitantes:** as cinco pessoas que mais fizeram pedidos
- **Top 10 Materiais:** os dez materiais mais solicitados no período
- **Lista completa de SAs:** todos os números de solicitação únicos do período

O relatório é atualizado automaticamente toda vez que você muda o período ou os filtros.

### Painel de KPIs lateral

À direita do texto há um painel visual com os principais números em destaque, complementando o relatório com uma visão rápida.

---

## 10. Exportando relatórios

O Rubi permite exportar os dados em três formatos diferentes.

---

### Exportar para Excel (.xlsx)

Disponível nas abas **Solicitações Pendentes** e **Status de Atendimento**.

Clique no botão **"💾 Exportar para Excel"** em qualquer uma dessas abas.
Uma janela vai abrir para você escolher onde salvar o arquivo e o nome.
O arquivo gerado contém exatamente os dados que estão visíveis na tabela no momento.

**Quando usar:** Quando precisar compartilhar os dados brutos com alguém ou fazer análises adicionais no Excel.

---

### Exportar Resumo em TXT

Disponível na aba **Resumo Executivo**.

Clique no botão **"Exportar Resumo (TXT)"**.
Escolha onde salvar e o nome do arquivo.
O arquivo `.txt` gerado contém o mesmo texto exibido na tela, formatado para leitura.

**Quando usar:** Para enviar o resumo por e-mail como texto simples ou para arquivar o relatório do período.

---

### Exportar Relatório em PDF

Disponível na aba **Resumo Executivo**.

Clique no botão **"Exportar Relatório (PDF)"**.
Escolha onde salvar.
O PDF gerado contém:
- Cabeçalho com a identidade visual do Rubi (carmesim e grafite)
- KPIs do período
- Top setores, solicitantes e materiais
- Gráficos integrados

**Quando usar:** Para apresentações formais, reuniões de gestão ou para imprimir o relatório do período.

> **Atenção:** A geração do PDF pode levar alguns segundos pois os gráficos são renderizados durante o processo. Uma notificação vai aparecer quando estiver pronto.

---

## 11. Dicas rápidas e perguntas frequentes

**Cliquei em "Carregar Dados" mas apareceu uma mensagem de erro.**
Verifique se:
- O arquivo Excel que você selecionou ainda existe no caminho indicado (ele não foi movido ou excluído).
- O arquivo não está aberto no Excel ao mesmo tempo. Feche o Excel e tente novamente.
- O arquivo é uma planilha `.xlsx` ou `.xls` — o Rubi não aceita outros formatos.

---

**A tabela está mostrando poucos dados ou nenhum dado.**
Pode ser que um filtro esteja ativo. Verifique:
- O filtro de data no painel de controle: clique em **"🔄 Limpar Filtro"** para remover.
- Os filtros de Armazém, Setor e Solicitante na aba: selecione **"Todos"** em cada um.
- O campo de busca: apague o texto digitado.

---

**Posso deixar o Rubi aberto e atualizar os dados sem fechar?**
Sim. Basta clicar em **"🔄 Carregar Dados"** novamente. Se o arquivo Excel foi modificado desde o último carregamento, o Rubi vai detectar a mudança e recarregar automaticamente. Se o arquivo não mudou, a carga será instantânea usando o cache.

---

**Como exporto apenas os dados de um setor específico?**
1. Na aba **Solicitações Pendentes**, selecione o setor desejado no filtro **"Setor"**.
2. A tabela vai filtrar automaticamente.
3. Clique em **"💾 Exportar para Excel"**.
O arquivo gerado vai conter apenas os dados daquele setor.

---

*Manual produzido pela DBSolutions Lab — Diego Bernardes*
*Sistema Rubi v2.3*
