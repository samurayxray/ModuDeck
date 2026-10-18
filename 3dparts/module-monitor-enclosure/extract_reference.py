"""Extract measurements and a STEP reference, without generating an enclosure.

Run with KiCad's bundled Python. Files are never overwritten by this script.
The editable KiCad project is read only.
"""
from pathlib import Path
import argparse
import csv
import hashlib
import json
import subprocess
from datetime import datetime, timezone
import pcbnew as pcb


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--kicad-cli', required=True)
    parser.add_argument('--output', type=Path, required=True,
                        help='New or empty output directory')
    args = parser.parse_args()
    repo = Path(__file__).resolve().parents[2]
    source = repo / 'electronics/module-monitor/ModuDeck-Module-Monitor.kicad_pcb'
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    if any(output.iterdir()):
        raise SystemExit('Output must be empty; preserve previous evidence.')
    source_hash = sha256(source)
    board = pcb.LoadBoard(str(source))
    model_library = Path(args.kicad_cli).resolve().parent.parent / 'share/kicad/3dmodels'

    def xy(point):
        return [round(pcb.ToMM(point.x), 6), round(pcb.ToMM(point.y), 6)]

    edges = []
    for drawing in board.GetDrawings():
        if drawing.GetLayer() == pcb.Edge_Cuts:
            if drawing.GetShape() != pcb.SHAPE_T_SEGMENT:
                raise SystemExit('Non-segment outline requires additional analysis.')
            edges.append({'start_mm': xy(drawing.GetStart()),
                          'end_mm': xy(drawing.GetEnd())})
    points = {tuple(e[k]) for e in edges for k in ('start_mm', 'end_mm')}
    xmin, ymin = map(min, zip(*points))
    xmax, ymax = map(max, zip(*points))
    degrees = {point: sum(point == tuple(e[k]) for e in edges
                         for k in ('start_mm', 'end_mm')) for point in points}
    assert len(edges) == 4 and len(points) == 4 and set(degrees.values()) == {2}
    assert points == {(xmin, ymin), (xmax, ymin), (xmax, ymax), (xmin, ymax)}
    assert all(e['start_mm'][0] == e['end_mm'][0]
               or e['start_mm'][1] == e['end_mm'][1] for e in edges)

    def local(point):
        x, y = xy(point)
        return [round(x - xmin, 6), round(y - ymin, 6)]

    footprints = []
    for fp in sorted(board.GetFootprints(), key=lambda x: x.GetReference()):
        models = []
        for model in fp.Models():
            name = model.m_Filename.replace('\\', '/').split('/')[-1]
            bundled = source.parent / 'models' / name
            if not bundled.is_file():
                raise SystemExit(f'Missing project model: {name}')
            library_prefix = '${KICAD10_3DMODEL_DIR}/'
            project_prefix = '${KIPRJMOD}/'
            if model.m_Filename.startswith(library_prefix):
                resolved = model_library / model.m_Filename[len(library_prefix):]
            elif model.m_Filename.startswith(project_prefix):
                resolved = source.parent / model.m_Filename[len(project_prefix):]
            else:
                raise SystemExit(f'Model path requires explicit resolution: {model.m_Filename}')
            assert resolved.is_file(), f'Missing referenced model: {resolved}'
            assert sha256(resolved) == sha256(bundled), f'Library differs from project copy: {name}'
            models.append({
                'pcb_model_path': model.m_Filename,
                'project_copy': bundled.relative_to(repo).as_posix(),
                'sha256': sha256(bundled),
                'resolved_source': str(resolved),
                'offset_mm': [model.m_Offset.x, model.m_Offset.y, model.m_Offset.z],
                'rotation_deg': [model.m_Rotation.x, model.m_Rotation.y, model.m_Rotation.z],
                'scale': [model.m_Scale.x, model.m_Scale.y, model.m_Scale.z],
            })
        pads = [{'number': pad.GetNumber(), 'center_local_mm': local(pad.GetPosition()),
                 'drill_mm': xy(pad.GetDrillSize()),
                 'npth': pad.GetAttribute() == pcb.PAD_ATTRIB_NPTH}
                for pad in fp.Pads()]
        footprints.append({'reference': fp.GetReference(), 'value': fp.GetValue(),
                           'footprint': str(fp.GetFPID().GetLibItemName()),
                           'anchor_local_mm': local(fp.GetPosition()),
                           'rotation_kicad_deg': fp.GetOrientationDegrees(),
                           'pads': pads, 'models': models})
    holes = [{'reference': fp['reference'], **pad}
             for fp in footprints for pad in fp['pads'] if pad['npth']]
    hole_x = sorted({h['center_local_mm'][0] for h in holes})
    hole_y = sorted({h['center_local_mm'][1] for h in holes})
    assert len(holes) == 4 and len(hole_x) == 2 and len(hole_y) == 2
    data = {
        'generated_utc': datetime.now(timezone.utc).isoformat(),
        'generated_by': 'Automated technical extraction by Codex; not personal modelling work',
        'kicad_version': pcb.GetBuildVersion(),
        'source': source.relative_to(repo).as_posix(), 'source_sha256': source_hash,
        'units': 'mm',
        'coordinate_system': 'Component-side top-left outline = (0,0); X right, Y down',
        'outline_absolute_mm': edges, 'outline_origin_absolute_mm': [xmin, ymin],
        'board_size_mm': [round(xmax-xmin, 6), round(ymax-ymin, 6),
                          pcb.ToMM(board.GetDesignSettings().GetBoardThickness())],
        'mounting_hole_spacing_mm': [hole_x[1]-hole_x[0], hole_y[1]-hole_y[0]],
        'mounting_holes': holes, 'footprints': footprints,
        'physical_measurement': False, 'enclosure_model_created': False,
    }
    (output / 'pcb-geometry.json').write_text(json.dumps(data, indent=2) + '\n', encoding='utf-8')
    with (output / 'component-positions.csv').open('w', newline='', encoding='utf-8') as stream:
        writer = csv.writer(stream)
        writer.writerow(['reference', 'value', 'anchor_x_mm', 'anchor_y_mm', 'kicad_rotation_deg', '3d_models'])
        for fp in footprints:
            writer.writerow([fp['reference'], fp['value'], *fp['anchor_local_mm'],
                             fp['rotation_kicad_deg'], len(fp['models'])])
    logs = []
    for filename, flags in [
        ('module-monitor-pcb-assembly.step', []),
        ('pcb-body.step', ['--board-only']),
        ('pico-and-sockets.step', ['--no-board-body', '--component-filter', 'A1']),
        ('terminal-j1.step', ['--no-board-body', '--component-filter', 'J1']),
    ]:
        command = [args.kicad_cli, 'pcb', 'export', 'step', *flags,
                   '--define-var', f'KICAD10_3DMODEL_DIR={model_library}', '--user-origin',
                   f'{xmin}x{ymin}mm', '--output', str(output / filename), str(source)]
        result = subprocess.run(command, capture_output=True, text=True, encoding='utf-8', errors='replace')
        logs.append({'command': command, 'exit_code': result.returncode,
                     'stdout': result.stdout, 'stderr': result.stderr})
        (output / 'step-export-details.json').write_text(json.dumps(logs, indent=2) + '\n', encoding='utf-8')
        if len(logs) == 1:
            (output / 'step-export.json').write_text(json.dumps(logs[0], indent=2) + '\n', encoding='utf-8')
        assert result.returncode == 0, result.stdout + result.stderr
    step = output / 'module-monitor-pcb-assembly.step'
    assert step.is_file() and step.stat().st_size > 10000
    assert sha256(source) == source_hash, 'Source PCB changed during extraction'
    (output / 'sha256.json').write_text(json.dumps({p.name: sha256(p)
        for p in sorted(output.iterdir()) if p.is_file()}, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'board_size_mm': data['board_size_mm'],
                      'hole_spacing_mm': data['mounting_hole_spacing_mm'],
                      'footprints': len(footprints),
                      'model_instances': sum(len(fp['models']) for fp in footprints),
                      'step_bytes': step.stat().st_size, 'output': str(output)}, indent=2))


if __name__ == '__main__':
    main()
