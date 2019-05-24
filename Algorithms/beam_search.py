import sys
import copy
sys.path.append('../Classes')
from Protein import Protein
sys.path.append('../')
from helpers import save_best_protein
from operator import itemgetter

def beam_search(protein_filename):
    """
    Algorithm that finds solutions by going breadth first through
    the statespace with a certain beam
    """
    protein = Protein(protein_filename)
    amino_acids = protein.get_amino_acids()
    best_proteins, queue, child_stabilities, beamsearch = ([] for i in range(4))
    beam = 50
    # place first two amino acids, bc their placing doesn't matter
    protein.place_first_two()

    # put start protein in the queue
    queue.append(protein)

    while queue != []:
        # pick the child in front off the queue
        protein = queue.pop(0)

        # if next amino exists,
        next_parent_amino = protein.get_next_amino()

        # make a list with all proteins and their stabilities
        if next_parent_amino:
                        # get all the possible places to put the next amino
            all_children = protein.get_kids()

            # append the new child to the pre-beam list
            for child in all_children:
                child.update_stability()
                beamsearch.append(child)
            beamsearch.sort()

            # if queue is empty al kids are made
            if queue == []:
                # if the beam is bigger than the number of kids, add all kids
                if len(beamsearch) < beam:
                    for i in range(len(beamsearch)):
                        queue.append(beamsearch[i])
                # else only pick the best kids
                else:
                    for i in range(beam):
                        queue.append(beamsearch[i])

                beamsearch = []

        # when protein is completed
        else:
            # save best protein
            best_proteins = save_best_protein(best_proteins, protein)
