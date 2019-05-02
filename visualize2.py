import matplotlib.pyplot as plt
import numpy as np
import pathlib
import sys
import csv
import pandas as pd

def visualize_csv(algorithm, protein):
    """
    A function that visualizes the folded protein using matplotlib
    """
    # check if file exists
    file = "_".join([algorithm, protein])
    filepath = pathlib.Path("Results/{}/{}.csv".format(algorithm, file))
    if not filepath.exists():
        print("file cannot be found")
        exit(1)


    df = pd.read_csv(filepath, decimal=",")

    print(df.head())

    # for coordinates in df['all_coordinates']:
        # unpack the coordinate values
        # print()
    #     x, y = coordinates
    #     x_list.append(x)
    #     y_list.append(y)
    #
    #     # group the coordinates of the same amino kinds
    #     amino = amino_places["{}".format(coordinates)]
    #     amino_kind = amino.get_kind()
    #     if amino_kind == 'P':
    #         scat_px_list.append(x)
    #         scat_py_list.append(y)
    #     elif amino_kind == 'H':
    #         scat_hx_list.append(x)
    #         scat_hy_list.append(y)
    #     else:
    #         scat_cx_list.append(x)
    #         scat_cy_list.append(y)
    #
    # # Plot cavalent line
    # plt.plot(x_list, y_list, color='black', linestyle='solid', zorder=1)
    #
    # # use different colours to visualize the amino kind groups
    # plt.scatter(scat_px_list, scat_py_list, color='red', zorder=2)
    # plt.scatter(scat_hx_list, scat_hy_list, color='blue', zorder=2)
    # plt.scatter(scat_cx_list, scat_cy_list, color='gold', zorder=2)
    #
    # # unpack the bonds neighboring_locations
    # for bond in bonds:
    #     bonds_x = []
    #     bonds_y = []
    #     for bonds_amino in bond:
    #         x, y = bonds_amino.get_location()
    #         bonds_x.append(x)
    #         bonds_y.append(y)
    #
    #     # plot bond
    #     plt.plot(bonds_x, bonds_y, color='green', linestyle='--', zorder=1)
    #
    # #  set plot axis and show plot
    # plt.axis([min(x_list) - 1, max(x_list) + 1, min(y_list) - 1, max(y_list) + 1])
    # plt.show()

if __name__=="__main__":
    visualize_csv(sys.argv[1], sys.argv[2])