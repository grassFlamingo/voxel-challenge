from scene_GUI import Scene
import taichi as ti
from taichi.math import *

scene = Scene(voxel_edges=0.1, exposure=3)
scene.set_floor(-1.00, (1.0, 1.0, 1.0))
#F5EEDC vec3(0.96, 0.93, 0.86)
scene.set_background_color((0.96, 0.93, 0.86))
scene.set_directional_light((1, 1, -1), 0.2, (0.96, 0.93, 0.86))


@ti.func
def sot(a, b):
    if b < a: a, b = b, a
    return a, b

@ti.func
def mk_b(center, box, color, cnoise=.1, p=1.0,t=1):
    ll, rr = center - box, center + box
    for x, y, z in ti.ndrange(sot(ll[0], rr[0]), sot(ll[1], rr[1]), sot(ll[2], rr[2])):
        if ti.random() < p:
            scene.set_voxel(vec3(x, y, z), t, color + cnoise * ti.random())

@ti.func
def liner_c(c1, c2, alpha):
    return c1 * alpha + (1-alpha)*c2

@ti.kernel
def initialize_voxels():
    #004F4D vec3(0.00, 0.31, 0.30)
    for r in range(0, 64*16):
        t = ti.max(r,16*16) / 16.0
        x = t * ti.sin(pi + t * pi * 3 / 64.0)
        z = t * ti.cos(pi + t * pi * 3 / 64.0)
        for h in range(3):
            scene.set_voxel(vec3(x, -t+h, z), 1, vec3(0.00, 0.31, 0.30) + 0.1 * ti.random())
        for y in range(-63, int(-t)):
            edge = vec3(x, y, z)
            if ti.random() < 0.6:
                scene.set_voxel(edge, 1, vec3(0.00, 0.31, 0.30) + 0.1 * ti.random())

                for l in range(0, 64):
                    if ti.random() < 0.6:
                        pp = vec3(x*l/64, y, z*l/64)
                        scene.set_voxel(pp, 1, vec3(0.00, 0.31, 0.30) + 0.1*ti.random())
   
    for x, y, z in ti.ndrange((-16,16), (-64, 32), (-16, 16)):
        if ti.random() < 0.8 and x*x + z*z < 16*16/2:
            #735B58 vec3(0.45, 0.36, 0.35)
            scene.set_voxel(vec3(x, y, z), 1, vec3(0.45, 0.36, 0.35))

    for x, y, z in ti.ndrange((-64, 64), (32, 64), (-64, 64)):
        r = 2*(32 - y)
        if ti.random() < 0.01 and x*x + z*z < r*r:
            mk_b(ivec3(x, 64+31-5 - y, z), ivec3(5, 5, 5), vec3(0,0.8,0), p=0.1)

    # add drops
    wcolor = vec3(0.00, 0.36, 0.33) #005C53 vec3(0.00, 0.36, 0.33)
    for x, z in ti.ndrange((-64, 64), (-64, 64)):
        for y in range(-63, 64):
            mat, color = scene.get_voxel(vec3(x,y,z))
            if mat == 1:
                scene.set_voxel(vec3(x,-64,z), 1, liner_c(color, wcolor, ti.random()))
                break

initialize_voxels()

scene.finish()
