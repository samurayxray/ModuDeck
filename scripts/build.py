"""Export ModuDeck STL concepts and standalone viewer. Requires OpenSCAD on PATH."""
from pathlib import Path
import json,re,subprocess,shutil,math

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"output"
CAD=OUT/"cad"
CAD.mkdir(parents=True,exist_ok=True)
parts=json.loads((ROOT/"parts.json").read_text())
models={}
meta={}

def export(source,target,defines=()):
    command=["openscad","--export-format","asciistl"]
    for value in defines:
        command+=["-D",value]
    command+=["-o",str(target),str(source)]
    subprocess.run(command,check=True)
    text=target.read_text()
    vertices=[[round(float(x),3) for x in match] for match in re.findall(r"vertex\s+([-+\deE.]+)\s+([-+\deE.]+)\s+([-+\deE.]+)",text)]
    if not vertices or len(vertices)%3 or not all(math.isfinite(x) for v in vertices for x in v):
        raise RuntimeError("Invalid or empty mesh: "+str(target))
    return [vertices[i:i+3] for i in range(0,len(vertices),3)]

for key,defines in [("assembled",["exploded=false","phone_open=false"]),("exploded",["exploded=true","phone_open=true"])]:
    models[key]=export(ROOT/"cad/modudeck.scad",CAD/("modudeck-"+key+".stl"),defines)
    meta[key]={"name":"Assemblato" if key=="assembled" else "Vista esplosa","role":"PC e tre piani vuoti"}
for part in parts:
    key=part["id"]
    models[key]=export(ROOT/"cad/parts"/(key+".scad"),CAD/(key+".stl"))
    meta[key]={"name":part["name"],"role":part["role"]}
template=(ROOT/"viewer/template.html").read_text()
html=template.replace("__MODELS__",json.dumps(models,separators=(",",":"))).replace("__META__",json.dumps(meta,ensure_ascii=False))
(OUT/"ModuDeck-parts-3D.html").write_text(html,encoding="utf-8")
(ROOT/"ModuDeck-parts-3D.html").write_text(html,encoding="utf-8")
shutil.copytree(ROOT/"cad",OUT/"sources",dirs_exist_ok=True)
shutil.copytree(ROOT/"docs",OUT/"docs",dirs_exist_ok=True)
for name in ["README.md","parts.json","BOM.csv","JOURNAL.md"]:
    shutil.copy2(ROOT/name,OUT/name)
print("Exported and checked",len(models),"models. Open output/ModuDeck-parts-3D.html")
