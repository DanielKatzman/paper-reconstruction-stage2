"""CPU v2 distribution wrapper around the unchanged Stage 2 v1.0.2 core."""
from contextlib import redirect_stdout
from pathlib import Path
import argparse
import hashlib
import json
import sys


def metadata():
    return json.loads(Path(__file__).with_name('compatibility.json').read_text(encoding='utf-8'))


def verify_models(models):
    from .onnx_runtime import OnnxModelRelease
    release = OnnxModelRelease.load(Path(models)/'release.json')
    expected = metadata()['model']
    if (release.model_sha256 != expected['sha256']
            or release.release_manifest_sha256 != expected['release_manifest_sha256']):
        raise ValueError('Model/configuration differs from this distribution')
    return release


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    v = sub.add_parser('verify'); v.add_argument('--models', type=Path, required=True)
    i = sub.add_parser('inspect'); i.add_argument('--input', type=Path, required=True)
    i.add_argument('--models', type=Path, required=True)
    r = sub.add_parser('run'); r.add_argument('--input', type=Path, required=True)
    r.add_argument('--output', type=Path, required=True); r.add_argument('--models', type=Path, required=True)
    r.add_argument('--cpu-threads', type=int, default=4); r.add_argument('--resume', action='store_true')
    args = parser.parse_args(argv)
    try:
        release = verify_models(args.models)
        if args.command == 'verify':
            result = {'status': 'verified', 'release_version': '2.0.0', 'device': 'cpu',
                      'component_software_version': '1.0.2', 'model_sha256': release.model_sha256}
        else:
            if args.command == 'run':
                if args.cpu_threads < 1:
                    raise ValueError('CPU thread count must be positive')
                from .production_cli import main as infer
                command = ['--input', str(args.input.resolve()), '--output', str(args.output.resolve()),
                           '--release', str(release.release_path), '--cpu-threads', str(args.cpu_threads)]
                if args.resume:
                    command.append('--resume')
                with redirect_stdout(sys.stderr):
                    infer(command)
                output = args.output.resolve()
            else:
                output = args.input.resolve()
            from .verification import verify_stage2_output
            report = verify_stage2_output(output, release_path=release.release_path)
            manifest = output/'edge_hypotheses_manifest.json'
            result = {'status': 'ready', 'output': str(output), 'verification': report,
                      'manifest_sha256': hashlib.sha256(manifest.read_bytes()).hexdigest()}
        print(json.dumps(result, sort_keys=True))
        return 0
    except KeyboardInterrupt:
        print(json.dumps({'status': 'interrupted'})); return 130
    except Exception as exc:
        print(str(exc), file=sys.stderr)
        print(json.dumps({'status': 'failed', 'error': str(exc)})); return 2


if __name__ == '__main__':
    raise SystemExit(main())
