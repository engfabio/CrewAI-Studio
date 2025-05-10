import os
import re
import sys
import shutil
from pathlib import Path

def fix_litelm_utils():
    """Corrige o problema de codificação no arquivo utils.py da biblioteca litelm"""
    # Caminho para o arquivo utils.py
    venv_path = Path(os.path.abspath('.venv'))
    utils_path = venv_path / "Lib" / "site-packages" / "litelm" / "utils.py"

    if not utils_path.exists():
        print(f"❌ Arquivo não encontrado: {utils_path}")
        return False

    try:
        # Criar um backup do arquivo original
        backup_path = utils_path.with_suffix('.py.bak')
        shutil.copy2(utils_path, backup_path)
        print(f"✅ Backup criado em: {backup_path}")

        # Ler o conteúdo do arquivo original
        with open(utils_path, 'r', encoding='utf-8') as file:
            content = file.read()

        # Corrigir o problema de codificação (exemplo: remover caracteres inválidos)
        fixed_content = re.sub(r'[^\x00-\x7F]+', '', content)

        # Escrever o conteúdo corrigido de volta ao arquivo
        with open(utils_path, 'w', encoding='utf-8') as file:
            file.write(fixed_content)

        print(f"✅ Arquivo corrigido com sucesso: {utils_path}")
        return True

    except Exception as e:
        print(f"❌ Erro ao corrigir o arquivo: {e}")
        return False
