# Claude Agent Template — Yahiko Setup

Padrão de configuração do agente Yahiko para o projeto ControladorSA (Zeus).

## Estrutura

```
.claude/
  settings.json          # Hooks de workflow do projeto
  commands/              # Slash commands (/status, /sync, /feature, /deploy-check)
  skills/                # Skills auto-ativadas por contexto
    python-test/         # Testes Python com coverage
    feature-start/       # Iniciar feature (branch)
  agents/                # System prompts de subagentes especializados
    python-reviewer.md   # Revisor Python/Tkinter/Pandas
    test-writer.md       # Escritor de testes (pytest + unittest)
    security-auditor.md  # Auditor de segurança para app desktop Python
```

## Como usar em um novo projeto

1. Copie a pasta `.claude/` para a raiz do novo projeto
2. Adicione `.claude/` ao `.gitignore` do projeto
3. Edite `.claude/settings.json` com os hooks específicos do projeto (se necessário)
4. Personalize os commands com os caminhos e contexto reais do projeto
5. Personalize as skills com contexto do projeto (linguagem, estrutura, Trello IDs)

## Hooks globais (já configurados em ~/.claude/settings.json)

O guard script `~/.claude/hooks/pre_bash_guard.py` avisa automaticamente sobre:
- `git push --force`, `git commit --no-verify`, `git reset --hard`
- `DROP TABLE`, `DROP DATABASE`, `TRUNCATE TABLE sem WHERE`
- `rm -rf /` e variantes destrutivas
- `--no-verify`, `--skip-ci`

Comportamento: **warn-only** — avisa mas não bloqueia. Diego decide.

## Camadas da arquitetura

| Camada | Onde | O que faz |
|---|---|---|
| Memory | `CLAUDE.md` + `~/.claude/projects/*/memory/` | Contexto persistente entre sessões |
| Guardrails | `~/.claude/hooks/` | Avisos automáticos sobre comandos perigosos |
| Workflows | `.claude/skills/` | Automações repetitivas ativadas por contexto |
| Commands | `.claude/commands/` | Atalhos de slash command |
| Agents | `.claude/agents/` | Subagentes especializados por domínio |
