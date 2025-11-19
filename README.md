# 🔗 Merge Project Files

Ferramenta para mesclar múltiplos arquivos de código/configuração de um projeto em um único arquivo.

## 📋 Funcionalidades

- ✅ Percorre recursivamente diretórios do projeto
- ✅ Filtra por extensão de arquivo
- ✅ Filtra por prefixo de arquivo
- ✅ Exclui diretórios automaticamente (node_modules, __pycache__, etc)
- ✅ Gera árvore visual de diretórios
- ✅ Suporta configuração simples

## 🚀 Como Usar

1. **Configure** as variáveis na seção "CONFIGURAÇÕES":

```python
JUST_FILE_PREFIXES = ""                    # Filtrar por prefixo (vazio = sem filtro)
INCLUDED_EXTENSIONS = ('.rs', '.ts', '.py')  # Extensões a incluir
EXCLUDED_DIRS = {'node_modules', '__pycache__'}  # Diretórios a excluir
```

2. **Execute** o script:

```bash
python merge_files.py
```

3. **Pronto!** Arquivo `merged_output_<nome_projeto>.txt` gerado

## 📝 Exemplos de Configuração

```python
# Incluir TODOS os .rs e .ts
JUST_FILE_PREFIXES = ""
INCLUDED_EXTENSIONS = ('.rs', '.ts')

# Incluir APENAS arquivos que começam com "domain"
JUST_FILE_PREFIXES = "domain"
INCLUDED_EXTENSIONS = ('.rs', '.ts')

# Incluir múltiplos prefixos
JUST_FILE_PREFIXES = "domain,auth,config"
INCLUDED_EXTENSIONS = ('.rs', '.ts')
```

## 📂 Saída Gerada

O arquivo de saída contém:
1. Conteúdo de todos os arquivos encontrados (comentados)
2. Árvore visual do projeto

Perfeito para análise, compartilhamento com IA ou documentação.

## 📋 Requisitos

- Python 3.6+

## 📄 Licença

Livre para usar e modificar.
