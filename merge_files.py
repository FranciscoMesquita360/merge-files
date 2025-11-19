#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔗 MERGE PROJECT FILES v1.8.0
================================================================================
Ferramenta para mesclar múltiplos arquivos de código/configuração de um projeto
em um único arquivo de saída, com filtros configuráveis.

📋 FUNCIONALIDADES:
  • Percorre recursivamente diretórios do projeto
  • Filtra por extensão de arquivo
  • Filtra por prefixo de arquivo
  • Filtra diretórios (como node_modules, __pycache__, etc)
  • Gera árvore de diretórios do projeto
  • Suporta strings simples para configuração

⚙️ COMO USAR:
  1. Configure as variáveis na seção "CONFIGURAÇÕES" abaixo
  2. Execute: python merge_files.py
  3. O arquivo "merged_output.txt" será gerado no mesmo diretório

📝 EXEMPLOS DE CONFIGURAÇÃO:

  # Incluir TODOS os arquivos .rs e .ts
  JUST_FILE_PREFIXES = ""
  INCLUDED_EXTENSIONS = ('.rs', '.ts')

  # Incluir APENAS arquivos que começam com "domain"
  JUST_FILE_PREFIXES = "domain"
  INCLUDED_EXTENSIONS = ('.rs', '.ts')

  # Incluir APENAS arquivos que começam com "domain" OU "auth" OU "config"
  JUST_FILE_PREFIXES = "domain,auth,config"
  INCLUDED_EXTENSIONS = ('.rs', '.ts')

  # Excluir certos diretórios da mesclagem
  EXCLUDED_DIRS = {'target', '.git', 'node_modules', 'build', '__pycache__'}

👨‍💻 AUTOR: Script criado para facilitar análise e compartilhamento de código
📅 ÚLTIMA ATUALIZAÇÃO: 2025/11/14
================================================================================
"""

import os
import sys

# ═══════════════════════════════════════════════════════════════════════════
# ⚙️ CONFIGURAÇÕES - CUSTOMIZE AQUI!
# ═══════════════════════════════════════════════════════════════════════════

# 📁 DIRETÓRIOS A EXCLUIR DA MESCLAGEM
# Estes diretórios NÃO serão percorridos/incluídos
EXCLUDED_DIRS = {
    'target',                  # Rust (compilação)
    '.git',                    # Git
    '.vscode',                 # VS Code config
    '__pycache__',             # Python cache
    'node_modules',            # Node.js dependencies
    'build',                   # Build output
    '.venv',                   # Python virtual env
    'windows-schema',          # Custom exclusão
    'gen',                     # Generated files
}

# 📄 PREFIXOS DE ARQUIVO A EXCLUIR DA MESCLAGEM
# Arquivos que começam com estes prefixos serão ignorados
EXCLUDED_FILE_PREFIXES = (
    'Insomnia',                # Arquivos Insomnia API
    'log',                     # Arquivos de log
    'merge_files',             # Este script
    'merged_output',           # Arquivo de saída anterior
    'Cargo.lock',              # Cargo lock
    'package-lock',            # npm lock
    'data',                    # Arquivos de dados
    'mod',                     # Módulos compilados
    'mock_bundle_registry',    # Mocks
    '.git'                     # Arquivos Git
)

# ✨ PREFIXOS PARA INCLUIR (FILTRO PRINCIPAL)
# Se vazio (""), inclui TODOS os arquivos com as extensões abaixo
# Se preenchido, inclui APENAS arquivos que começam com estes prefixos
#
# EXEMPLOS:
#   ""                         → Inclui tudo (sem filtro)
#   "domain"                   → Inclui apenas: domain.rs, domain_*.rs, etc
#   "domain,auth,config"       → Inclui: domain*, auth*, config*
JUST_FILE_PREFIXES = ""

# 📂 EXTENSÕES DE ARQUIVO A INCLUIR
# Apenas arquivos com estas extensões serão mesclados
INCLUDED_EXTENSIONS = (
    '.rs',                     # Rust
    '.ts',                     # TypeScript
    '.tsx',                    # TypeScript React
    '.css',                    # CSS
    '.json',                   # JSON
    '.toml',                   # TOML (Cargo.toml)
    '.html',                   # HTML
    '.py',                     # Python
    '.txt'                     # Text files
)

# ═══════════════════════════════════════════════════════════════════════════
# 🌳 CONFIGURAÇÕES DA ÁRVORE DE DIRETÓRIOS
# (Pode ser diferente das configurações de mesclagem se necessário)
# ═══════════════════════════════════════════════════════════════════════════

# 📁 DIRETÓRIOS A EXCLUIR DA ÁRVORE
EXCLUDED_DIRS_PRINT_TREE = {
    'target', '.git', '.vscode', '__pycache__', 
    'node_modules', 'build', '.venv', 'windows-schema', 'gen', 'icons'
}

# 📄 PREFIXOS DE ARQUIVO A EXCLUIR DA ÁRVORE
EXCLUDED_FILE_PREFIXES_PRINT_TREE = (
    'gitignore', 'package-lock', 'merge_files', 'merged_output',
    'README', 'tauri_studio_structure', 'Cargo.lock','.git'
)

# ✨ PREFIXOS PARA INCLUIR NA ÁRVORE
# (Deixe vazio para não aplicar filtro)
JUST_FILE_PREFIXES_PRINT_TREE = ""

# 📂 EXTENSÕES A INCLUIR NA ÁRVORE
# (Deixe vazio para incluir todas)
INCLUDED_EXTENSIONS_PRINT_TREE = (
    '.rs', '.ts', '.tsx', '.css', '.json', '.toml', '.html','.PY', '.txt'
)

# 💬 SÍMBOLO DE COMENTÁRIO (varia por linguagem)
# Usado para comentar o conteúdo do arquivo de saída
INLINE_COMMENT_SYMBOL = "//"

# 📝 DESCRIÇÃO DO PROJETO (opcional)
# Se preenchida, aparecerá no topo do arquivo de saída
PROJECT_DESCRIPTION = """"""

# ═══════════════════════════════════════════════════════════════════════════
# 🔧 FUNÇÕES AUXILIARES
# ═══════════════════════════════════════════════════════════════════════════

def _parse_prefixes(prefixes_input):
    """
    Converte diferentes formatos de entrada de prefixos para um set.
    
    Suporta:
      - String simples: "domain" → {"domain"}
      - String com múltiplos: "domain,auth,config" → {"domain", "auth", "config"}
      - Tupla: ("domain",) → {"domain"}
      - Vazio/None: "" ou None → None (sem filtro)
    
    Args:
        prefixes_input: str, tuple, list ou None
        
    Returns:
        set: Conjunto de prefixos, ou None se o filtro está desativado
        
    Examples:
        >>> _parse_prefixes("domain")
        {'domain'}
        >>> _parse_prefixes("domain,auth,config")
        {'domain', 'auth', 'config'}
        >>> _parse_prefixes("")
        None
    """
    if not prefixes_input:
        return None
    
    if isinstance(prefixes_input, str):
        # Remove espaços em branco e divide por vírgula
        prefixes = [p.strip() for p in prefixes_input.split(',') if p.strip()]
        return set(prefixes) if prefixes else None
    else:
        # Já é tupla/list
        return set(prefixes_input) if prefixes_input else None


def merge_project_files(directory, output_file):
    """
    Mescla múltiplos arquivos de código do projeto em um único arquivo.
    
    O arquivo de saída contém:
      1. Conteúdo de todos os arquivos encontrados (comentado)
      2. Árvore visual de diretórios do projeto
    
    Args:
        directory (str): Caminho do diretório raiz do projeto
        output_file (str): Caminho do arquivo de saída
        
    Returns:
        None (cria/escreve no arquivo_output)
    """
    
    output_filename = os.path.basename(output_file)
    script_filename = os.path.basename(__file__)
    
    print(f"🔍 Procurando arquivos em: {directory}")
    print(f"📝 Saída será salva em: {output_filename}\n")

    # ─────────────────────────────────────────────────────────────────────
    # FASE 1: Coleta de arquivos a mesclar
    # ─────────────────────────────────────────────────────────────────────
    found_files = []
    just_prefixes_set = _parse_prefixes(JUST_FILE_PREFIXES)
    
    for root, dirs, files in os.walk(directory, topdown=True):
        # Filtra diretórios (modifica 'dirs' in-place para evitar recursão)
        dirs[:] = [d for d in dirs if d not in EXCLUDED_DIRS]
        
        for file in files:
            # ✗ Exclui: script que está rodando, arquivo de saída anterior
            if file == script_filename or file == output_filename:
                continue
            
            # ✗ Exclui: arquivos com prefixos na lista de exclusão
            if file.startswith(EXCLUDED_FILE_PREFIXES):
                continue
            
            # ✗ Exclui: arquivos com extensões não autorizada
            if not file.endswith(INCLUDED_EXTENSIONS):
                continue
            
            # ✗ Exclui: se filtro JUST_FILE_PREFIXES está ativo, verifica prefixo
            if just_prefixes_set and not any(file.startswith(prefix) for prefix in just_prefixes_set):
                continue
            
            # ✅ Arquivo passou em todos os filtros
            full_path = os.path.join(root, file)
            found_files.append(full_path)
    
    found_files.sort()  # Ordena para saída consistente
    
    print(f"✅ Encontrados {len(found_files)} arquivos para mesclar\n")

    # ─────────────────────────────────────────────────────────────────────
    # FASE 2: Escreve arquivo de saída
    # ─────────────────────────────────────────────────────────────────────
    with open(output_file, 'w', encoding='utf-8') as outfile:
        
        # --- Adiciona descrição do projeto (se configurada) ---
        if PROJECT_DESCRIPTION:
            outfile.write(INLINE_COMMENT_SYMBOL + " PROJECT DESCRIPTION\n")
            outfile.write(INLINE_COMMENT_SYMBOL + "-" * 50 + "\n")
            for line in PROJECT_DESCRIPTION.strip().splitlines():
                outfile.write(INLINE_COMMENT_SYMBOL + " " + line + "\n")
            outfile.write("\n" + INLINE_COMMENT_SYMBOL + "=" * 50 + "\n\n\n")

        # --- Escreve conteúdo de cada arquivo ---
        for file_path in found_files:
            relative_path = os.path.relpath(file_path, directory)
            
            # Linha de separação com nome do arquivo
            outfile.write(INLINE_COMMENT_SYMBOL + "=" * 50 + "\n")
            outfile.write(INLINE_COMMENT_SYMBOL + relative_path + "\n")
            
            try:
                with open(file_path, 'r', encoding='utf-8') as infile:
                    outfile.write(infile.read())
            except Exception as e:
                # Se erro na leitura (ex: arquivo binário)
                outfile.write(INLINE_COMMENT_SYMBOL + f" [ERRO AO LER ARQUIVO: {e}]\n")
            
            outfile.write("\n\n")

        # ─────────────────────────────────────────────────────────────────
        # FASE 3: Árvore de diretórios
        # ─────────────────────────────────────────────────────────────────
        outfile.write(INLINE_COMMENT_SYMBOL + " PROJECT DIRECTORY TREE\n")
        outfile.write(INLINE_COMMENT_SYMBOL + "-" * 50 + "\n")
        
        tree = {}  # Dicionário aninhado para armazenar estrutura
        root_name = os.path.basename(os.path.abspath(directory))
        outfile.write(INLINE_COMMENT_SYMBOL + " " + root_name + "/\n")
        
        just_prefixes_set_print_tree = _parse_prefixes(JUST_FILE_PREFIXES_PRINT_TREE)
        
        # Constrói a estrutura de árvore "on-the-fly"
        for root, dirs, files in os.walk(directory, topdown=True):
            dirs[:] = [d for d in dirs if d not in EXCLUDED_DIRS_PRINT_TREE]
            
            # Encontra o nó "atual" na árvore
            relative_root = os.path.relpath(root, directory)
            current_node = tree
            if relative_root != ".":
                parts = relative_root.split(os.sep)
                for part in parts:
                    current_node = current_node.setdefault(part, {})
            
            # Adiciona subdiretórios como nós vazios
            for d in dirs:
                current_node.setdefault(d, {})
            
            # Adiciona arquivos que passam nos filtros da árvore
            for file in files:
                if file == script_filename or file == output_filename:
                    continue
                
                if file.startswith(EXCLUDED_FILE_PREFIXES_PRINT_TREE):
                    continue

                if INCLUDED_EXTENSIONS_PRINT_TREE and not file.endswith(INCLUDED_EXTENSIONS_PRINT_TREE):
                    continue
                
                if just_prefixes_set_print_tree and not any(file.startswith(prefix) for prefix in just_prefixes_set_print_tree):
                    continue
                
                current_node[file] = None

        # Função recursiva para imprimir árvore formatada
        def print_tree(node, prefix):
            """
            Imprime a árvore formatada com linhas visuais (├──, └──, │).
            
            Args:
                node (dict): Nó atual da árvore
                prefix (str): Prefixo de indentação para este nível
            """
            keys = sorted(node.keys())
            for i, key in enumerate(keys):
                is_last = i == (len(keys) - 1)
                connector = "└── " if is_last else "├── "
                
                is_directory = (node[key] is not None)
                
                if not is_directory:
                    # É arquivo: imprime nome direto
                    outfile.write(INLINE_COMMENT_SYMBOL + " " + prefix + connector + key + "\n")
                else:
                    # É diretório: imprime com "/" e recursa se não vazio
                    outfile.write(INLINE_COMMENT_SYMBOL + " " + prefix + connector + key + "/\n")
                    
                    if node[key] != {}:  # Se diretório não está vazio
                        next_prefix = prefix + ("    " if is_last else "│   ")
                        print_tree(node[key], next_prefix)

        print_tree(tree, "")
        outfile.write("\n" + INLINE_COMMENT_SYMBOL + "=" * 50 + "\n\n")
    
    print(f"✅ Arquivo gerado com sucesso: {output_filename}")
    print(f"📊 Tamanho: {os.path.getsize(output_file) / 1024:.2f} KB")


# ═══════════════════════════════════════════════════════════════════════════
# 🚀 PONTO DE ENTRADA
# ═══════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    # Obtém diretório onde o script está executando
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Nome do arquivo de saída: merged_output_<nome_do_diretorio>.txt
    dir_name = os.path.basename(current_dir)
    output_name = f"merged_output_{dir_name}.txt"
    output_path = os.path.join(current_dir, output_name)
    
    try:
        print("=" * 70)
        print("🔗 MERGE PROJECT FILES v1.8.0")
        print("=" * 70 + "\n")

        # Deleta o arquivo de saída se ele já existir
        if os.path.exists(output_path):
            print(f"🧹 Removendo arquivo de saída anterior: {output_name}")
            os.remove(output_path)
        
        merge_project_files(current_dir, output_path)
        
        print("\n" + "=" * 70)
        print("✅ Processo concluído com sucesso!")
        print("=" * 70)
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Operação cancelada pelo usuário")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ ERRO: {e}", file=sys.stderr)
        sys.exit(1)
