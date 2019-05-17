from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
import numpy as np
import pathlib
from helpers import load_from_csv, get_file
import math
import sys
import csv
import ast


def visualize_csv(algorithm, protein, size=3):
    """
    A function that visualizes the folded protein using matplotlib
    Usage: python visualize_csv.py algorithm protein_name [size]
    """
    # construct the path to the csv file
    filepath = pathlib.Path("Results/{}/{}_{}.csv".format(algorithm, algorithm, protein))

    # check if file exists
    if not filepath.exists():
        print("file cannot be found")
        exit(1)

    # read in the file as a list of protein objects
    all_proteins = load_from_csv(filepath, protein)
    num_proteins = len(all_proteins)

    # specify how many protein subplots to visualize in one figure
    size = int(size)
    total_in_plot = size * size

    for protein_i, protein in enumerate(all_proteins):
        # get the attributes of the protein
        all_coordinates = protein.get_all_coordinates()
        amino_places = protein.get_amino_places()
        bonds = protein.get_bonds()

        # putting the coordinates in an x and an y list
        x_list, y_list, z_list, \
        scat_hx_list, scat_hy_list, scat_hz_list, \
        scat_px_list, scat_py_list, scat_pz_list, \
        scat_cx_list, scat_cy_list scat_cz_list = ([] for list in range(12))

        # print(all_coordinates)

        for coordinates in list(all_coordinates):
            # unpack the coordinate values
            x, y = coordinates
            x_list.append(x)
            y_list.append(y)
            z_lisy.append(z)

            # group the coordinates of the same amino kinds
            amino_kind = amino_places["{}".format(coordinates)]
            if amino_kind == 'P':
                scat_px_list.append(x)
                scat_py_list.append(y)
                scat_pz_list.append(z)
            elif amino_kind == 'H':
                scat_hx_list.append(x)
                scat_hy_list.append(y)
                scat_hz_list.append(z)
            else:
                scat_cx_list.append(x)
                scat_cy_list.append(y)
                scat_cz_list.append(z)

        # put the protein in a subplot
        position = (protein_i + 1) % total_in_plot
        if position == 0:
            position = total_in_plot
        plt.subplot(size, size, position)

        # Plot cavalent line
        plt.plot3D(x_list, y_list, z_list, color='black', linestyle='solid', zorder=1)

        # use different colours to visualize the amino kind groups
        plt.scatter3D(scat_px_list, scat_py_list, scat_pz_list, color='red', zorder=2)
        plt.scatter3D(scat_hx_list, scat_hy_list, scat_hz_list, color='blue', zorder=2)
        plt.scatter3D(scat_cx_list, scat_cy_list, scat_cz_list, color='gold', zorder=2)

        # unpack the bonds neighboring_locations
        for bond in bonds:
            bonds_x, bonds_y, bonds_z = ([] for list in range(3))
            for coordinate in bond:
                x, y = coordinate
                bonds_x.append(x)
                bonds_y.append(y)
                bonds_z.append(z)

            # plot bond
            plt.plot(bonds_x, bonds_y, bonds_z, color='green', linestyle='--', zorder=1)

        #  set plot axis
        plt.axes([min(x_list) - 1, max(x_list) + 1, min(y_list) - 1, max(y_list) + 1, min(z_list) - 1, max(z_list) + 1], projection='3d')

        # show figure when total subplots are placed or last protein is reached
        if position == total_in_plot or protein_i == num_proteins - 1:
            plt.show()
            # clear figure
            plt.clf()


if __name__ == "__main__":

    if len(sys.argv) == 3:
        visualize_csv(sys.argv[1], sys.argv[2])
    # argv[3] is the size of the subplots, which is in this case optional
    elif len(sys.argv) == 4:
        visualize_csv(sys.argv[1], sys.argv[2], sys.argv[3])
    else:
        print("Usage: python 3D_visualize_csv.py algorithm protein_name [size]")
        exit(1)