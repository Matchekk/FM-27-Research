"""Reproduce the narrow source/archive audit offline, without new native calls."""
from argparse import ArgumentParser
from hashlib import sha256
from itertools import product
import json
from pathlib import Path
import struct
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from analysis import run_observer005 as observer
from analysis.startpolicy002_gate import (CONTEXTS, EXPERIMENT, audit_start_state,
    compile_cell, repeat_equivalence)
from research.native import digest, read, require, rows, write
from research.passive_observer import audit_trace, prepared_dump


def rva_slice(image, rva, size):
    require(image[:2] == b'MZ', 'Not a PE image')
    header = struct.unpack_from('<I', image, 0x3c)[0]
    require(image[header:header+4] == b'PE\0\0', 'Not a PE image')
    count = struct.unpack_from('<H', image, header+6)[0]
    optional = struct.unpack_from('<H', image, header+20)[0]
    for index in range(count):
        at = header+24+optional+index*40
        _, virtual, raw_size, raw_at = struct.unpack_from('<4I', image, at+8)
        if virtual <= rva and rva+size <= virtual+raw_size:
            start = raw_at+rva-virtual
            require(start+size <= len(image), 'Truncated PE section')
            return image[start:start+size]
    raise ValueError('Unbacked RVA')


def audit(archive, engine, host_source):
    archive, engine, host_source = Path(archive), Path(engine), Path(host_source)
    identity = read(archive/'data/valid-002/validation-summary.json')['identity']
    require(digest(engine) == identity['engine_sha256'], 'Original engine hash drift')
    old = archive/'local/valid005-observer-v1'
    frozen = read(archive/'data/valid-005-observer-v1/inputs.json')
    require(frozen['identity'] == identity, 'Observer/base identity mismatch')
    configs = read(old/'configs.json')
    catalog = read(archive/'local/runtime-v1114.6/source/tactics_ui/catalog.json')
    seeds = read(old/'seed-plan.json')['seeds']; cells = []
    for i, (context, side) in enumerate(product(CONTEXTS, (0,1))):
        label = f'{context}-{side}'; binary = old/'inputs'/(label+'.bin')
        require(digest(binary) == frozen['setups'][label], 'D00 archive bytes changed')
        high, high_audit = compile_cell(binary.read_bytes(), side, 10000)
        low, low_audit = compile_cell(binary.read_bytes(), side, 7000)
        evidence = rows(old/'technical'/(label+'-observer_on.jsonl'))
        repeat = rows(old/'technical'/(label+'-observer_on_repeat.jsonl'))
        dump_path = old/'technical'/(label+'-observer_on.input.json')
        dump = read(dump_path)
        observer.audit_input(evidence, dump, configs[label], high, catalog, frozen['oop_map'])
        audit_trace(evidence, dump, seeds[i]); audit_start_state(evidence, high, side, 10000)
        aa = repeat_equivalence(evidence, repeat, seeds[i])
        original_dump = archive/'local/tact-002-r0/technical/part-000'/f'tech-{label}-R00-r0.input.json'
        require(prepared_dump(read(original_dump)) == prepared_dump(dump),
                'Original R00 prepared fields/identities/rawTF33 differ from observer D00')
        cells.append(dict(context=context, side=side, high_default=high_audit, low=low_audit,
            high_sha256=sha256(high).hexdigest(), low_sha256=sha256(low).hexdigest(),
            prepared_first_high_raw_and_cache_verified=True,
            original_r00_prepared_dump_fields_and_rawtf33_equal=True,
            observer_log_sha256=digest(old/'technical'/(label+'-observer_on.jsonl')),
            observer_repeat_log_sha256=digest(old/'technical'/(label+'-observer_on_repeat.jsonl')),
            original_r00_dump_sha256=digest(original_dump), observer_dump_sha256=digest(dump_path), aa=aa))
    image = engine.read_bytes()
    # Hash short private disassembly evidence windows; never publish engine bytes.
    windows = [(0x36c50,8,'read_actor_c7a'), (0x36ccb,8,'subtract_actor_1aa6'),
               (0x36cd3,8,'write_actor_c90'), (0x36cf8,6,'write_statistics_cache_8a')]
    source = host_source.read_text(encoding='utf8')
    apply_at = source.index('if(!apply_scenario(match))')
    prep_at = source.index('((void(*)(void*))at(0x4b98f50))(match);', apply_at)
    verify_at = source.index('if(!verify_scenario(match))', prep_at)
    require(apply_at < prep_at < verify_at and '0xc90,0xc7a' in source,
            'Original preparation/profile offset evidence changed')
    return dict(schema='fm27.startpolicy002.offline-audit.v1', experiment_id=EXPERIMENT,
        build=identity['build'], engine_sha256=identity['engine_sha256'],
        observer_host_sha256=frozen['observer_host_sha256'],
        native_host_source_sha256=digest(host_source), tool_tag=identity['lab_version'], tool_commit=identity['lab_commit'],
        source_semantics_manually_reviewed=True, original_profile_application_before_preparation=True,
        original_function_rva='0x36a20', private_instruction_windows=[dict(rva=hex(rva), size=size,
            semantic=semantic, sha256=sha256(rva_slice(image,rva,size)).hexdigest()) for rva,size,semantic in windows],
        cells=cells, new_native_calls=0, new_seeds_reserved=0,
        low7000_native_transfer_verified=False, scientific_main_released=False, career_released=False)


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('--archive', type=Path, required=True)
    parser.add_argument('--engine', type=Path, required=True)
    parser.add_argument('--host-source', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    require(not args.output.exists(), 'Audit report retained; no overwrite')
    result = audit(args.archive, args.engine, args.host_source)
    write(args.output,result)
    print(json.dumps(dict(cells=len(result['cells']),new_native_calls=0,low7000_native_transfer_verified=False)))


if __name__ == '__main__':
    main()
