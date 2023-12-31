import pandas as pd
import numpy as np
import random
import os
from tqdm import tqdm
import Arg_Parser

############ Set PAM matrix location here ############
matrix = np.loadtxt(os.path.join(Arg_Parser.root_dir, "Resources/PAM_250.txt"))
matrix = np.array(matrix)

col_names = ("A", "R", "N", "D", "C", "Q", "E", "G", "H", "I", "L", "K", "M", "F", "P", "S", "T", "W", "Y", "V")
row_names = col_names
pam = pd.DataFrame(matrix, columns=col_names, index=row_names)  #Creates a square matrix of substitution likelihoods.
pam = pam / np.max(pam)


class Selection:

    def __init__(self):
        self.result_pop = dict()
        self.selection_dict = dict()
        self.likelihood = dict()

    def somatic_hyp(self, exchange_iter, antigen, lymphocyte, is_reinf, max_affinity=True):
        """
        Performs somatic hypermutation on each B-cell population generated in Ant_Lymph.py. Each random paratope generated
        represents a population with a property n as the number of individuals in the population. This will become
        relevant in the immune response. Substitution likelihoods are calculated for each character of the paratope
        taken from the PAM 250 matrix. This will run for exchange_iter number of iterations.

        :arg lymphocyte
        :arg antigen
        :arg max_affinity --> Breaks the loop if paratope fitness is equal to 1.
        :arg exchange_iter --> The amount of iterations before fitness is calculated.

        :return: Population(s) with max affinity to the antigen epitope.
        """
        ant = antigen.epitope # Stores the input epitope

        aa_list = ['A', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'M',
                   'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'Y']

        # Create a dictionary with each population as keys and the paratopes as values
        self.selection_dict = lymphocyte.pops

        for item in aa_list:
            self.likelihood[item] = 0

        for aa in self.likelihood.keys():
            other_likelihood = dict()
            for row in row_names:

                # Calls the df column for the amino acid
                col = pam[aa]

                # Calls the value for the column and row
                value = col[row]

                other_likelihood[row] = value
            self.likelihood[aa] = other_likelihood

        # Identifies the index - specific match integer
        for key, value in self.selection_dict.items():
            para = value
            match_number = len(list(filter(lambda xy: xy[0] == xy[1], zip(ant, para))))

            # Calculate and append number of B cells in the population and fitness value
            fitness = match_number / len(ant)
            value.append(lymphocyte.n)
            value.append(fitness)

            # Each population will undergo somatic hypermutation as opposed to each individual because the likelihood of
            # substitution would be the same for each individual in the population.

        ############# Selection Process #############
        print("Starting populations: ", self.selection_dict)
        print("Antigen Epitope: ", ant)
        c=0 # counts how many times PAM substitution occurs
        if is_reinf == False:
            for i in tqdm(range(0, exchange_iter)):

                # Iterate through each population
                for item in self.selection_dict.values():
                    product = ''

                    # Iterate through each amino acid in the paratope sequence
                    for a in item[0]:
                        # Index amino acids in the paratope to their PAM likelihood values
                        v = list(self.likelihood[a].values())
                        k = list(self.likelihood[a].keys())

                        # Remove and prevent self substitutions
                        v.remove(v[k.index(a)])
                        k.remove(a)
                        #Select a random amino acid to replace the vth amino acid
                        randv = random.choice(v)
                        if randv > 0:
                            q = random.randrange(0, 1)
                            if randv >= q:
                                # Substitutes the original amino acid with the new
                                product += k[v.index(randv)]
                                c+=1
                            else:
                                product += a
                        else:
                            product += a

                    item[0] = product
                    para = item[0]

                    # Calculate the fitness of each paratope after selection
                    match_number = len(list(filter(lambda xy: xy[0] == xy[1], zip(ant, para))))
                    fitness = match_number / len(ant)
                    item[2] = fitness

                    if max_affinity:
                        if fitness == 1:
                            break
        #print("c",c)
        return self.selection_dict
