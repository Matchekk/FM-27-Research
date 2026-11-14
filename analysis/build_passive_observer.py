"""Compile an isolated private observer host; do not run it or alter upstream.

Requires already installed MSVC/Windows SDK. No download, installer, game code
copy, host invocation, runtime/server import, seed or registry access occurs.
"""
import argparse
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from research.passive_observer import ENGINE, VERSION, file_hash, instrument_source, require

UPSTREAM_COMMIT = '91f2eba57fac0b7fbd3dff616056907e3ce461be'
HOST_SOURCE = '72025a966fd244933bcec731f0789b7a1eba834e991f6e9bae4762a148bcc43a'


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def build(upstream, game, output, toolchain, sdk):
    upstream, game, output, toolchain, sdk = [Path(p).resolve() for p in (upstream, game, output, toolchain, sdk)]
    require('local' in [p.name for p in output.parents] and output not in (upstream, game) and
            upstream not in output.parents and game not in output.parents,
            'Choose a new private directory below local/, outside game/upstream trees')
    require(not output.exists(), 'Build attempt exists: retain it, never overwrite')
    actual = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=upstream, text=True).strip()
    require(actual == UPSTREAM_COMMIT and not subprocess.check_output(
        ['git', 'status', '--porcelain'], cwd=upstream, text=True).strip(), 'Upstream drift/dirty tree')
    native = upstream/'native'
    require(file_hash(native/'desktop_host.cpp') == HOST_SOURCE, 'Host source drift')
    require((upstream/'LICENSE').read_text(encoding='utf8').startswith('MIT License'), 'License drift')
    dll = game/'fm_Data/Plugins/x86_64/game_plugin.dll'
    require(file_hash(dll) == ENGINE, 'Engine drift: no private contract generated')
    compiler = toolchain/'bin/Hostx64/x64/cl.exe'
    require(compiler.is_file(), 'Existing MSVC x64 compiler required')
    include = [toolchain/'include', *[sdk/'Include/10.0.22621.0'/p for p in ('ucrt','um','shared','winrt','cppwinrt')]]
    libs = [toolchain/'lib/x64', sdk/'Lib/10.0.22621.0/ucrt/x64', sdk/'Lib/10.0.22621.0/um/x64']
    require(all(p.is_dir() for p in include+libs), 'Pinned existing SDK/toolchain directories missing')
    sdk_bin = sdk/'bin/10.0.22621.0/x64'
    require((sdk_bin/'mt.exe').is_file(), 'Existing SDK manifest linker required')
    output.mkdir(parents=True, exist_ok=False)
    provenance = dict(schema=VERSION, build_status='preparing', upstream_commit=actual,
        upstream_license='MIT', license_sha256=file_hash(upstream/'LICENSE'),
        engine_sha256=ENGINE, compiler_binary_sha256=file_hash(compiler),
        toolset_directory=toolchain.name, sdk_directory='10.0.22621.0',
        prepared_utc=datetime.now(timezone.utc).isoformat(), native_starts=0,
        native_release_granted=False)
    manifest = output/'build-manifest.json'
    def save():
        manifest.write_text(json.dumps(provenance, indent=2)+'\n', encoding='utf8')
    save()
    try:
        copied = {}
        for path in native.iterdir():
            if path.suffix in {'.cpp','.h','.manifest'}:
                shutil.copy2(path, output/path.name)
                copied[path.name] = file_hash(path)
        shutil.copy2(upstream/'LICENSE', output/'UPSTREAM-LICENSE.txt')
        source = (output/'desktop_host.cpp').read_bytes().decode('utf8')
        require(instrument_source(source, enabled=False).encode('utf8') == source.encode('utf8'),
                'Disabled source transform differs')
        (output/'desktop_host.cpp').write_bytes(instrument_source(source).encode('utf8'))
        shutil.copy2(ROOT/'adapters/passive_observer_v1.h', output/'passive_observer_v1.h')
        # Pure source helpers. Do not call generate(), which writes into upstream.
        sys.path.insert(0, str(upstream/'scripts'))
        generator = load('observer_generate_profile', upstream/'scripts/generate_profile.py')
        formatter = load('observer_profile_header', upstream/'scripts/profile_header.py')
        metadata = json.loads((native/'profile_metadata.json').read_text(encoding='utf8'))
        profile = generator.restore_profile(metadata, dll.read_bytes())
        (output/'engine_compat_profile.h').write_text(formatter.header(profile), encoding='ascii')
        provenance.update(source_files_sha256=copied,
            modified_host_source_sha256=file_hash(output/'desktop_host.cpp'),
            observer_header_sha256=file_hash(output/'passive_observer_v1.h'),
            private_compatibility_header_sha256=file_hash(output/'engine_compat_profile.h'),
            source_disabled_transform_identical=True, build_status='compiling')
        save()
        env = dict(os.environ)
        env['PATH'] = str(compiler.parent)+os.pathsep+str(sdk_bin)+os.pathsep+env.get('PATH','')
        env['INCLUDE'] = os.pathsep.join(map(str,include))
        env['LIB'] = os.pathsep.join(map(str,libs))
        env['LIBPATH'] = str(toolchain/'lib/x64')
        command = [str(compiler), '/nologo','/O2','/EHsc','/std:c++17','desktop_host.cpp',
                   '/Fe:FM27PassiveObserver.exe','/Fo:desktop_host.obj','/link','/INCREMENTAL:NO',
                   '/MANIFEST:EMBED','/MANIFESTINPUT:host.manifest','user32.lib']
        with (output/'compiler.stdout').open('wb') as log:
            result = subprocess.run(command, cwd=output, env=env, stdout=log,
                stderr=subprocess.STDOUT, timeout=90, creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
        provenance.update(compiler_returncode=result.returncode,
                          compiler_stdout_sha256=file_hash(output/'compiler.stdout'))
        require(result.returncode == 0, 'Private compile failed; retained original attempt')
        provenance.update(build_status='compiled_not_executed', observer_host_sha256=file_hash(output/'FM27PassiveObserver.exe'),
                          observer_host_bytes=(output/'FM27PassiveObserver.exe').stat().st_size)
        save()
        require(not subprocess.check_output(['git','status','--porcelain'],cwd=upstream,text=True).strip(),
                'Upstream unexpectedly changed')
        return provenance
    except Exception as error:
        provenance.update(build_status='failed', error_type=type(error).__name__)
        save()
        raise


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ('upstream','game','output','toolchain','sdk'):
        parser.add_argument('--'+name, type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(build(args.upstream,args.game,args.output,args.toolchain,args.sdk), indent=2))
