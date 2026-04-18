# Fontes do Projeto

## Quicksand (Google Fonts)

**Fonte principal do projeto ControladorSA**

### Sobre a Fonte

- **Nome:** Quicksand
- **Designer:** Andrew Paglinawan
- **Licença:** Open Font License (OFL)
- **Fonte:** Google Fonts
- **Estilo:** Sans-serif geométrica moderna

### Características

- Design limpo e arredondado
- Excelente legibilidade em interfaces
- Suporte completo a caracteres latinos
- Múltiplos pesos disponíveis

### Arquivos Incluídos

| Arquivo | Peso | Uso |
|---------|------|-----|
| `Quicksand-Light.ttf` | 300 | Textos secundários |
| `Quicksand-Regular.ttf` | 400 | Texto padrão |
| `Quicksand-Medium.ttf` | 500 | Ênfase moderada |
| `Quicksand-SemiBold.ttf` | 600 | Subtítulos |
| `Quicksand-Bold.ttf` | 700 | Títulos e destaques |

### Uso no Código

```python
# Exemplo de uso
font=('Quicksand', 12, 'bold')  # Título
font=('Quicksand', 10)          # Texto normal
font=('Quicksand', 9)           # Texto pequeno
```

### Empacotamento

As fontes são automaticamente empacotadas no executável via PyInstaller e registradas no Windows através da função `_registrar_fontes()` em `interface_sa_pro.py`.

### Licença

```
Copyright 2011 The Quicksand Project Authors (https://github.com/andrew-paglinawan/QuicksandFamily)

This Font Software is licensed under the SIL Open Font License, Version 1.1.
This license is available with a FAQ at: http://scripts.sil.org/OFL
```

### Links

- [Google Fonts - Quicksand](https://fonts.google.com/specimen/Quicksand)
- [GitHub - Quicksand Family](https://github.com/andrew-paglinawan/QuicksandFamily)

---

**Última atualização:** 17/04/2026
