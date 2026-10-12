"""Run using KiCad's bundled Python after exporting exports/netlist.xml."""
from pathlib import Path
import collections, json, re, xml.etree.ElementTree as ET
import pcbnew as p

root=Path(__file__).resolve().parent
xml=ET.parse(root/'exports/netlist.xml')
actual={n.get('name'):{(x.get('ref'),x.get('pin')) for x in n} for n in xml.findall('./nets/net')}
expected={'/+3V3':{('A1','36'),('R1','1'),('R3','1'),('R5','1')},
          '/GND':{('A1',str(n)) for n in [3,8,13,18,23,28,38]} | {(f'J{i}','2') for i in [1,2,3]} | {(f'D{i}','1') for i in [1,2,3]}}
for i in [1,2,3]:
    expected[f'/IN{i}']={('A1',str(i+3)),(f'R{2*i-1}','2'),(f'R{2*i}','2')}
    expected[f'Net-(J{i}-Pin_1)']={(f'J{i}','1'),(f'R{2*i}','1')}
    expected[f'/LED{i}']={('A1',str(i+13)),(f'R{6+i}','2')}
    expected[f'Net-(D{i}-A)']={(f'R{6+i}','1'),(f'D{i}','2')}
assert {n:v for n,v in actual.items() if not n.startswith('unconnected-')}==expected, 'Schematic circuit differs from requirements'
values={n.get('ref'):n.findtext('value') for n in xml.findall('./components/comp')}
for i in [1,2,3]:
    assert values[f'R{2*i-1}']=='10k'
    assert values[f'R{2*i}']=='1k'
    assert values[f'R{6+i}']=='1k'

board=p.LoadBoard(str(root/'ModuDeck-Module-Monitor.kicad_pcb'))
boardN=collections.defaultdict(set); refs={f.GetReference():f for f in board.GetFootprints()}
for f in board.GetFootprints():
    for pad in f.Pads():
        if pad.GetNumber():boardN[pad.GetNetname()].add((f.GetReference(),pad.GetNumber()))
for net,pins in actual.items():assert boardN[net]==pins, ('Board pad/net mismatch',net)
assert board.GetDesignSettings().GetCopperLayerCount()==2
assert p.ToMM(board.GetDesignSettings().GetBoardThickness())==1.6
pico={x.GetNumber():x for x in refs['A1'].Pads()}
assert set(pico)=={str(n) for n in range(1,41)}
def mm(pos):return (round(p.ToMM(pos.x),4),round(p.ToMM(pos.y),4))
for n,pad in pico.items():
    i=int(n);assert mm(pad.GetPosition())==(160 if i<=20 else 177.78,round(54+(i-1 if i<=20 else 40-i)*2.54,4))
    assert p.ToMM(pad.GetDrillSize().x)==1
for pin in [30,33,35,37,39,40]:assert pico[str(pin)].GetNetname().startswith('unconnected-')
assert {mm(refs[h].GetPosition()) for h in ['H1','H2','H3','H4']}=={(105,55),(185,55),(105,115),(185,115)}
for h in ['H1','H2','H3','H4']:
    assert p.ToMM(next(iter(refs[h].Pads())).GetDrillSize().x)==3.2
edges=list(board.GetDrawings()); segments=[x for x in edges if x.GetLayer()==p.Edge_Cuts]
points={mm(pt) for s in segments for pt in [s.GetStart(),s.GetEnd()]}
assert points=={(100,50),(190,50),(190,120),(100,120)}
assert len(segments)==4
tracks=list(board.GetTracks());assert all(p.ToMM(t.GetWidth())>=0.25 for t in tracks)
keepouts=[z for z in board.Zones() if z.GetIsRuleArea()]
assert len(keepouts)==4
assert all(z.GetDoNotAllowZoneFills() and z.GetDoNotAllowTracks() for z in keepouts)

g=root/'exports/gerbers'; names=list(g.iterdir())
for ext in ['.gtl','.gbl','.gts','.gbs','.gto','.gbo','.gm1']:
    files=[f for f in names if f.suffix==ext];assert len(files)==1
    assert 'M02*' in files[0].read_text()
drillCounts={}
for kind,count in [('PTH',70),('NPTH',4)]:
    content=(g/f'ModuDeck-Module-Monitor-{kind}.drl').read_text()
    hits=re.findall(r'^X[-\d.]+Y[-\d.]+$',content,re.M)
    assert len(hits)==count,(kind,len(hits))
    drillCounts[kind]=len(hits)
images=list((root/'exports/images').glob('*.png'));assert len(images)==6
assert all(f.stat().st_size>10000 for f in images)
result={'status':'PASS','functional_nets':14,'footprints':20,'board_mm':[90,70,1.6],
        'pico_rows_mm':17.78,'pico_pitch_mm':2.54,'tracks':len(tracks),
        'vias':sum(isinstance(t,p.PCB_VIA) for t in tracks),'drill_hits':drillCounts,
        'hardware_tested':False,'checks':['Exact required schematic topology','Schematic-to-board pad net agreement',
        'Pico pin numbering and socket geometry','Unused supply pins isolated on carrier',
        'Mounting holes and copper keepouts','Board outline, two copper layers and trace width',
        'Gerber layer set and file endings','Excellon drill counts','Six exported image files']}
(root/'checks/design-verification.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
