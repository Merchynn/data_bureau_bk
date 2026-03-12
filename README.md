Este é um modelo de README.md estruturado para destacar suas habilidades técnicas para recrutadores de Big Techs e Bancos. Ele foca na resolução de um problema real de engenharia de dados: a manipulação eficiente de grandes volumes de dados.

Pipeline de Extração e Consolidação de Dados: BigQuery para Local
Descrição do Projeto
Este projeto demonstra um fluxo completo de engenharia de dados para extrair, transferir e consolidar grandes volumes de dados (14GB+) originados no Google BigQuery. O foco principal é superar a limitação de exportação do BigQuery, que fragmenta tabelas grandes em centenas de arquivos, e consolidá-los localmente de forma performática.

Problema
Ao trabalhar com tabelas massivas no BigQuery, a exportação direta para um único arquivo não é suportada. O sistema gera múltiplos arquivos fragmentados (shards). O desafio é baixar esses arquivos e uni-los sem exceder a memória RAM disponível no ambiente local.

Tecnologias Utilizadas
Google BigQuery (SQL): Manipulação e filtragem de dados em larga escala.

Google Cloud CLI (gcloud/bq/gsutil): Automação de processos de extração e transferência Cloud-to-Local.

Python 3.x: Processamento de arquivos via streaming para eficiência de memória.

Bibliotecas Python: gzip, shutil, pathlib.

Fluxo de Trabalho
1. Preparação dos Dados (SQL)
Antes da extração, os dados são processados e atualizados diretamente no Lakehouse via DML otimizado.

SQL
UPDATE `lakehouse-sbox-credit.sbox_processos.TB_DADOS_BUREAU` A
SET status_receita = 2
FROM `lakehouse-sbox-credit.sbox_processos.TB_EQUIFAX_FEV` B
WHERE A.DOC = B.CPF
  AND CAST(B.score AS INT64) > 349;
2. Extração e Transferência (CLI)
Utilização do GCP CLI para exportação fragmentada e download multithread:

Bash
# Exportacao do BigQuery para Google Cloud Storage (Bucket) em GZIP
bq extract --destination_format=CSV --compression=GZIP --field_delimiter="," \
"lakehouse-sbox-credit:sbox_processos.TB_DADOS_BUREAU" \
gs://nome_do_seu_bucket/DADOS_BUREAU/dados_bureau_*.csv.gz

# Download paralelo (multithread) para maquina local
gsutil -m cp -r gs://nome_do_seu_bucket/DADOS_BUREAU "C:\Caminho\Local"
3. Consolidação Eficiente (Python)
O script de consolidação foi desenvolvido com foco em I/O bound efficiency. Em vez de carregar os 14GB na RAM, ele utiliza o método de streaming shutil.copyfileobj, processando os dados em buffers.

Destaques técnicos do script:

Memory Safety: Consumo de memória constante, independentemente do tamanho do arquivo final.

Header Handling: Tratamento automático para manter o cabeçalho apenas na primeira linha do arquivo consolidado.

Automation: Descompressão e união em um único passo.

Detalhes de Implementação (Python)
Python
import gzip
import shutil
import glob
from pathlib import Path

# O script percorre todos os arquivos .csv.gz, realiza a leitura
# em blocos e escreve no arquivo final, descartando headers repetidos.
# (Consulte o arquivo consolidate_bq_extracts.py para o código completo)
Resultados
Volume Processado: 14GB+

Arquivos Fragmentados: 400+

Tempo de Consolidação: Otimizado via streaming.

Uso de Memória: Inferior a 100MB de RAM.

Como Utilizar
Configure suas credenciais do GCP via gcloud auth login.

Execute o comando de extração contido na seção CLI.

Configure os caminhos de entrada e saída no script Python.

Execute o script para obter o arquivo consolidado pronto para análise.
