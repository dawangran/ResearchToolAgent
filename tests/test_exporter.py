import shutil
import unittest
from pathlib import Path

from core.exporter import materialize_project


class ExporterTests(unittest.TestCase):
    def setUp(self) -> None:
        self.base_dir = Path("tmp_test_generated")
        if self.base_dir.exists():
            shutil.rmtree(self.base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def tearDown(self) -> None:
        if self.base_dir.exists():
            shutil.rmtree(self.base_dir)

    def test_materialize_project_writes_files(self):
        files = {
            "README.md": "# Demo\n",
            "src/main.py": "print('hello')\n",
        }
        output_path = materialize_project(str(self.base_dir), "Demo Tool", files)
        output_dir = Path(output_path)
        self.assertTrue(output_dir.exists())
        self.assertTrue((output_dir / "README.md").exists())
        self.assertTrue((output_dir / "src/main.py").exists())


if __name__ == "__main__":
    unittest.main()
