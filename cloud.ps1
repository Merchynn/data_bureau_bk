# Autenticar na conta Google Cloud

gcloud auth login



# Definir o projeto de trabalho

gcloud config set project lakehouse-sbox-credit

bq extract --destination_format=CSV --compression=GZIP --field_delimiter="," "lakehouse-sbox-credit:sbox_processos.TB_DADOS_BUREAU" gs://informacional_time_credito/DADOS_BUREAU/dados_bureau_*.csv.gz

# Exemplo para download no Windows

gsutil -m cp -r gs://informacional_time_credito/DADOS_BUREAU "C:\Users\NI422434\Downloads"
