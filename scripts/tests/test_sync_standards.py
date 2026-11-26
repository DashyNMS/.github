import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('sync', Path(__file__).resolve().parents[1] / 'sync_standards.py')
sync = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sync)


class StandardsEncodingTests(unittest.TestCase):
    def test_utf8_round_trip_and_preflight_before_writes(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder) / 'source'
            consumer = Path(folder) / 'consumer'
            (root / 'policy').mkdir(parents=True)
            (consumer / '.github').mkdir(parents=True)
            (consumer / '.github/repository-config.json').write_text('{}', encoding='utf-8')
            (root / 'policy/claude-conventions.md').write_text('Shared.\n', encoding='utf-8')
            claude = consumer / 'CLAUDE.md'
            claude.write_text('# “Guide”\n\n## Repository conventions\nold\n## Validation and releases\nLocal.\n', encoding='utf-8')
            (root / 'managed.txt').write_bytes(b'new')
            (consumer / 'managed.txt').write_bytes(b'old')
            with patch.object(sync, 'ROOT', root), patch.object(sync, 'SHARED', ['managed.txt']), \
                    patch.object(sync, 'HELPERS', []), \
                    patch.object(sync.subprocess, 'check_output', side_effect=['', 'a' * 40]), \
                    patch('sys.argv', ['sync', str(consumer)]):
                sync.main()
            self.assertIn('# “Guide”', claude.read_text(encoding='utf-8'))
            self.assertEqual('a' * 40, json.loads((consumer / '.github/repository-standards.json').read_text(encoding='utf-8'))['revision'])
            claude.write_bytes(b'invalid sections')
            (consumer / 'managed.txt').write_bytes(b'old')
            with patch.object(sync, 'ROOT', root), patch.object(sync, 'SHARED', ['managed.txt']), \
                    patch.object(sync, 'HELPERS', []), \
                    patch.object(sync.subprocess, 'check_output', side_effect=['', 'a' * 40]), \
                    patch('sys.argv', ['sync', str(consumer)]), self.assertRaises(ValueError):
                sync.main()
            self.assertEqual(b'old', (consumer / 'managed.txt').read_bytes())
