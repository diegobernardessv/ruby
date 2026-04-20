# Roadmap - Zeus: Sistema Elizeus de Controle de Solicitações

**Projeto:** ControladorSA  
**Empresa:** DBSolutions Lab  
**Responsável:** Diego Bernardes  
**Última atualização:** 20/04/2026

---

## Visão Geral

Sistema desktop para análise e controle de solicitações ao armazém, com interface gráfica profissional, dashboards interativos e exportação de relatórios.

**Objetivo:** Transformar dados brutos de solicitações em insights acionáveis para gestão de almoxarifado.

---

## Status Atual — v2.1 Enhanced Edition (Concluída)

### Concluído

#### v1.0 — MVP
- [x] Leitura de planilha Excel
- [x] Tabela de solicitações com filtro de datas
- [x] Exportação Excel

#### v2.0 PRO — Analytics Completo (Abril 2026)
- [x] Sistema de 5 abas especializadas com identidade visual única
- [x] Aba Solicitações Pendentes: tabela + filtros + exportação
- [x] Aba Status de Atendimento: KPIs com badges + filtros + busca + exportação
- [x] Aba Dashboard: 5 KPIs coloridos + 4 gráficos principais
- [x] Aba Análise Detalhada: 4 gráficos avançados
- [x] Aba Resumo Executivo: relatório formatado + exportação TXT
- [x] 8 gráficos com Matplotlib (top materiais, setores, tendências, distribuição)
- [x] Executável standalone via PyInstaller
- [x] Tipografia Quicksand empacotada

#### v2.1 Enhanced Edition (Abril 2026)
- [x] Sistema de configurações persistente (config.json)
- [x] Cache inteligente de dados (evita re-leitura desnecessária do Excel)
- [x] Notificações toast modernas (substituiu messageboxes)
- [x] Tratamento de erros com mensagens amigáveis
- [x] Badges coloridos 3D para KPIs de atendimento
- [x] Cores temáticas por aba (5 paletas distintas)
- [x] Botões maiores e mais acessíveis

---

## Próximas Versões

### v2.2 — Exportação Avançada (Próxima)

**Objetivo:** Permitir que Elizeus compartilhe os dados em qualquer formato.

**Prioridade: alta**

- [ ] Exportar PDF do Resumo Executivo (texto + KPIs)
- [ ] Exportar relatório PDF completo (todas as abas + gráficos)
- [ ] Exportar gráficos individualmente como PNG
- [ ] Branding Zeus no cabeçalho dos relatórios exportados

**Dependências:** `reportlab` ou `fpdf2` para PDF

---

### v2.3 — Filtros Avançados

**Objetivo:** Aumentar granularidade de análise sem complicar a interface.

**Prioridade: alta**

- [ ] Filtro por armazém específico
- [ ] Filtro por setor específico
- [ ] Filtro por solicitante específico
- [ ] Combinação simultânea de múltiplos filtros
- [ ] Filtro por faixa de quantidade (min/max)
- [ ] Limpar filtros individualmente

---

### v2.4 — UX e Gráficos Interativos

**Objetivo:** Tornar a exploração de dados mais intuitiva.

**Prioridade: média**

- [ ] Hover nos gráficos com tooltip mostrando valor exato
- [ ] Comparação de dois períodos lado a lado
- [ ] Cálculo de variação percentual entre períodos
- [ ] Loading spinner em operações longas (carregamento, exportação)
- [ ] Atalhos de teclado para ações comuns

---

### v3.0 — Metas e Alertas (Futuro)

**Objetivo:** Gestão proativa do almoxarifado.

**Prioridade: média**

- [ ] Configurar meta de SAs por período
- [ ] Alertas quando volume excede limites configurados
- [ ] Identificação automática de anomalias (picos incomuns)
- [ ] Histórico de alertas

---

### v4.0 — Previsão de Demanda (Futuro)

**Objetivo:** Antecipar necessidades com ML simples.

**Prioridade: baixa**

- [ ] Previsão de demanda por material (regressão simples)
- [ ] Identificação de padrões sazonais
- [ ] Sugestão de ponto de reposição
- [ ] Detecção de anomalias automática

**Dependências:** `scikit-learn` ou `statsmodels`

---

### v5.0 — Versão Web (Futuro)

**Objetivo:** Acesso remoto sem instalar o executável.

**Prioridade: baixa (alto esforço)**

- [ ] Backend Flask ou FastAPI
- [ ] Interface web responsiva
- [ ] Autenticação básica
- [ ] Multi-usuário com permissões

---

## Backlog de Ideias

- Integração com ERP
- Exportação para Google Sheets
- Notificações por email (picos de demanda)
- Clustering de setores por perfil de consumo

---

## Stack Tecnológica

### Atual
- Python 3.8+
- CustomTkinter (GUI)
- Pandas (análise de dados)
- Matplotlib (gráficos)
- tkcalendar (calendário)
- openpyxl (Excel)
- PyInstaller (executável)

### Planejado (v2.2+)
- reportlab ou fpdf2 (PDF)

### Futuro (v4.0+)
- Flask / FastAPI
- scikit-learn

---

## Histórico de Versões

| Versão | Data | Destaque |
|--------|------|----------|
| v2.1 Enhanced | Abr/2026 | Cache, toasts, badges 3D, cores temáticas |
| v2.0 PRO | Abr/2026 | 5 abas, 8 gráficos, PyInstaller |
| v1.0 MVP | — | Leitura Excel, tabela, filtro de datas |

---

**Próxima revisão:** Após conclusão da v2.2
