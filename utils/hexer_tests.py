from hexer import *

# --- test plots ---
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
    plt.gca().set_aspect('equal')
    plt.show()


def test_plot_rotation(m,n):
    # jsut a little test
    tri_points=generate_goldberg_triangle(m,n)
    new_tri=[]
    for p in tri_points:
        new_tri.append(renormalise_from_triangle(p, tri_points[1]))

    tri_xpoints=[p.x for p in new_tri]
    tri_ypoints=[p.y for p in new_tri]
    tri_xpoints.append(tri_xpoints[0])
    tri_ypoints.append(tri_ypoints[0])
    plt.plot(tri_xpoints, tri_ypoints)
    plt.gca().set_aspect('equal')
    plt.show()



def test_plot_normalisation(m,n):
    # jsut a little test
    tri_points, points=build_normalised_trimap(m, n)
    tri_xpoints=[p.x for p in tri_points]
    tri_ypoints=[p.y for p in tri_points]
    tri_xpoints.append(tri_xpoints[0])
    tri_ypoints.append(tri_ypoints[0])
    plt.plot(tri_xpoints, tri_ypoints)

    xpoints=[p.x for p in points]
    ypoints=[p.y for p in points]
    for i in range(len(xpoints)):
        print(f"X:{xpoints[i]}, Y:{ypoints[i]}")

    plt.plot(xpoints, ypoints, "x")
    plt.gca().set_aspect('equal')
    plt.show()

    plt.gca().set_aspect('equal')
    plt.show()


def test_plot_denormalisation():
    # tests whether get_denornalistaion_matrices can reconstruct a rotation and trnaslation matrix
    test_trans=np.array([[4], [3.5], [17]])
    
    # this equates to 37 degrees around [0.7, 0.3, 0.648...]
    test_denorm_rot= np.array([[0.8973041, -0.3477342,  0.2718939],
                        [0.4323072,  0.8167583, -0.3821208],
                        [-0.0891951,  0.4604203,  0.8832086 ]])
    test_A=Vertex((test_denorm_rot @ np.array([[0],[0],[0]])) + test_trans)
    test_B=Vertex((test_denorm_rot @ np.array([[2],[0],[0]])) + test_trans)
    test_C=Vertex((test_denorm_rot @ np.array([[1],[sqrt(3)],[0]])) + test_trans)

    # sometimes you gotta test the test
    assert(is_good_triangle((test_A, test_B, test_C)))

    calced_denorm_rot, calced_trans = get_normalisation_matrices(test_A, test_B, test_C)

    rot_good=False

    if np.allclose(calced_denorm_rot, test_denorm_rot, atol=0.001):
        print("Rot was good!")
        rot_good=True
    else:
        print(f"Rot was bad :( \n The calculated rotation matrix for denormalisation: \n{calced_denorm_rot}\n")
        print(f"The denormalisation matrix used for generating the test case: \n{test_denorm_rot}\n")

    if np.allclose(calced_trans, test_trans):
        print("Trans was good!")
        if rot_good:
            print("🎉🎉🎉Holy shit you did it 🎉🎉🎉🎉")
    else:
        print(f"Trans was bad :( \n The calculated Trans was: \n{calced_trans}")

def test_plot_denormalisation_x():
    angle = 1 # radians
    test_denorm_rot= np.array([[1, 0,  0 ],
                        [0, cos(angle), -sin(angle)],
                        [0, sin(angle), cos(angle) ]])
    
    test_A=Vertex(test_denorm_rot @ np.array([[0],[0],[0]])) 
    test_B=Vertex(test_denorm_rot @ np.array([[2],[0],[0]])) 
    test_C=Vertex(test_denorm_rot @ np.array([[1],[sqrt(3)],[0]])) 
    
    
    calced_denorm_rot, calced_trans = get_normalisation_matrices(test_A, test_B, test_C)

    rot_good=False

    if np.allclose(calced_denorm_rot, test_denorm_rot):
        print("Rot was good!")
        rot_good=True
    else:
        print(f"Rot was bad :( \n The calculated rotation matrix for denormalisation: \n{calced_denorm_rot}\n")
        print(f"The denormalisation matrix used for generating the test case: \n{test_denorm_rot}\n")


    

def test_plot_denormalisation_y():
    angle = 1 # radians
    test_denorm_rot= np.array([[cos(angle), 0, sin(angle)],
                        [0, 1, 0],
                        [-sin(angle), 0,  cos(angle) ]])
    
    test_A=Vertex(test_denorm_rot @ np.array([[0],[0],[0]])) 
    test_B=Vertex(test_denorm_rot @ np.array([[2],[0],[0]])) 
    test_C=Vertex(test_denorm_rot @ np.array([[1],[sqrt(3)],[0]])) 
    
    

    calced_denorm_rot, calced_trans = get_normalisation_matrices(test_A, test_B, test_C)

    if np.allclose(calced_denorm_rot, test_denorm_rot):
        print("Rot was good!")
 
    else:
        print(f"Rot was bad :( \n The calculated rotation matrix for denormalisation: \n{calced_denorm_rot}\n")
        print(f"The denormalisation matrix used for generating the test case: \n{test_denorm_rot}\n")

    

def test_plot_denormalisation_z():
    angle = 1 # radians
    test_denorm_rot= np.array([[cos(angle), -sin(angle),0 ],
                        [ sin(angle), cos(angle), 0 ],
                        [0, 0, 1]])
    
    test_A=Vertex(test_denorm_rot @ np.array([[0],[0],[0]])) 
    test_B=Vertex(test_denorm_rot @ np.array([[2],[0],[0]])) 
    test_C=Vertex(test_denorm_rot @ np.array([[1],[sqrt(3)],[0]])) 

    
    calced_denorm_rot, calced_trans = get_normalisation_matrices(test_A, test_B, test_C)

    

    if np.allclose(calced_denorm_rot, test_denorm_rot):
        print("Rot was good!")
        
    else:
        print(f"Rot was bad :( \n The calculated rotation matrix for denormalisation: \n{calced_denorm_rot}\n")
        print(f"The denormalisation matrix used for generating the test case: \n{test_denorm_rot}\n")





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


#test_plot_normalisation(4,2)

def test_denormalisations():
    print("--- TESTING Y ROTATION ---")
    test_plot_denormalisation_y()
    print("\n\n")

    print("--- TESTING Z ROTATION ---")
    test_plot_denormalisation_z()
    print("\n\n")
    print("--- TESTING X ROTATION ---")
    test_plot_denormalisation_x()
    print("\n\n")
    print("--- TESTING COMPOUND ROTATION WITH TRANSLATION ---")
    test_plot_denormalisation()

points = [Vertex(cos(radians(theta)), sin(radians(theta)), 0) for theta in range(30, 360, 30)]

geo_json_points(points)