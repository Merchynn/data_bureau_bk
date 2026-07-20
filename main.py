from __future__ import annotations

import argparse
import gzip
import shutil
import time
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ConsolidationResult:
    """Resumo de uma consolidação concluída."""

    source_files: int
    output_file: Path
    output_bytes: int
    duration_seconds: float


def consolidate_gzip_files(
    input_dir: str | Path,
    output_file: str | Path,
    file_pattern: str = "*.csv.gz",
) -> ConsolidationResult:
    """
    Consolida arquivos CSV compactados em GZIP mantendo apenas um cabeçalho.

    O processamento é feito por streaming: cada arquivo é descompactado
    diretamente para a saída, sem carregar o conjunto completo em memória.

    Args:
        input_dir: Diretório com os arquivos de origem.
        output_file: Arquivo CSV/TXT consolidado.
        file_pattern: Padrão glob usado para localizar as origens.

    Raises:
        FileNotFoundError: Quando o diretório ou os arquivos não existem.
        ValueError: Quando a saída também seria selecionada como entrada.
    """
    started_at = time.perf_counter()
    input_path = Path(input_dir).expanduser().resolve()
    output_path = Path(output_file).expanduser().resolve()

    if not input_path.is_dir():
        raise FileNotFoundError(f"Diretório de entrada não encontrado: {input_path}")

    source_files = sorted(path.resolve() for path in input_path.glob(file_pattern))
    if not source_files:
        raise FileNotFoundError(
            f"Nenhum arquivo encontrado em {input_path} com o padrão {file_pattern!r}"
        )

    if output_path in source_files:
        raise ValueError("O arquivo de saída não pode fazer parte das entradas.")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    temporary_output = output_path.with_suffix(output_path.suffix + ".part")

    try:
        with temporary_output.open("wb") as target:
            for index, source_file in enumerate(source_files):
                with gzip.open(source_file, "rb") as source:
                    if index > 0:
                        source.readline()
                    shutil.copyfileobj(source, target)

                processed = index + 1
                if processed % 50 == 0 or processed == len(source_files):
                    percentage = processed / len(source_files) * 100
                    print(
                        f"Progresso: {processed}/{len(source_files)} "
                        f"({percentage:.1f}%)"
                    )

        temporary_output.replace(output_path)
    except Exception:
        temporary_output.unlink(missing_ok=True)
        raise

    duration = time.perf_counter() - started_at
    return ConsolidationResult(
        source_files=len(source_files),
        output_file=output_path,
        output_bytes=output_path.stat().st_size,
        duration_seconds=duration,
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Consolida exports CSV.GZ fragmentados mantendo somente "
            "o cabeçalho do primeiro arquivo."
        )
    )
    parser.add_argument(
        "--input-dir",
        required=True,
        help="Diretório que contém os arquivos CSV.GZ.",
    )
    parser.add_argument(
        "--output-file",
        required=True,
        help="Caminho do arquivo consolidado.",
    )
    parser.add_argument(
        "--pattern",
        default="*.csv.gz",
        help="Padrão glob das entradas. Padrão: *.csv.gz",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()

    try:
        result = consolidate_gzip_files(
            input_dir=args.input_dir,
            output_file=args.output_file,
            file_pattern=args.pattern,
        )
    except (FileNotFoundError, ValueError, OSError) as exc:
        print(f"Erro: {exc}")
        return 1

    size_gib = result.output_bytes / (1024**3)
    print("-" * 60)
    print(f"Arquivos processados: {result.source_files}")
    print(f"Saída: {result.output_file}")
    print(f"Tamanho: {size_gib:.2f} GiB")
    print(f"Tempo: {result.duration_seconds:.2f} segundos")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
