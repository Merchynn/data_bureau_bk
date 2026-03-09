import gzip
import shutil
import glob
import os
import time
from pathlib import Path

def consolidate_gzip_files(input_dir, output_file, file_pattern="*.csv.gz"):
    """
    Consolida multiplos arquivos GZIP em um unico arquivo de texto/CSV,
    mantendo apenas o cabecalho do primeiro arquivo.
    
    Args:
        input_dir (str): Caminho da pasta com os arquivos .gz
        output_file (str): Caminho completo do arquivo de saida (.txt ou .csv)
        file_pattern (str): Padrao de busca dos arquivos.
    """
    start_time = time.time()
    input_path = Path(input_dir)
    output_path = Path(output_file)
    
    # Criar diretorio de saida caso nao exista
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Listar e ordenar arquivos para consistencia
    files = sorted(list(input_path.glob(file_pattern)))
    
    if not files:
        print(f"Erro: Nenhum arquivo encontrado em {input_dir} com o padrao {file_pattern}")
        return

    print(f"Iniciando consolidacao de {len(files)} arquivos...")
    print(f"Diretorio de destino: {output_path}")

    try:
        with open(output_path, 'wb') as f_out:
            for i, file_path in enumerate(files):
                with gzip.open(file_path, 'rb') as f_in:
                    if i == 0:
                        # Primeiro arquivo: Copia tudo (incluindo header)
                        shutil.copyfileobj(f_in, f_out)
                    else:
                        # Arquivos subsequentes: Pula a primeira linha (header)
                        f_in.readline()
                        shutil.copyfileobj(f_in, f_out)
                
                # Log de progresso a cada 50 arquivos
                if (i + 1) % 50 == 0 or (i + 1) == len(files):
                    percent = ((i + 1) / len(files)) * 100
                    print(f"Progresso: {i + 1}/{len(files)} ({percent:.1f}%)")

        end_time = time.time()
        duration = end_time - start_time
        print("-" * 40)
        print(f"Sucesso! Arquivo consolidado em {duration:.2f} segundos.")
        print(f"Tamanho final aproximado: {output_path.stat().st_size / (1024**3):.2f} GB")

    except Exception as e:
        print(f"Erro critico durante o processamento: {e}")

if __name__ == "__main__":
    # --- CONFIGURACOES ---
    # Substitua pelos caminhos do seu ambiente
    PASTA_DOS_DADOS = r'C:\Users\NI422434\Downloads\DADOS_BUREAU'
    ARQUIVO_FINAL = r'D:\DADOS_BUREAU_CONSOLIDADO.txt' 
    
    consolidate_gzip_files(PASTA_DOS_DADOS, ARQUIVO_FINAL)
