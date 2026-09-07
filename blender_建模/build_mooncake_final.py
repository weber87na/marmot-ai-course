# 完整重建：原始圖片 → 立體模型 → 烘焙貼圖 → blend 與 GLB。
# Blender 5.2：blender -b --python build_mooncake_final.py
import sys, json, struct
import bpy, math, os
from mathutils import Vector
from math import sin, cos, pi
ROOT=os.path.dirname(os.path.abspath(__file__))
bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete(use_global=False)

def pastry(name, dark=False):
 m=bpy.data.materials.new(name); m.use_nodes=True
 n=m.node_tree.nodes; l=m.node_tree.links; n.clear()
 out=n.new('ShaderNodeOutputMaterial'); p=n.new('ShaderNodeBsdfPrincipled'); l.new(p.outputs['BSDF'],out.inputs[0])
 p.inputs['Roughness'].default_value=.29; p.inputs['Coat Weight'].default_value=.24; p.inputs['Coat Roughness'].default_value=.22
 p.inputs['Subsurface Weight'].default_value=.015
 tex=n.new('ShaderNodeTexCoord'); noise=n.new('ShaderNodeTexNoise'); noise.inputs['Scale'].default_value=7; noise.inputs['Detail'].default_value=4
 l.new(tex.outputs['Object'],noise.inputs['Vector'])
 ramp=n.new('ShaderNodeValToRGB'); ramp.color_ramp.elements.remove(ramp.color_ramp.elements[1])
 colors=[(.2,(.12,.022,.004,1)),(.43,(.36,.085,.012,1)),(.62,(.68,.25,.042,1)),(.82,(.93,.48,.12,1))] if dark else [(.18,(.23,.055,.009,1)),(.42,(.53,.19,.035,1)),(.63,(.82,.39,.095,1)),(.85,(.96,.59,.23,1))]
 for i,(pos,col) in enumerate(colors):
  e=ramp.color_ramp.elements[0] if i==0 else ramp.color_ramp.elements.new(pos); e.position=pos; e.color=col
 l.new(noise.outputs['Fac'],ramp.inputs[0]); l.new(ramp.outputs['Color'],p.inputs['Base Color'])
 for e in ramp.color_ramp.elements:
  e.color=(e.color[0]*.6,e.color[1]*.32,e.color[2]*.16,1)
 fine=n.new('ShaderNodeTexNoise'); fine.inputs['Scale'].default_value=145; fine.inputs['Detail'].default_value=3; l.new(tex.outputs['Object'],fine.inputs['Vector'])
 bump=n.new('ShaderNodeBump'); bump.inputs['Strength'].default_value=.24; bump.inputs['Distance'].default_value=.025; l.new(fine.outputs['Fac'],bump.inputs['Height']); l.new(bump.outputs[0],p.inputs['Normal'])
 return m
base=pastry('金黃餅皮 • 微孔與烘烤斑'); glaze=pastry('蛋液焦糖浮雕',True)
def mesh(name,v,f,mat):
 me=bpy.data.meshes.new(name); me.from_pydata(v,[],f); me.update(); o=bpy.data.objects.new(name,me); bpy.context.collection.objects.link(o); o.data.materials.append(mat)
 for p in me.polygons:p.use_smooth=True
 return o
# Rounded scalloped solid, with explicit top and bottom surfaces.
N=576; v=[]; f=[]
profile=[(.0,.94),(.025,.975),(.09,1.0),(.22,1.007),(.9,1.0),(1.06,.988),(1.13,.963),(1.155,.93)]
for z,s in profile:
 for j in range(N):
  a=2*pi*j/N; r=(3+.095*cos(24*a))*s; v.append((r*cos(a),r*sin(a),z))
for k in range(len(profile)-1):
 for j in range(N):
  q=k*N+j; q2=k*N+(j+1)%N; f.append((q,q2,q2+N,q+N))
f.append(tuple(reversed(range(N)))); f.append(tuple((len(profile)-1)*N+j for j in range(N)))
body=mesh('月餅 • 二十四瓣餅身',v,f,base)
def tube(name,pts,r=.055,mat=glaze):
 cu=bpy.data.curves.new(name,'CURVE'); cu.dimensions='3D'; cu.resolution_u=16; cu.bevel_depth=r; cu.bevel_resolution=4
 sp=cu.splines.new('POLY'); sp.points.add(len(pts)-1)
 for p,co in zip(sp.points,pts):p.co=(*co,1)
 ob=bpy.data.objects.new(name,cu); bpy.context.collection.objects.link(ob); ob.data.materials.append(mat); return ob
for r,z,w in [(1.39,1.23,.069),(1.50,1.19,.04),(2.88,1.17,.065)]:
 tube('模壓環框',[( (r+(.065*cos(24*a) if r>2 else 0))*cos(a),(r+(.065*cos(24*a) if r>2 else 0))*sin(a),z) for a in [i*2*pi/576 for i in range(577)]],w)
def petal(cx,cy,ang,length,width):
 vv=[]; ff=[]; nu=24; nv=20
 for i in range(nu+1):
  t=i/nu; x=.035+length*t; w=width*(sin(pi*t)**.65)
  for j in range(nv+1):
   s=-pi/2+pi*j/nv; y=w*sin(s); z=1.19+.19*(sin(pi*t)**.6)*cos(s)
   # A central crease and two fine moulded veins.
   z-=.026*math.exp(-(y/.026)**2)*sin(pi*t)
   vv.append((cx+x*cos(ang)-y*sin(ang),cy+x*sin(ang)+y*cos(ang),z))
 for i in range(nu):
  for j in range(nv):
   q=i*(nv+1)+j; ff.append((q,q+1,q+nv+2,q+nv+1))
 ob=mesh('花瓣 • 壓紋',vv,ff,glaze); so=ob.modifiers.new('浮雕厚度','SOLIDIFY'); so.thickness=.055
def sphere(name,loc,scale,mat):
 bpy.ops.mesh.primitive_uv_sphere_add(segments=24,ring_count=12,location=loc); o=bpy.context.object; o.name=name; o.scale=scale; o.data.materials.append(mat)
 for p in o.data.polygons:p.use_smooth=True
for k in range(8):
 a=2*pi*k/8; cx=2.13*cos(a); cy=2.13*sin(a)
 for j in range(5):petal(cx,cy,a+j*2*pi/5,.44,.17)
 sphere('花心',(cx,cy,1.30),(.10,.10,.105),base)
 # Paired scrolling tendrils in the space between flowers.
 mid=a+pi/8
 for side in [-1,1]:
  pts=[]
  for i in range(100):
   t=i/99; theta=side*(t*2*pi*1.12); rr=.43*(1-t)+.035
   x=2.15+rr*cos(theta); y=side*.12+rr*sin(theta)
   pts.append((x*cos(mid)-y*sin(mid),x*sin(mid)+y*cos(mid),1.22+.03*sin(t*pi)))
  tube('卷草浮雕',pts,.067)
font=bpy.data.fonts.load('C:/Windows/Fonts/kaiu.ttf')
for char,y in [('中',.55),('秋',-.57)]:
 cu=bpy.data.curves.new('中秋書法','FONT'); cu.body=char; cu.font=font; cu.align_x='CENTER'; cu.align_y='CENTER'; cu.size=1.12; cu.extrude=.09; cu.bevel_depth=.024; cu.bevel_resolution=3
 ob=bpy.data.objects.new('浮雕字 • '+char,cu); bpy.context.collection.objects.link(ob); ob.location=(0,y,1.17); ob.data.materials.append(glaze)
for x in [-1.0,1.0]:tube('中框直飾',[(x,-.79,1.22),(x,.79,1.22)],.045)
# A dark ceramic serving plate and studio surface.
cer=bpy.data.materials.new('墨綠霧面陶瓷'); cer.diffuse_color=(.018,.035,.030,1); cer.use_nodes=True; cer.node_tree.nodes.clear(); cp=cer.node_tree.nodes.new('ShaderNodeBsdfPrincipled'); co=cer.node_tree.nodes.new('ShaderNodeOutputMaterial'); cer.node_tree.links.new(cp.outputs[0],co.inputs[0]); cp.inputs['Base Color'].default_value=(.018,.035,.03,1); cp.inputs['Roughness'].default_value=.32
bpy.ops.mesh.primitive_cylinder_add(vertices=192,radius=3.65,depth=.14,location=(0,0,-.14)); plate=bpy.context.object; plate.name='陶瓷盤'; plate.data.materials.append(cer); mod=plate.modifiers.new('柔和盤緣','BEVEL'); mod.width=.12; mod.segments=5
for p in plate.data.polygons:p.use_smooth=True
floor=bpy.data.materials.new('暖灰背景'); floor.diffuse_color=(.12,.105,.085,1)
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.24)); bpy.context.object.data.materials.append(floor)
def aim(o,pt):o.rotation_euler=(Vector(pt)-o.location).to_track_quat('-Z','Y').to_euler()
bpy.ops.object.camera_add(location=(0,-9.7,9.4)); cam=bpy.context.object; aim(cam,(0,0,.45)); cam.data.type='ORTHO'; cam.data.ortho_scale=8.6; bpy.context.scene.camera=cam
for name,loc,power,size,col in [('主柔光',(-4,-3,7),900,5,(1,.86,.69)),('輪廓光',(3,4,6),1150,4,(1,.93,.82)),('補光',(4,-2,4),450,3,(.76,.85,1))]:
 bpy.ops.object.light_add(type='AREA',location=loc); o=bpy.context.object; o.name=name; o.data.energy=power; o.data.shape='DISK'; o.data.size=size; o.data.color=col; aim(o,(0,0,0))
sc=bpy.context.scene; sc.render.engine='CYCLES'; sc.cycles.samples=64; sc.cycles.use_denoising=True
sc.world.color=(.22,.22,.22); sc.render.resolution_x=1400; sc.render.resolution_y=1400; sc.render.resolution_percentage=100
sc.view_settings.view_transform='AgX'; sc.view_settings.look='AgX - Medium High Contrast'
# Store the source image inside the project as reference, not as a flat surface substitute.
ref=bpy.data.images.load(os.path.join(ROOT,'中秋.png')); ref.pack()
sc['說明']='依中秋.png重建：24瓣餅身、花朵卷草浮雕、中秋文字；程序式焦糖色差與微孔凹凸材質。'
bpy.ops.object.select_all(action='DESELECT'); body.select_set(True); bpy.context.view_layer.objects.active=body
for a in bpy.context.screen.areas:
 if a.type=='VIEW_3D':a.spaces.active.region_3d.view_perspective='CAMERA'

R=ROOT
if '--output-dir' in sys.argv: R=sys.argv[sys.argv.index('--output-dir')+1]
os.makedirs(R,exist_ok=True)
sc=bpy.context.scene
sc.render.engine='CYCLES'; sc.cycles.samples=8
# Export the product only, without studio geometry, cameras, or lights.
bpy.ops.object.select_all(action='DESELECT')
for o in list(sc.objects):
 if o.type in {'MESH','CURVE','FONT'} and o.name!='陶瓷盤' and not (o.type=='MESH' and max(o.dimensions)>50):o.select_set(True)
bpy.context.view_layer.objects.active=next(o for o in sc.objects if o.select_get())
bpy.ops.object.convert(target='MESH')
bpy.ops.object.join(); cake=bpy.context.object; cake.name='Mooncake_Baked'
bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
bpy.ops.object.mode_set(mode='EDIT'); bpy.ops.mesh.select_all(action='SELECT'); bpy.ops.uv.smart_project(angle_limit=1.15,island_margin=.008); bpy.ops.object.mode_set(mode='OBJECT')

maps={}
for kind in ['BaseColor','Normal']:
 im=bpy.data.images.new('Mooncake_'+kind,width=2048,height=2048,alpha=False)
 if kind=='Normal':im.colorspace_settings.name='Non-Color'
 for m in cake.data.materials:
  n=m.node_tree.nodes.new('ShaderNodeTexImage'); n.image=im; m.node_tree.nodes.active=n
 sc.render.bake.margin=12; sc.render.bake.use_pass_direct=False; sc.render.bake.use_pass_indirect=False; sc.render.bake.use_pass_color=True
 print('BAKING '+kind,flush=True)
 bpy.ops.object.bake(type='DIFFUSE' if kind=='BaseColor' else 'NORMAL')
 im.pack(); maps[kind]=im
m=bpy.data.materials.new('Mooncake_PBR_Baked'); m.use_nodes=True; n=m.node_tree.nodes; n.clear(); l=m.node_tree.links
p=n.new('ShaderNodeBsdfPrincipled'); out=n.new('ShaderNodeOutputMaterial'); l.new(p.outputs['BSDF'],out.inputs['Surface'])
p.inputs['Roughness'].default_value=.29; p.inputs['Coat Weight'].default_value=.24; p.inputs['Coat Roughness'].default_value=.22
col=n.new('ShaderNodeTexImage'); col.image=maps['BaseColor']; l.new(col.outputs['Color'],p.inputs['Base Color'])
nor=n.new('ShaderNodeTexImage'); nor.image=maps['Normal']; nm=n.new('ShaderNodeNormalMap'); l.new(nor.outputs['Color'],nm.inputs['Color']); l.new(nm.outputs['Normal'],p.inputs['Normal'])
cake.data.materials.clear(); cake.data.materials.append(m)
for f in cake.data.polygons:f.material_index=0
plate=bpy.data.objects.get('陶瓷盤'); plate.select_set(True)
bpy.ops.object.convert(target='MESH')
bpy.ops.file.pack_all()
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(R,'中秋月餅_GLTF貼圖版.blend'))
path=os.path.join(R,'中秋月餅_含貼圖.glb')
bpy.ops.export_scene.gltf(filepath=path,export_format='GLB',use_selection=True,export_apply=True,export_cameras=False,export_lights=False)
with open(path,'rb') as f:
 f.read(12); length,typ=struct.unpack('<II',f.read(8)); doc=json.loads(f.read(length))
assert len(doc.get('images',[]))>=2
assert all('bufferView' in im for im in doc['images'])
assert any('baseColorTexture' in x.get('pbrMetallicRoughness',{}) and 'normalTexture' in x for x in doc['materials'])
print('VERIFIED embedded base color and normal textures',flush=True)

