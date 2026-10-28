import io
import json
from contextlib import redirect_stdout
from pathlib import Path
import unittest
from unittest.mock import patch

from paper_reconstruction_stage2 import release_cli


class ReleaseInterfaceTests(unittest.TestCase):
    def test_invalid_models_have_machine_readable_failure(self):
        output = io.StringIO()
        with redirect_stdout(output):
            code = release_cli.main(['verify', '--models', 'missing-model-directory'])
        self.assertEqual(code, 2)
        self.assertEqual(json.loads(output.getvalue())['status'], 'failed')

    def test_cpu_wrapper_authenticates_release_configuration(self):
        from types import SimpleNamespace
        expected = release_cli.metadata()['model']
        fake = SimpleNamespace(model_sha256=expected['sha256'], release_manifest_sha256='0'*64)
        with patch('paper_reconstruction_stage2.onnx_runtime.OnnxModelRelease.load', return_value=fake):
            with self.assertRaisesRegex(ValueError, 'configuration differs'):
                release_cli.verify_models(Path('models'))
