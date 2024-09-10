from math import sqrt, cos, sin, asin, radians, degrees, isclose
import numpy as np
import matplotlib.pyplot as plt
from copy import copy
from itertools import combinations

class Vertex:
    def __init__(self, x, y=None, z=0):
        if type(x)==int and type(y)==int:
            self.x = x
            self.y = y
            self.z = z
            self.connected_points=[]
        elif type(x)==np.ndarray:
            if y!=None:
                raise TypeError()
            if x.shape==(3,):
                assert(len(x)==3)
                self.x = x[0]
                self.y = x[1]
                self.z = x[2]
                self.connected_points=[]
            elif x.shape==(1,3):
                # this is probably a bit naughty tbh but I'll let it pass 
                self.x = x[0][0]
                self.y = x[0][1]
                self.z = x[0][2]
                self.connected_points=[]
            elif x.shape==(3,1):
                self.x = x[0][0]
                self.y = x[1][0]
                self.z = x[2][0]
                self.connected_points=[]
            else:
                print("Bad stuff! This matrix shape is unexpected")
                print(x)
                raise ValueError
       
    def distance(self, b):
        return sqrt((self.x-b.x)**2 +
                    (self.y-b.y)**2 +
                    (self.z-b.z)**2)
    
    def __add__(self, b):
        if type(b)==Vertex:
            return Vertex(self.x+b.x, self.y+b.y, self.z+b.z)
        elif type(b)==np.ndarray:
            return Vertex(self.x+b[0], self.y+b[1], self.z+b[0])
        else:
            raise TypeError()
        
    def __sub__(self, b):
        if type(b)==Vertex:
            return Vertex(self.x-b.x, self.y-b.y, self.z-b.z)
        elif type(b)==np.ndarray:
            return Vertex(self.x-b[0], self.y-b[1], self.z-b[0])
        else:
            raise TypeError()
        
    def to_np_vec(self):
        return np.array([[self.x], [self.y], [self.z]])
    
    def __repr__(self):
        return f"Vertex({self.x}, {self.y}, {self.z}), with {len(self.connected_points)} connections"

def is_good_triangle(corners):
    # a good triangle is equilateral with side lenghths 2
    assert(len(corners)==3)

    return (isclose(corners[0].distance(corners[1]), 2, abs_tol=0.001) and
            isclose(corners[1].distance(corners[2]), 2, abs_tol=0.001) and
            isclose(corners[2].distance(corners[0]), 2, abs_tol=0.001))


def generate_goldberg_triangle (m, n):
    A=Vertex(0,0,0)

    xb=m+ n/2 
    yb=(sqrt(3)*n)/2
    print(f"B: ({xb}, {yb})")
    B=Vertex(xb, yb, 0) # quick mafs

    #trust me, I used a ruler and everything
    l=sqrt(xb**2 + yb**2)
    theta = asin(yb/l)
    xc=sin(radians(90)-theta-radians(60))*l
    yc=cos(radians(90)-theta-radians(60))*l

    C=Vertex(xc, yc, 0)
    return (A,B, C)

def point_in_triangle(pt, A, B, C):
    # shamelessly stolen from https://stackoverflow.com/questions/2049582/how-to-determine-if-a-point-is-in-a-2d-triangle
    area=0.5 *(-B.y*C.x + A.y*(-B.x + B.x) + A.x*(B.y - C.y) + B.x*C.y)
    s = 1/(2*area)*(A.y*C.x - A.x*C.y + (C.y - A.y)*pt.x + (A.x - C.x)*pt.y)
    t = 1/(2*area)*(A.x*B.y - A.y*B.x + (A.y - B.y)*pt.x + (B.x - A.x)*pt.y)
    return s>0 and t>0 and 1-s-t>0

def generate_trimap(m: int, n: int) ->list:
    # generates a network of hexagons which subdivide an equilateral triangle
    # see https://royalsocietypublishing.org/doi/10.1098/rsos.220675 diagram 2(a)

    # we are thinking of vertices as "columms".  the vertical spacing between points within a column alternates betweenr 1/sqrt(3) and 2/sqrt(3)
    # moving from one column to the next we either go diagonally up (abs val is 1/root3) or diagonally down
    
    # the jank way I'm going to do this is just enumerating the hexagon points in a m+n*m+n box, and checking if it's in the triangle
    # I could probably do a DFS, which would also let me link up my vertices with edges... oh well...
    triangle=generate_goldberg_triangle(m, n)

    invroot3=1/sqrt(3) # in all of this jank, now is defnitiely the time to be efficient and precompute this... 
    trimap=[]
    
 #   Y Y Y
 #   | | | |
 #   ⅄ ⅄ ⅄ ⅄
 #  | | | |
 #   Y Y Y
    # this is a horrible name.  Basically some vertices look like Y, others look like ⅄, and we need to know which one we are starting with because the iteration behaviour depends on it.
    column_startpoint_is_y_shaped=True
    column_startpoint=Vertex(0, -invroot3, 0)

    while column_startpoint.x < m+n:
        print(f"Starting new column, with a {'Y-shaped' if column_startpoint_is_y_shaped else 'lambda-shaped'} starting point {column_startpoint.x}, {column_startpoint.y}")
        
        candidate=copy(column_startpoint)
        candidate_is_y_shaped=column_startpoint_is_y_shaped

        while candidate.y<m+n:
            print(f"Checking candidate {candidate.x}, {candidate.y}, {'Y-shaped' if candidate_is_y_shaped else 'lambda-shaped'} ")
            if point_in_triangle(candidate, triangle[0], triangle[1], triangle[2]):
                trimap.append(copy(candidate))
                print(f"determined {candidate.x}, {candidate.y} to be   IN   triangle")
            else:
                print(f"determined {candidate.x}, {candidate.y} to be OUT of triangle")
            if candidate_is_y_shaped:
                candidate.y+=2*invroot3
            else:
                candidate.y+=invroot3
            candidate_is_y_shaped=not candidate_is_y_shaped
        
        if column_startpoint_is_y_shaped:
            column_startpoint.x+=0.5
            column_startpoint.y+=1/(2*sqrt(3))
            column_startpoint_is_y_shaped=False
        else:
            column_startpoint.x+=0.5
            column_startpoint.y-=1/(2*sqrt(3)) 
            column_startpoint_is_y_shaped=True
    print(trimap)

    return trimap

def renormalise_from_triangle(p: Vertex, b:Vertex):
    #The coordinate system we used to build our Goldberg triangle is not the one we want to use for constructing our icosohedron.
    # This rotates p around the axis and then translates it so that the centre of the triangle defined by m and n is on the origin
    # b is the second vector of the goldberg triangle(counting anti-clockwise), p is the point to be transformed
    # Finally, the point gets scaled such that the side length of the triangle is 2.  This ends up being useful for a nice neat expression of coordinates of the vertices of an icosohedron.

    l = sqrt(b.x**2 + b.y**2)
    print(f"L: {l}")
    theta=asin(b.y/l)

    T = np.array([[cos(theta), sin(theta)],
                 [-sin(theta), cos(theta)]])   # variant of the usual rotation matrix for clockwise rotation
    
    p_vec=np.array([[p.x],
                   [p.y]])

    p_vec=np.matmul(T,  p_vec)      # rotation
    p_vec[0][0]-=l/2                # translation in x
    p_vec[1][0]-=l/(2*sqrt(3))      # translation in y
    
    p_vec[0][0]/=(l/2)              # scale to triangl side length 2 
    p_vec[1][0]/=(l/2)              # 


    return Vertex(p_vec[0][0], p_vec[1][0],0)

def build_normalised_trimap(m, n):
    tri_points=generate_goldberg_triangle(m,n)
    new_tri=[renormalise_from_triangle(p, tri_points[1]) for p in tri_points]

    points=generate_trimap(m, n) 

    for i in range(len(points)):
        points[i]=renormalise_from_triangle(points[i], tri_points[1])

    return(new_tri, points)

def get_normalisation_matrices(A: Vertex, B: Vertex, C: Vertex) -> tuple[np.ndarray[float], np.ndarray[float]]:
    # returns a vector and a matrix such that applying the rotation described by the matrix, and then adding the translation, will map a normalised triangle onto ABC!
    # Will break horrendously if side lengths are not 2.
    # I should probably calculate and assert the side length... oh well.
    l=2

    trans_vec=np.array([[-A.x], [-A.y], [-A.z]])

    A_after_trans=A.to_np_vec()+trans_vec
    B_after_trans=B.to_np_vec()+trans_vec
    C_after_trans=C.to_np_vec()+trans_vec

    # Rotation 1 - rotating b into  the xy plane, around the y axis
    # Trust me, I used paper and a pen.
    cos_theta=B_after_trans[0][0]/(sqrt(B_after_trans[2][0]**2+B_after_trans[0][0]**2))
    sin_theta=B_after_trans[2][0]/(sqrt(B_after_trans[2][0]**2+B_after_trans[0][0]**2))
    rot1_matr=np.array([[ cos_theta,   0.,   sin_theta ],
                        [0.,            1.,   0.         ],
                        [-sin_theta,   0.,   cos_theta ]])
    
    
    B_after_Rot_1 = rot1_matr @ B_after_trans   # @ is a spefical infix operator for mat mul!
    C_after_Rot_1 = rot1_matr @ C_after_trans
    # A should be unaffected as it's at the origin.


    # rotation 2 - bring b onto the x axis by a rotation around the z axis
    # note my alpha is the opposite direction to the classic matrix - so used sin(-a) =-sin(a) 
    cos_alpha=B_after_Rot_1[0][0]/l
    sin_alpha=B_after_Rot_1[1][0]/l

    rot2_matr=np.array([[ cos_alpha,   sin_alpha,   0 ],
                        [ -sin_alpha,   cos_alpha,    0 ],
                        [ 0,           0,            1 ]])
    

    B_after_Rot_2= rot2_matr @ B_after_Rot_1
    C_after_Rot_2= rot2_matr @ C_after_Rot_1
    # again, A should be unaffected

    PC=(sqrt(3)*l)/2 
    sin_beta=C_after_Rot_2[2][0]/PC
    cos_beta=C_after_Rot_2[1][0]/PC


    rot3_matr=np.array([[ 1,           0,            0      ],
                        [ 0,           cos_beta,  sin_beta ],
                        [ 0,           -sin_beta,  cos_beta ]])
    
    #B should really be unaffected, but oh well, lets check
    B_after_Rot_3= rot3_matr @ B_after_Rot_2
    C_after_Rot_3 = rot3_matr @ C_after_Rot_2


    overall_rot= rot3_matr @ rot2_matr @ rot1_matr
    denormalise_rot = np.linalg.inv(overall_rot)
    denormalise_trans = -1 * trans_vec
    return  (denormalise_rot, denormalise_trans)

def buil_icoso_map (m:int, n:int) -> list[Vertex]:
    φ = (1+sqrt(5))/2
    vertices=(Vertex(φ, 1,0), 
              Vertex(φ, -1, 0),
                Vertex(-φ, -1,0),
                Vertex(-φ, 1,0),
                Vertex(1, 0,φ),
                Vertex(-1, 0,φ),
                Vertex(-1, 0,-φ),
                Vertex(1, 0,-φ),
                Vertex(0, φ, 1),
                Vertex(0, φ, -1),
                Vertex(0, -φ, -1),
                Vertex(0, -φ, 1))
    
    triangles=[]#TODO

    norm_tri, normalised_points=build_normalised_trimap(m, n)
    
    icoso_points=[]

    for tri in triangles:
        rot, trans =get_normalisation_matrices(tri)
        for point in normalised_points:
            icoso_points.append(Vertex((rot @ point.to_np_vec)+trans))

def nearest_neighbours(p: Vertex, points: list[Vertex], n=1) -> list[Vertex]:
    #find the n points closest to p
    assert(len(points))>n
    assert(n>0)
    def key(b):
        return p.distance(b)
    points.sort(key)

    #only gotta check points[0] because a point is always going to be its own nearest neighbour
    if points[0] is p:
        return points[1:n+1]
    else:
        return points[:n]            
    

def connect_icoso_points(icoso_points: list[Vertex]):
    for point in icoso_points:
        point.connected_points+=nearest_neighbours(point, icoso_points, 3-len(point.connected_points))





"""
def build_icoso(m,n):
    for tri in triangles:
        icoso_map=[]
        trans=<the translation vector to bring a point of tri to the origin>
        rot=<the matrix by which tri would have to be rotated in order to normalise it - no idea how >
        rerot=np.linalg.inv(rot)
        for point in tri_map_points:
            old_point=[point.x, point.y, point.z]
            new_point=np.subtract(np.matmul(old_point, rerot), trans)
            icoso_map.append(Vertex(new_point[0], new_point[1], new_point[2]))
            

    tri, points = build_normalised_trimap(m,n)
    for 
"""




