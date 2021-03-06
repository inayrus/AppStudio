import sys
sys.path.append('../')
import pathlib
import random
from Amino import Amino
import copy

class Protein(object):
    """Representation of a protein"""

    def __init__(self, file):
        """ Initializes a protein"""
        self.stability = 0
        self.amino_acids = self.load_protein(file)
        self.bonds = []
        self.all_coordinates = []
        self.amino_places = {}
        self.is_straight = True

    def load_protein(self, file):
        """
        Reads the protein in from a text file
        Returns a list of Amino instances
        """
        # ensure the file can be found despite the directory that the user is in
        filepath = pathlib.Path("ProteinData/{}.txt".format(file))
        if not filepath.exists():
            p = pathlib.Path("../ProteinData/{}.txt".format(file))
            filepath = p.resolve()

        # read in the file
        with filepath.open('r') as f:
            amino_acids = []

            for line in f:
                # get rid of whitespace
                seq = line.strip()

                for index, letter in enumerate(seq):
                    # turn each letter into an Amino object
                    new_amino = Amino(index, letter)

                    # add the new and prev amino to each other's connections
                    if index > 0:
                        prev_amino = amino_acids[index - 1]
                        new_amino.set_connections(prev_amino)
                        prev_amino.set_connections(new_amino)

                    # add the new amino to the list
                    amino_acids.append(new_amino)

        return amino_acids

    def get_kids(self):
        """
        Function that makes the children
        Returns a list with children
        """
        kids = []
        all_places = self.get_place_options(self.get_rearmost_amino())

        # only continue if protein hasn't folded into itself
        if all_places != []:
            # for every possible place, copy the current protein and create a child
            for place in all_places:
                protein_child = copy.deepcopy(self)

                # place new amino
                next_child_amino = protein_child.get_next_amino()
                protein_child.place_amino(place, next_child_amino.get_id())
                kids.append(protein_child)

        return kids


    def update_bonds(self):
        """
        Function to store the bonds H's or C's made in the protein
        """
        # loop through the aminos in the protein
        for amino in self.amino_acids:
            num_placed = len(self.all_coordinates)

        for index in range(num_placed - 1):
            amino = self.amino_acids[index]

            # if H or C, get surrounding locations the amino is not connected to
            if amino.get_kind() != 'P':
                surroundings = self.get_neighbors(amino)

                # remove location of connected amino's
                for conn_amino in amino.get_conn():
                    conn_location = conn_amino.get_location()
                    if conn_location in surroundings:
                        surroundings.remove(conn_location)

                for location in surroundings:
                    # check if location is in dict
                    str_location = "{}".format(location)

                    if str_location in self.amino_places:
                        amino_id = self.amino_places[str_location]
                        nearby_amino = self.amino_acids[amino_id]

                        # there's only a bond if new amino is H or C
                        if nearby_amino.get_kind() != 'P':

                           # check if current bond is already stored
                            if [amino, nearby_amino] not in self.bonds and \
                               [nearby_amino, amino] not in self.bonds:

                                # if not, add bond to attribute
                                self.bonds += [[amino, nearby_amino]]

        return self.bonds

    def set_bonds(self, bonds):
        """
        Sets the bonds attribute to a certain value.
        """
        self.bonds = bonds

    def update_stability(self):
        """
        A function that sets the stability of the protein
        """
        self.update_bonds()

        # reset stability
        self.stability = 0

        # check all bonds and get kinds of bonded amino's
        for bond in self.bonds:
            amino, other_amino = bond
            amino = amino.get_kind()
            other_amino = other_amino.get_kind()

            # set stability to -1 of -5 depending on bond
            if amino == "H" or other_amino == "H":
                self.stability -= 1
            elif amino == "C" and other_amino == "C":
                self.stability -= 5

        return self.stability

    def set_stability(self, stability):
        """
        Sets the stability attribute to a certain value.
        """
        self.stability = stability

    def add_coordinates(self, coordinate):
        """
        A function that adds a coordinate to the list of all used coordinates
        in the protein
        """
        self.all_coordinates += [coordinate]

    def remove_coordinates(self, coordinate):
        """
        A function that removes a coordinate from the list of all used coordinates
        in the protein
        """
        self.all_coordinates.remove(coordinate)

    def set_all_coordinates(self, coordinates):
        """
        Sets the coordinates attribute to a certain value
        """
        self.all_coordinates = coordinates

    def add_amino_place(self, coordinate, amino_id):
        """
        A function that links an Amino to its coordinates
        {'coordinates': Amino id}
        """
        self.amino_places["{}".format(coordinate)] = amino_id

    def remove_amino_place(self, coordinate):
        """
        A function that deletes a coordinate key from the dict
        Returns the removed amino
        """
        return self.amino_places.pop("{}".format(coordinate))

    def set_amino_places(self, amino_places):
        """
        Sets the amino places attribute to a certain value.
        """
        self.amino_places = amino_places

    def get_neighbors(self, amino):
        """
        A function that returns a list of all coordinates around a certain
        grid point
        """
        # returns surrounding coordinates in 2d
        if sys.argv[3] == "2d":
            coordinates = amino.get_location()
            x, y = coordinates
            return [[x, y + 1], [x, y - 1], [x + 1, y], [x - 1, y]]

        # returns surrounding coordinates in 3d
        if sys.argv[3] == "3d":
            coordinates = amino.get_location()
            x, y, z = coordinates
            return [[x, y + 1, z], [x, y - 1, z], [x + 1, y, z], [x - 1, y, z], [x, y, z + 1], [x, y, z - 1]]

    def get_place_options(self, amino):
        """
        Returns a list with the optional coordinates to place next amino in
        """
        # get all spaces around amino
        all_places = self.get_neighbors(amino)

        # remove symmetry for 2d proteins
        if sys.argv[3] == '2d':
            if self.is_straight == True:
                x_check = 0
                for x, y in self.all_coordinates:
                    x_check += x
                if x_check == 0:
                    # remove the left (x - 1) space option
                    all_places = [[x, y + 1], [x + 1, y]]
                else:
                    self.is_straight = False

        # remove symmetry for 3d proteins
        if sys.argv[3] == "3d":
            if self.is_straight == True:
                x_check = 0
                z_check = 0
                for x, y, z in self.all_coordinates:
                    x_check += x
                    z_check += z
                if x_check == 0:
                    # remove the left (x - 1) space option
                    all_places = [[x, y + 1, z], [x + 1, y, z]]
                elif z_check == 0:
                    # remove the backwards (z - 1) space option
                    all_places = [[x + 1, y, z], [x, y + 1, z], [x, y - 1, z], [x, y, z + 1]]
                else:
                    self.is_straight = False

        # remove places that already have amino acids on them
        for coordinate in self.get_all_coordinates():
            if coordinate in all_places:
                all_places.remove(coordinate)

        return all_places

    def get_next_amino(self):
        """
        Returns the first amino that's not yet placed
        """
        # get the number of placed amino's
        num_placed = len(self.all_coordinates)

        if num_placed < len(self.amino_acids):
            next_amino = self.amino_acids[num_placed]
            return next_amino

        # there is no next amino
        else:
            return None

    def __lt__(self, other):
        return self.stability < other.get_stability()

    def get_rearmost_amino(self):
        """
        Returns the last placed amino.
        """
        num_placed = len(self.all_coordinates)
        amino = self.amino_acids[num_placed - 1]
        prev_amino = self.amino_acids[num_placed - 2]
        return amino

    def place_first_two(self):
        """
        Places first two aminoacids to get rid of rotational symmetry
        """
        if sys.argv[3] == "2d":
            self.place_amino([0, 0], 0)
            self.place_amino([0, 1], 1)

        if sys.argv[3] == "3d":
            self.place_amino([0, 0, 0], 0)
            self.place_amino([0, 1, 0], 1)

    def place_amino(self, coordinates, amino_id):
        """
        Places an amino on given coordinates.
        """
        self.add_coordinates(coordinates)
        self.add_amino_place(coordinates, amino_id)
        self.amino_acids[amino_id].set_location(coordinates)

    def get_stability(self):
        """
        Returns the protein's stability (int)
        """
        return self.stability

    def get_amino_acids(self):
        """
        Returns a list with all Amino objects in this Protein
        """
        return self.amino_acids

    def get_bonds(self):
        """
        Returns a list with all bonds between H and C amino acids
        [Amino object 1, Amino object 2]
        """
        return self.bonds

    def get_all_coordinates(self):
        """
        Returns a list with all coordinates in this protein configuarion
        """
        return self.all_coordinates

    def get_amino_places(self):
        """
        Returns a dict for all locations of the amino acids
        {'coordinate': Amino object}
        """
        return self.amino_places

    def __repr__(self):
        s="======= Protein\n"
        s+="stability:"+str(self.stability)+"\n"
        s+="amino_acids:"+str(self.amino_acids)+"\n"
        s+="bonds:"+str(self.bonds)+"\n"
        s+="all_coordinates:"+str(self.all_coordinates)+"\n"
        s+="amoni_places"+str(self.amino_places)+"\n"
        return s

    def __str__(self):
        return repr(self)
