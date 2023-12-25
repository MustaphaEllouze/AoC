from typing import Any, Self
from aoc.tools import ABCSolver
from dataclasses import dataclass
from functools import partial
from scipy.optimize import minimize
import sympy as sp

@dataclass
class Hail:
    px:int
    py:int
    pz:int
    vx:int
    vy:int
    vz:int

    def point(self, parameter:float)->tuple[float, float, float]:
        return (
            self.px+parameter*self.vx,
            self.py+parameter*self.vy,
            self.pz+parameter*self.vz,
        )

@dataclass
class Vector:
    x:int ; y:int ; z:int

    @classmethod
    def cross_product(cls, v1:Self, v2:Self):
        return Vector(
            x = v1.y*v2.z-v2.y*v1.z,
            y = v1.z*v2.x-v2.z*v1.x,
            z = v1.x*v2.y-v2.x*v1.y,
        )
    
    @property
    def norm(self)->float:
        return (self.x**2+self.y**2+self.z**2)**0.5

def hail_cross(
        hail1:Hail, 
        hail2:Hail,
        dont_ignore_z:bool=False,
    )->tuple[float, float, bool]:
    """
    Args:
        hail1 (Hail): 
        hail2 (Hail):
        dont_ignore_z (bool, optional): Defaults to False.

    Returns:
        tuple[int, int, bool]: paramter cross 1, parameter cross 2, does cross
    """
    v1 = Vector(
        hail1.vx, 
        hail1.vy, 
        hail1.vz*int(dont_ignore_z)
    )
    v2 = Vector(
        hail2.vx, 
        hail2.vy,
        hail2.vz*int(dont_ignore_z)
    )
    px1,py1,pz1,px2,py2,pz2 = (
        hail1.px, hail1.py, hail1.pz*int(dont_ignore_z), 
        hail2.px, hail2.py, hail2.pz*int(dont_ignore_z), 
    )
    cross_product = Vector.cross_product(v1,v2)
    if cross_product.norm <1e-12 : 
        # Hypothèse : les droites ne peuvent pas être confondues
        # AV VERIFIER
        return 0, 0, False
    else:
        det_xy = -(v1.x*v2.y - v2.x*v1.y)
        det_yz = -(v1.y*v2.z - v2.y*v1.z)
        det_zx = -(v1.z*v2.x - v2.z*v1.x)

        cramer_xy_prime = v1.x*(py2-py1)-v1.y*(px2-px1)
        cramer_yz_prime = v1.y*(pz2-pz1)-v1.z*(py2-py1)
        cramer_zx_prime = v1.z*(px2-px1)-v1.x*(pz2-pz1)
        
        cramer_xy_nprim = -v2.x*(py2-py1)+v2.y*(px2-px1)
        cramer_yz_nprim = -v2.y*(pz2-pz1)+v2.z*(py2-py1)
        cramer_zx_nprim = -v2.z*(px2-px1)+v2.x*(pz2-pz1)

        if abs(det_xy)>1e-12:
            t_nprim = -cramer_xy_nprim/det_xy
            t_prime = cramer_xy_prime/det_xy
            u1,l1,u2,l2 = pz1,v1.z, pz2,v2.z
        elif abs(det_yz)>1e-12:
            t_nprim = -cramer_yz_nprim/det_yz
            t_prime = cramer_yz_prime/det_yz
            u1,l1,u2,l2 = px1,v1.x, px2,v2.x
        elif abs(det_zx)>1e-12:
            t_nprim = -cramer_zx_nprim/det_zx
            t_prime = cramer_zx_prime/det_zx
            u1,l1,u2,l2 = py1,v1.y, py2,v2.y
        else : raise NotImplementedError()

        if abs(u1+l1*t_nprim - u2+l2*t_prime) > 1e-12 : return 0,0,False
        else:
            return t_nprim, t_prime, True

def do_intersect_in_future(
        hail1:Hail, 
        hail2:Hail, 
        dont_ignore_z:bool=False
    )->tuple[float, float, bool]:
    t,tp,test = hail_cross(
        hail1=hail1, 
        hail2=hail2, 
        dont_ignore_z=dont_ignore_z,
    )
    return (t,tp,test and t>=0 and tp>=0)

class Solver(ABCSolver):

    def solve(self, part2: bool = False) -> tuple[Any, str]:

        hailstones = [
            Hail(*[int(e) for e in line.split([',','@'])]) 
            for line in self.data
        ]

        if not part2 : 

            test_mini = 200000000000000
            test_maxi = 400000000000000

            result = 0

            for i,haili in enumerate(hailstones):
                for hailj in hailstones[i+1:]:
                    # print(haili)
                    # print(hailj)
                    t,tp,test = do_intersect_in_future(haili, hailj, part2)
                    if test :
                        if test_mini<=haili.point(t)[0]<=test_maxi \
                        and test_mini<=haili.point(t)[1]<=test_maxi: 
                            result += 1

            return 'No structure', result

        else:
            # On récupère les trois premières droites et on espère qu'on 
            #   puisse trouver une solution qui fonctionne avec ces droites là
            #   et que cette solution soit unique.
            # Ensuite, on vérifie que cette solution marche bien avec 
            #   toutes les autres droites.
           
            hail0, hail1, hail2 = tuple(hailstones[0:3])
            x0=hail0.px ; y0=hail0.py ; z0=hail0.pz ;
            x1=hail1.px ; y1=hail1.py ; z1=hail1.pz ;
            x2=hail2.px ; y2=hail2.py ; z2=hail2.pz ;
            lx0=hail0.vx; ly0=hail0.vy; lz0=hail0.vz;
            lx1=hail1.vx; ly1=hail1.vy; lz1=hail1.vz;
            lx2=hail2.vx; ly2=hail2.vy; lz2=hail2.vz;

            # def solve_function(
            #         # x0: int, x1: int, x2: int,
            #         # y0: int, y1: int, y2: int,
            #         # z0: int, z1: int, z2: int,
            #         # lx0:int, lx1:int, lx2:int,
            #         # ly0:int, ly1:int, ly2:int,
            #         # lz0:int, lz1:int, lz2:int,
            #         # xb: int, yb: int, zb: int,
            #         # lxb:int, lyb:int, lzb:int,
            #         # t0: int, t1: int, t2: int, 
            #         input:tuple[int],
            # )->float:
            #     xb,yb,zb,lxb,lyb,lzb,t0,t1,t2 = input
            #     a01 = (x0+lx0*t0-xb-lxb*t0)
            #     a02 = (y0+ly0*t0-yb-lyb*t0)
            #     a03 = (z0+lz0*t0-zb-lzb*t0)
            #     a04 = (x1+lx1*t1-xb-lxb*t1)
            #     a05 = (y1+ly1*t1-yb-lyb*t1)
            #     a06 = (z1+lz1*t1-zb-lzb*t1)
            #     a07 = (x2+lx2*t2-xb-lxb*t2)
            #     a08 = (y2+ly2*t2-yb-lyb*t2)
            #     a09 = (z2+lz2*t2-zb-lzb*t2)
            #     all_terms = (a01,a02,a03,a04,a05,a06,a07,a08,a09)
            #     return sum([e**2 for e in all_terms])

            # x0 = sp.Symbol('x0')
            # y0 = sp.Symbol('y0')
            # z0 = sp.Symbol('z0')
            # x1 = sp.Symbol('x1')
            # y1 = sp.Symbol('y1')
            # z1 = sp.Symbol('z1')
            # x2 = sp.Symbol('x2')
            # y2 = sp.Symbol('y2')
            # z2 = sp.Symbol('z2')

            # lx0 = sp.Symbol('lx0')
            # ly0 = sp.Symbol('ly0')
            # lz0 = sp.Symbol('lz0')
            # lx1 = sp.Symbol('lx1')
            # ly1 = sp.Symbol('ly1')
            # lz1 = sp.Symbol('lz1')
            # lx2 = sp.Symbol('lx2')
            # ly2 = sp.Symbol('ly2')
            # lz2 = sp.Symbol('lz2')

            xb = sp.Symbol('xb')
            yb = sp.Symbol('yb')
            zb = sp.Symbol('zb')

            lxb = sp.Symbol('lxb')
            lyb = sp.Symbol('lyb')
            lzb = sp.Symbol('lzb')
            
            t0 = sp.Symbol('t0')
            t1 = sp.Symbol('t1')
            t2 = sp.Symbol('t2')

            eq1 = (x0+lx0*t0-xb-lxb*t0)
            eq2 = (y0+ly0*t0-yb-lyb*t0)
            eq3 = (z0+lz0*t0-zb-lzb*t0)
            eq4 = (x1+lx1*t1-xb-lxb*t1)
            eq5 = (y1+ly1*t1-yb-lyb*t1)
            eq6 = (z1+lz1*t1-zb-lzb*t1)
            eq7 = (x2+lx2*t2-xb-lxb*t2)
            eq8 = (y2+ly2*t2-yb-lyb*t2)
            eq9 = (z2+lz2*t2-zb-lzb*t2)

            solution = sp.solve(
                [eq1,eq2,eq3,eq4,eq5,eq6,eq7,eq8,eq9],
                xb,yb,zb,lxb,lyb,lzb,t0,t1,t2,
            )

            return 0,sum(solution[0][:3])

    
    def generate_view(self, structure: Any) -> str:
        return super().generate_view(structure)
        

# print(
#     hail_cross(
#         Hail(1.2, 2.0, 0.0, -1.0, 0.2, 0.0),
#         Hail(2.1, 1.2, 0.0, 1.0, 1.2, 0.0),
#         dont_ignore_z=True,
#     )
# )