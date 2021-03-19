from stl import mesh
import math
import numpy
import numpy as np
from matplotlib import pyplot
from mpl_toolkits import mplot3d


import open3d as o3d






def topPoints(size,f,xo,h,r):
    verticies = []
    s = np.linspace(-r,r,size)
    for i in range(int(len(s)/3)):
        for j in range(3):
            x = s[(i*3)+j]
            verticies += [[x,f(x,r),h]]
        
        
    for i in range(int(len(s)/3)):
        
        for j in range(3):
            x = s[(i*3)+j]
            verticies += [[-x,f(x,r),h]]
            
    
    for i in range(int(len(s)/3)):
        
        for j in range(3):
            x = s[(i*3)+j]
            verticies += [[-x,-f(x,r),h]]
            
            
    for i in range(int(len(s)/3)):
        
        for j in range(3):
            x = s[(i*3)+j]
            verticies += [[x,-f(x,r),h]]
    

        
    print(verticies)
    return verticies
    
    

def botumPoints(size,f,xo,r):
    verticies = []
    s = np.linspace(-r,r,size)
    for i in range(int(len(s)/3)):
        for j in range(3):
            x = s[(i*3)+j]
            verticies += [[x,f(x,r),0]]
        
        
    for i in range(int(len(s)/3)):
        
        for j in range(3):
            x = s[(i*3)+j]
            verticies += [[-x,f(x,r),0]]
    
    
    for i in range(int(len(s)/3)):
        
        for j in range(3):
            x = s[(i*3)+j]
            verticies += [[-x,-f(x,r),0]]
            
    for i in range(int(len(s)/3)):
        
        for j in range(3):
            x = s[(i*3)+j]
            verticies += [[x,-f(x,r),0]]
            
        
    return verticies
	

def makecylinder(h,r):

    circle = lambda x,r:math.sqrt(r**2-x**2)
    i=0
    size = 350
    data = numpy.zeros((size*4)+4, dtype=mesh.Mesh.dtype)
    xo = 0
    top = topPoints(size,circle,xo,h,r)
    bot = topPoints(size,circle,xo,0,r)
    #print(top)
    for i in range(size):
        tri = numpy.array([[top[i],top[i+1],bot[i]],
                          [bot[i],top[i+1],bot[i+1]],
                          [top[i+1],bot[i+2],bot[i+1]]])
                          
        tri2 = numpy.array([[bot[i],bot[i+1],top[i]],
                          [top[i],bot[i+1],top[i+1]],
                          [bot[i+2],top[i+2],top[i+1]]])
                          

        print(tri)
        print('\n')
        print(data['vectors'].shape)
        
        #print(type(data['vectors']))
        for j in range(3):
            for k in range(3):
                print(type(data['vectors'][i][j]))
                print(str(i),str(k),str(j),'\n')
                print(tri[k])
                print(tri[k][j])
                print('\n')
                data['vectors'][i][j] =  tri[k][j]
                data['vectors'][-i][j] =  tri2[k][j]
                data['vectors'][size+i][j] = (tri[k][j]*[-1,-1,1])
                data['vectors'][-(size+i)][j] = (tri2[k][j]*[-1,-1,1])
                
    data['vectors'][(-2*size)] = numpy.array([data['vectors'][0][0],
                                              data['vectors'][0][1],
                                              data['vectors'][-1][0]*[1,-1,1]])
                                              
    data['vectors'][(-2*size)-1] = numpy.array([data['vectors'][-2*size][1],
                                               data['vectors'][-2*size][0]*[ 1,-1,1],
                                               data['vectors'][-1][1]*[1,-1,1]])
    
    data['vectors'][(-2*size)-2] = numpy.array([data['vectors'][-2*size][1]*[-1,1,1],
                                               data['vectors'][-2*size][0]*[-1,1,1],
                                               data['vectors'][size][0]])
                                               
    data['vectors'][(-2*size)-3] = numpy.array([data['vectors'][size][0],
                                               data['vectors'][-2*size][0]*[-1,1,1],
                                               data['vectors'][size][1]])
    

    # Create a new plot
    
    print(data['vectors'])
    figure = pyplot.figure()
    axes = mplot3d.Axes3D(figure)

    # Render the cube faces
    m = mesh.Mesh(data)
    axes.add_collection3d(mplot3d.art3d.Poly3DCollection(m.vectors))

    # Auto scale to the mesh size
    scale = numpy.concatenate([m.points for i in m]).flatten()
    axes.auto_scale_xyz(scale, scale, scale)

    # Show the plot to the screen
    pyplot.show()
# Parabolic gradient with radial symmetry and Z-axis variation
def index(z, x, y):
    n0 = 1.50  # maximum index
    nr2 = -2.44e-4  # index/mm^2
    nz = -2e-2  # index/mm
    r = np.sqrt(x ** 2 + y ** 2)  # radius in mm
    N = n0 + nr2 * r ** 2 + nz * z  # index value
    return N

def generateSTL(mtx):

    xsize = mtx.shape[0]
    ysize = mtx.shape[1]
    zsize = mtx.shape[2]
    
    nullSpace = np.nan
    
    surface = []
    
    dx = 10#(xf-xi)/xsize
    dy = 10#(xf-xi)/xsize
    dz = 10#(xf-xi)/xsize
    
    for x in range(0,xsize,dx):
        for y in range(0,ysize,dy):
            for z in range(0,zsize,dz):
                
                if mtx[x][y][z] != nullSpace and not math.isnan(mtx[x][y][z]):
                    
                    
                    # if a point is next to an NaN value then it is on the surface
                    
                    print(mtx[x][y][z])
                    # if at edge of space
                    if z+dz >= zsize or y+dy >= ysize or x+dx >= xsize:
                        print("at edge \n \n")
                        #surface = surface+[[x,y,z]]
                        #surface = surface+[[0,y,z]]
                        print(str(x),str(y),str(z))
                    else:
                        if math.isnan(mtx[x+dx][y][z]) or mtx[x+dx][y][z] == nullSpace:
                            surface = surface+[[x,y,z]]
                            print(str(x),str(y),str(z))
                            #print(surface)
                        elif math.isnan(mtx[x][y+dy][z]) or mtx[x][y+dy][z] == nullSpace:
                            surface = surface+[[x,y,z]]
                            print(str(x),str(y),str(z))
                            # print(surface)
                        elif math.isnan(mtx[x][y][z+dz]) or mtx[x][y][z+dz] == nullSpace:
                            surface = surface+[[x,y,z]]
                            print(str(x),str(y),str(z))
                            #print(surface)
    
    #with open3d
    #m = o3dtut.get_bunny_mesh()
    pcd = o3d.geometry.PointCloud()#m.sample_points_poisson_disk(750)
    pcd.points = o3d.utility.Vector3dVector(surface)
    o3d.visualization.draw_geometries([pcd])
    alpha = 0.03
    print(f"alpha={alpha:.3f}")
    tetra_mesh, pt_map = o3d.geometry.TetraMesh.create_from_point_cloud(pcd)
    #m=o3d.geometry.triangleMesh()
    #m.verticies = surface

    tetra_mesh, pt_map = o3d.geometry.TetraMesh.create_from_point_cloud(pcd)
    o3d.visualization.draw_geometries([tetra_mesh])
    #o3d.io.write_triangle_mesh("lense.stl", tetra_mesh)
    o3d.visualization.draw_geometries([tetra_mesh])	
    mesh = o3d.geometry.TriangleMesh.create_from_point_cloud_alpha_shape(pcd, alpha, tetra_mesh, pt_map)
	
    o3d.visualization.draw_geometries([mesh])

    #m = o3d.geometry.TriangleMesh.create_from_point_cloud_alpha_shape(pcd, alpha, tetra_mesh, pt_map)
    #m.compute_vertex_normals()
    #o3d.visualization.draw_geometries([m], mesh_show_back_face=True)
    
	
	#raw connect points
	#'''
    print(surface)
    triangles = len(surface)//3
    i=0
    data = numpy.zeros(triangles, dtype=mesh.Mesh.dtype)
    while i < triangles:
        #if surface[3*i:3*i+3].shape==(3,3):
        data['vectors'][i] = surface[3*i:3*i+3]
        print(surface[3*i:3*i+3])
        print(data['vectors'][i])
        i+=1
	#'''
	
	
	
	
	
	
	
	#solve for triangles with k nearest points
	def dist(p1,p2):
		return sqrt((p2[0]-p1[0])**2 + (p2[1]-p1[1])**2 + (p2[2]-p2[2])**2)
		
	def kNearestPoints(k,PointIndex,P):
		centerPoint = P[PointIndex]
		nearestPoints = []
		nearestPointdist = []
		for i in P:
			if len(nearestPoints) < k:
				nearestPoints+=i
				nearestPointdist+=dist(centerPoint,i)
			else:
				currentdist = dist(centerPoint,i)
				#should make shure the distances stay ordered
				for p in len(nearestPoints):
					#if this point is closer than any other closest point replace it with the new point
					if nearestPointdist[p] > currentdist:
						nearestPoints[p] = i
						nearestPointdist[p] = currentdist
			
		return nearestPoints
	
	
    #print(data['vectors'])
    # Create a new plot
    figure = pyplot.figure()
    axes = mplot3d.Axes3D(figure)

    # Render the mesh
    m = mesh.Mesh(data)
    axes.add_collection3d(mplot3d.art3d.Poly3DCollection(m.vectors))

    # Auto scale to the mesh size
    scale = numpy.concatenate([m.points]).flatten()
    axes.auto_scale_xyz(scale, scale, scale)

    # Show the plot to the screen
    pyplot.show()



def main():
	mtx = numpy.array([[0,0,0],[0,2,0],[3,0,2],
                    [0,2,0],[0,-1,3],[0,0,0],
                    [1,1,1],[0,2,0],[2,2,0]])
				

	dpi = 600  # resolution in dots per inch (DPI)
	dpmm = 600 / 25.4  # resolution in dots per millimeter (DPMM)

	part_width = 25.0  # mm
	part_thickness = 4  # mm

	part_width_pixels = np.round(part_width*dpmm).astype(int)  # number of pixels in the part width
	part_thickness_pixels = np.round(part_thickness*dpmm).astype(int)  # number of pixels in the thickness (z-axis)

					
					
	# creating a "meshgrid". This creates a coordinate space to which you can apply the function
	y_dim = np.linspace(-part_width / 2, part_width / 2, part_width_pixels)  # defines y-axis dimensions
	x_dim = np.linspace(-part_width / 2, part_width / 2, part_width_pixels)  # defines x-axis dimensions
	z_dim = np.linspace(0, part_thickness, part_thickness_pixels)  # defines z-axis dimensions
	Z, Y, X = np.meshgrid(z_dim, y_dim, x_dim, indexing='ij')
	
	
	part = index(Z, X, Y)  # Applying the function to the coordinate space. Returns an 3D array of index values

	# setting all values outside the target diameter to NANs (Not A Number)
	radius_map = np.sqrt(X**2 + Y**2)
	# a 3D array, where each elements value is mapped to it's radial distance in mm from the center
	
	part[radius_map > part_width/2] = np.nan
	# sets all elements in 'part' outside the target radius to a NAN (could be set to any value)

	#for space if x+1 or y+1 or z+1 == NAN 
		#surface+=[x,y,z]
	
	print(part.shape)
	generateSTL(part)
    
main()
#makecylinder(100,50)
    
