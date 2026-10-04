from pathlib import Path
import json,re
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
p=Path(__file__).parent
items=json.loads((p/'parts.json').read_text())
models={}; meta={}
for a in items:
 s=(p/'cad/parts'/f"{a['name']}.stl").read_text()
 v=[[round(float(x),2) for x in m] for m in re.findall(r'vertex\s+([-+\deE.]+)\s+([-+\deE.]+)\s+([-+\deE.]+)',s)]
 models[a['name']]=[v[i:i+3] for i in range(0,len(v),3)]
 meta[a['name']]={'name':a['name'],'role':a['note']}
source=Path('ModuDeck/make_parts_viewer.py').read_text()
template=source.split("html='''",1)[1].split("'''.replace",1)[0]
template=template.replace("let mode='exploded'","let mode='01-pc-lower-shell'").replace('MODELS',json.dumps(models,separators=(",",":"))).replace('META',json.dumps(meta))
(p/'ModuDeck-ThinkPad-3D.html').write_text(template)
groups=[('01-computer-parts',['01-pc-lower-shell','02-top-deck-blank','03-display-back','04-display-frame','05-keyboard-mount-rail','06-touchpad-support'],'Computer enclosure and supports'),('02-three-empty-trays',['09-empty-tray-lower','10-empty-tray-middle','11-empty-tray-upper','12-rear-cable-panel'],'Three empty trays and rear panel'),('03-small-parts',['07-board-mount-rail','08-board-standoff','13-alignment-guide','14-cable-clamp','15-foot','16-side-joining-tab','17-handle','18-hinge-mount-block'],'Mounts and mechanical accessories')]
for filename,names,title in groups:
 fig=plt.figure(figsize=(14,9),facecolor='#eef3f8')
 fig.suptitle('ModuDeck | '+title,fontsize=19)
 for i,name in enumerate(names):
  ax=fig.add_subplot(2,4 if len(names)>6 else 3,i+1,projection='3d')
  faces=models[name];ax.add_collection3d(Poly3DCollection(faces,facecolor='#4191b7',edgecolor='#153f56',linewidth=.08))
  vs=[v for f in faces for v in f];lo=[min(v[k] for v in vs) for k in range(3)];hi=[max(v[k] for v in vs) for k in range(3)]
  ax.set_xlim(lo[0],hi[0]);ax.set_ylim(lo[1],hi[1]);ax.set_zlim(lo[2],max(hi[2],lo[2]+1));ax.set_box_aspect([max(hi[k]-lo[k],2) for k in range(3)])
  ax.view_init(30,-55);ax.set_axis_off();ax.set_title(name[3:].replace('-',' '),fontsize=10)
 fig.text(.5,.025,'Actual STL previews | 370 x 240 mm provisional envelope | Fit, cutouts and fasteners pending measurement',ha='center',fontsize=11)
 fig.savefig(p/(filename+'.png'),dpi=150);plt.close(fig)
print('3 mesh preview images and offline 18-part viewer created')
