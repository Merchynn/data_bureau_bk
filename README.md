# BigQuery Export Consolidator

Utilitário em Python para consolidar centenas de arquivos `CSV.GZ` gerados por exports fragmentados do BigQuery em um único arquivo, mantendo apenas o cabeçalho da primeira parte.

## Problema resolvido

Exports de tabelas grandes no BigQuery normalmente são divididos em vários objetos no Cloud Storage. Baixar e concatenar esses arquivos de forma ingênua pode duplicar cabeçalhos ou consumir memória demais.

Este projeto processa os arquivos por streaming:

1. localiza e ordena as partes;
2. descompacta cada arquivo diretamente para a saída;
3. mantém o cabeçalho apenas da primeira parte;
4. grava em arquivo temporário e substitui a saída somente ao final;
5. informa quantidade de arquivos, tamanho e duração.

No caso de uso original, a rotina foi aplicada a um volume superior a 14 GB e mais de 400 arquivos. Esses números representam o contexto operacional original, não um benchmark automatizado deste repositório.

## Requisitos

- Python 3.10 ou superior;
- somente a biblioteca padrão do Python.

## Uso

```bash
python main.py \
  --input-dir "./data/export" \
  --output-file "./output/consolidated.csv"
```

Outro padrão de arquivo pode ser informado:

```bash
python main.py \
  --input-dir "./data/export" \
  --output-file "./output/consolidated.txt" \
  --pattern "*.gz"
```

## Testes

```bash
python -m unittest discover -s tests -v
```

## Decisões técnicas

- **Streaming:** evita carregar o conjunto completo na memória.
- **Ordenação determinística:** processa os shards sempre na mesma ordem.
- **Escrita atômica:** a saída definitiva só é criada após a conclusão.
- **Falha explícita:** diretórios inválidos ou ausência de arquivos encerram a execução com erro.
- **CLI parametrizada:** nenhum caminho de máquina ou usuário fica fixado no código.

## Estrutura

```text
.
├── main.py
├── tests/
│   └── test_main.py
├── .gitignore
└── README.md
```

## Limitações

- pressupõe que todos os arquivos possuam o mesmo layout;
- remove a primeira linha de todas as partes após a primeira;
- não valida tipos ou quantidade de colunas;
- não realiza download do Cloud Storage — a consolidação começa com os arquivos já disponíveis localmente.
