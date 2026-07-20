import gzip
import tempfile
import unittest
from pathlib import Path

from main import consolidate_gzip_files


class ConsolidateGzipFilesTests(unittest.TestCase):
    def test_consolidates_files_and_keeps_single_header(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            rows = [
                "id,name\n1,Ana\n2,Bruno\n",
                "id,name\n3,Carla\n",
                "id,name\n4,Diego\n5,Elisa\n",
            ]

            for index, content in enumerate(rows):
                with gzip.open(
                    root / f"part-{index:03d}.csv.gz",
                    "wt",
                    encoding="utf-8",
                ) as file:
                    file.write(content)

            output = root / "out" / "consolidated.csv"
            result = consolidate_gzip_files(root, output)

            self.assertEqual(result.source_files, 3)
            self.assertEqual(
                output.read_text(encoding="utf-8"),
                "id,name\n1,Ana\n2,Bruno\n3,Carla\n4,Diego\n5,Elisa\n",
            )

    def test_raises_when_no_source_files_exist(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            with self.assertRaises(FileNotFoundError):
                consolidate_gzip_files(root, root / "output.csv")


if __name__ == "__main__":
    unittest.main()
