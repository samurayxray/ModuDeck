"""Read-only Open CASCADE checks of KiCad STEP references, not enclosure approval.

Requires cadquery-ocp (this run: 8.0.1.1.0). Supply its installation directory
with --runtime when it is outside the active Python environment.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import sys


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--runtime', type=Path)
    parser.add_argument('--reference', type=Path, default=Path(__file__).parent / 'reference')
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise SystemExit('Output exists; preserve the previous check.')
    if args.runtime:
        sys.path.insert(0, str(args.runtime.resolve()))
    import OCP
    from OCP.STEPControl import STEPControl_Reader
    from OCP.IFSelect import IFSelect_RetDone
    from OCP.Bnd import Bnd_Box
    from OCP.BRepBndLib import BRepBndLib
    from OCP.BRepCheck import BRepCheck_Analyzer
    from OCP.BRep import BRep_Tool
    from OCP.TopExp import TopExp_Explorer
    from OCP.TopAbs import TopAbs_SOLID, TopAbs_SHELL

    measurements = []
    for path in sorted(args.reference.glob('*.step')):
        raw = path.read_bytes()
        assert raw.startswith(b'ISO-10303-21;')
        assert b'SI_UNIT(.MILLI.,.METRE.)' in raw
        reader = STEPControl_Reader()
        assert reader.ReadFile(str(path.resolve())) == IFSelect_RetDone
        assert reader.TransferRoots() > 0
        shape = reader.OneShape()
        assert not shape.IsNull()
        box = Bnd_Box()
        BRepBndLib.AddOptimal_s(shape, box, False, False)
        low, high = box.CornerMin(), box.CornerMax()
        lower, upper = [low.X(), low.Y(), low.Z()], [high.X(), high.Y(), high.Z()]
        solids = TopExp_Explorer(shape, TopAbs_SOLID)
        valid = []
        closed = []
        shell_counts = []
        while solids.More():
            solid = solids.Current()
            valid.append(BRepCheck_Analyzer(solid).IsValid())
            shells = TopExp_Explorer(solid, TopAbs_SHELL)
            count = 0
            while shells.More():
                closed.append(BRep_Tool.IsClosed_s(shells.Current()))
                count += 1
                shells.Next()
            shell_counts.append(count)
            solids.Next()
        assert valid and all(valid) and closed and all(closed) and all(shell_counts)
        measurements.append({
            'file': path.name, 'sha256': hashlib.sha256(raw).hexdigest(),
            'bounds_min_mm': lower, 'bounds_max_mm': upper,
            'size_mm': [b-a for a, b in zip(lower, upper)],
            'solid_count': len(valid), 'valid_solids': sum(valid),
            'shell_count': len(closed), 'closed_shells': sum(closed),
        })
    assembly = next(m for m in measurements if m['file'] == 'module-monitor-pcb-assembly.step')
    result = {
        'generated_utc': datetime.now(timezone.utc).isoformat(),
        'generated_by': 'Codex automated technical checks',
        'ocp_version': OCP.__version__,
        'units': 'mm',
        'step_coordinates': 'X right, Y up (PCB extends toward negative Y); board substrate bottom Z=0',
        'measurements': measurements,
        'provisional_stack': {
            'interpretation': '28mm base height; 2.5mm lid rests ON rim, total closed height 30.5mm',
            'base_outer_mm': [112, 94, 28], 'wall_and_floor_mm': 2.5,
            'lid_mm': [112, 94, 2.5], 'support_above_inner_floor_mm': 5,
            'pcb_underside_enclosure_z_mm': 7.5,
            'assembly_max_enclosure_z_mm': 7.5 + assembly['bounds_max_mm'][2],
            'lid_underside_z_mm': 28,
            'model_top_gap_mm': 28 - 7.5 - assembly['bounds_max_mm'][2],
            'model_lead_to_floor_gap_mm': 5 + assembly['bounds_min_mm'][2],
            'internal_xy_mm': [107, 89],
            'unused_total_xy_for_nominal_board_mm': [17, 19],
            'pcb_xy_position_selected': False,
            'physical_fit_verified': False,
        },
        'enclosure_solids_exist': False, 'enclosure_interferences_checked': False,
        'printable_stl_files_exist': False, 'physical_test_performed': False,
        'limits': [
            'STEP body is the substrate; default export omits copper and soldermask geometry.',
            'Nominal PCB thickness 1.6mm comes from the PCB file; substrate STEP alone is thinner.',
            'No enclosure, USB plug, wires, fasteners, lid bosses or print tolerances are represented.',
            'A bounding-box gap does not test access, removal paths or collision with future supports.',
        ],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
