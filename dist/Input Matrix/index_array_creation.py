import numpy as np
import matplotlib.pyplot as plt

dpi = 600  # resolution in dots per inch (DPI)
dpmm = 600 / 25.4  # resolution in dots per millimeter (DPMM)

part_width = 25.0  # mm
part_thickness = 4  # mm

part_width_pixels = np.round(part_width*dpmm).astype(int)  # number of pixels in the part width
part_thickness_pixels = np.round(part_thickness*dpmm).astype(int)  # number of pixels in the thickness (z-axis)

# ------Here are multiple examples of functions. Uncomment whichever function you want to try. -------


# Parabolic gradient with radial symmetry
# def index(z, x, y):
#     n0 = 1.50  # maximum index
#     nr2 = -2.44e-4  # index/mm^2
#     r = np.sqrt(x ** 2 + y ** 2)  # radius in mm
#     N = n0 + nr2 * r ** 2  # index value
#     return N

# Parabolic gradient with radial symmetry and Z-axis variation
def index(z, x, y):
    n0 = 1.50  # maximum index
    nr2 = -2.44e-4  # index/mm^2
    nz = -2e-2  # index/mm
    r = np.sqrt(x ** 2 + y ** 2)  # radius in mm
    N = n0 + nr2 * r ** 2 + nz * z  # index value
    return N

# Cubic gradient (non-radial symmetry)
# def index(z, y, x):
#     L=part_width/2
#     nH = 1.5
#     nL = 1
#     n = (nH + nL)/2 + ((nH - nL)/2) * (x**3 + y**3)/(2*(L**3))
#     return n

# ---------------------------------------------------------------


# creating a "meshgrid". This creates a coordinate space to which you can apply the function
y_dim = np.linspace(-part_width / 2, part_width / 2, part_width_pixels)  # defines y-axis dimensions
x_dim = np.linspace(-part_width / 2, part_width / 2, part_width_pixels)  # defines x-axis dimensions
z_dim = np.linspace(0, part_thickness, part_thickness_pixels)  # defines z-axis dimensions
Z, Y, X = np.meshgrid(z_dim, y_dim, x_dim, indexing='ij')

part = index(Z, X, Y)  # Applying the function to the coordinate space. Returns an 3D array of index values

# setting all values outside the target diameter to NANs (Not A Number)
radius_map = np.sqrt(X**2 + Y**2)  # a 3D array, where each elements value is mapped to it's radial distance in mm from the center
part[radius_map > part_width/2] = np.nan  # sets all elements in 'part' outside the target radius to a NAN (could be set to any value)

# ----- saving the array for later use -------

# Saving the array
np.save('index_profile.npy', part)
# file can be loaded again using np.load()

# ---------- Plotting cross sections for visualization -----------

Z_slice = 1  # slice along Z to plot
plt.imshow(part[Z_slice, :, :], origin='lower')  # plotting a z-axis cross section
plt.colorbar()

plt.figure()
plt.imshow(part[:, int(part.shape[1]/2), :], origin='lower')  # plotting a ZX cross section down the center
plt.colorbar()

plt.show()




