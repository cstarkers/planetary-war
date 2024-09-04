from math import sqrt, cos, sin, asin, radians, degrees
import matplotlib.pyplot as plt
import copy

class Vertex:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.connected_points=[]

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
    s = 1/(2*area)*(A.y*C.x - A.x*C.y + (C.y - A.y)*pt.x + (A.x - C.x)*pt.x)
    t = 1/(2*area)*(A.x*B.y - A.y*B.x + (A.y - B.y)*pt.x + (B.x - A.x)*pt.x)

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
        
        candidate=copy.copy(column_startpoint)
        candidate_is_y_shaped=column_startpoint_is_y_shaped

        while candidate.y<m+n:
            print(f"Checking candidate {candidate.x}, {candidate.y}, {'Y-shaped' if candidate_is_y_shaped else 'lambda-shaped'} ")
            if point_in_triangle(candidate, triangle[0], triangle[1], triangle[2]):
                trimap.append(copy.copy(candidate))
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

def test_plot_tri(m,n):
    # jsut a little test
    points=generate_goldberg_triangle(m,n)
    xpoints=[p.x for p in points]
    ypoints=[p.y for p in points]
    xpoints.append(0)
    ypoints.append(0)
    plt.plot(xpoints, ypoints)
    plt.show()

def test_plot_hexmap(m,n):
    # jsut a little test
    tri_points=generate_goldberg_triangle(m,n)
    tri_xpoints=[p.x for p in tri_points]
    tri_ypoints=[p.y for p in tri_points]
    tri_xpoints.append(0)
    tri_ypoints.append(0)
    plt.plot(tri_xpoints, tri_ypoints)

    points= generate_trimap(m, n) 
    xpoints=[p.x for p in points]
    ypoints=[p.y for p in points]
    for i in range(len(xpoints)):
        print(f"X:{xpoints[i]}, Y:{ypoints[i]}")

    plt.plot(xpoints, ypoints, "x")
    plt.show()


"""
def position_on_icosohedron(trimap_points) -> list:
    # positions the trimap in 3d space, mapped onto the faces of an icosohedron
    # see https://royalsocietypublishing.org/doi/10.1098/rsos.220675 diagram 2(a)
    return icoso_points

def join_trimaps():
    # joins the trimap corners up
    # see https://royalsocietypublishing.org/doi/10.1098/rsos.220675 diagram 2(c)
    return icoso_points

def project_to_sphere(points):
    return points
    """


test_plot_hexmap(4,2)





