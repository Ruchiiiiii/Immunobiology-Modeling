import random
import os
import numpy as np
import sys
import time
from Ant_Lymph import Antigen, Lymphocyte
from Bcell_Selection import Selection
from numpy import array
from Arg_Parser import *
from datetime import date, datetime
import operator
import time
import matplotlib.pyplot as plt

args = ant_lymph_parser().parse_args(sys.argv[1:])


class Main:

    def __init__(self, ):
        self.iteration_counts = dict()

    def immune_response(self, population_dict, antigen_pop, a_div):
        """
        Simulates immune response games between the antigen and lymphocyte populations.

        :arg population_dict --> Post-selection dictionary from B-cell selection algorithm
        :arg antigen_pop --> Dictionary for the single antigen population
        :arg response_time --> Number of iterations allowed for the immune response games
        :arg a_div --> Antigen division rate

        :return Population dictionary

        """
        for k in population_dict.copy():
                if population_dict[k][2] == 0.0:
                    population_dict.pop(k)
        
        
        print("Immune response games between the antigen and lymphocyte populations")
        print("Post-selection dictionary from B-cell selection algorithm:", population_dict)
        # Run an agent-based game between each lymphocyte population and the antigen population
        
        while(antigen_pop.n>0):
            if antigen_pop.n>10000:
                print("ANTIGENS WON")
                break
            for pop in population_dict.values():
                if pop[1] > 0 and antigen_pop.n>0:
                    # Runs a game where a random number between 0 and 1 is picked.
                    #for n in range(0, pop[1]):
                        draw = random.random()
                        
                        # Removes 1 individual from the lymphocyte population (antigen wins)
                        if draw > pop[2]:
                            pop[1] -= 1 # If the antibody loses the fight against the antigen, it dies
                            antigen_pop.n += a_div #Antigen divides

                        # Removes 1 individual from the antigen population (lymphocyte wins)
                        elif draw <= pop[2]:
                            pop[1] += 1 # If the antibody wins the fight against the antigen, the antibody dies and the B cell produces 2 more antibodies
                            antigen_pop.n -= 1 #Antigen dies
                            if antigen_pop.n<=0:
                                print("ANTIGENS ERADICATED")
                                break
                    
                        else:
                            print("Error: Draw exceeds 0-1 range.")
        print("Antigen population", antigen_pop.n)
        return population_dict


if __name__ == '__main__':

    pop_size = int(args.pop_size)
    pop_num = int(args.pop_num)
    epitope = args.epitope
    ant_div = int(args.division_rate)
    exchange_iter = int(args.exchange_iter)
    is_reinf = int(args.is_reinf)
    antigen = Antigen(epitope=epitope, pop_num=1, n=3, division_rate=ant_div)
    

    start_time1 = time.time()
    lymph = Lymphocyte(paratope='', pop_num=pop_num, n=pop_size)

    for k in range(0, lymph.pop_num):
        paratope = lymph.gen_para(len(antigen.epitope))
        lymph.pops[k] = [paratope]

    selection = Selection()
    print("_________________________________________________________________")

    # Run B-cell Somatic Hypermutation
    populations = selection.somatic_hyp(exchange_iter=exchange_iter, antigen=antigen,
                                             lymphocyte=lymph, is_reinf=False)
    print("_________________________________________________________________")

    # Run the immune response for all populations
    response = Main()
    final_pops = response.immune_response(populations, antigen, a_div=ant_div)
    survived = list()
    for v in final_pops.values():
        if v[1] >= 1:
            survived.append(v)

    print("Surviving Populations: ", survived)
    
    print("--- %s seconds before reinfection ---" % (time.time() - start_time1))
    


    #If reinfection occures
    if is_reinf:
        antigen = Antigen(epitope=epitope, pop_num=1, n=1000, division_rate=ant_div)
        survived = sorted(survived, key = operator.itemgetter(2, 1), reverse=True)
        #survived.sort(key = lambda x: x[2], reverse=True)    
        print("Sorted Surviving Populations: ", survived)
        
        #Make before reinfection graph
        aa_list = [x[0] for x in survived]
        pop_size_list = [x[1] for x in survived]
        fitness_list = [x[2] for x in survived]
        fig, ax = plt.subplots(figsize = (10, 5))
        plt.title('Population size and fitness of surviving population after Natural Selection - Before Reinfection')
        ax2 = ax.twinx()
        ax.plot(aa_list, pop_size_list, '.', color = 'g')
        ax2.plot(aa_list, fitness_list, '.', color = 'b')

        ax.set_xlabel('Surviving populations', color = 'r')
        ax.set_ylabel('Population sizes', color = 'g')
        ax2.set_ylabel('Fitness values', color = 'b')
        plt.tight_layout()
        plt.show()

        start_time2 = time.time()
        #prev_para_reinf = survived[:5:]
        lymph = Lymphocyte(paratope='', pop_num=pop_num, n=pop_size)

        for k in range(0, lymph.pop_num):
            lymph.pops[k] = [survived[k%len(survived)][0]]
        print("After reinfection")
        print("_________________________________________________________________")

        #selection = Selection()
        print("_________________________________________________________________")

        # Run B-cell Somatic Hypermutation
      
        #populations = selection.somatic_hyp(exchange_iter=exchange_iter, antigen=antigen, lymphocyte=lymph, is_reinf=True)
        populations_reinf = dict()
        for i in range(len(survived)):
            populations_reinf[i] = survived[i]
        print("Starting populations after Reinfection: ", populations_reinf)
        print("Antigen Epitope: ", antigen.epitope)
        print("_________________________________________________________________")

        # Run the immune response for all populations
        response = Main()
        final_pops = response.immune_response(populations_reinf, antigen, a_div=ant_div)
        survived_after_reinf = list()
        for v in final_pops.values():
            if v[1] >= 1:
                survived_after_reinf.append(v)

        print("Surviving Populations after Reinfection: ", survived_after_reinf)
        survived_after_reinf = sorted(survived_after_reinf, key = operator.itemgetter(2, 1), reverse=True)
        #survived.sort(key = lambda x: x[2], reverse=True)    
        print("--- %s seconds after reinfection ---" % (time.time() - start_time2))
        print("Sorted Surviving Populations after Reinfection: ", survived_after_reinf)

        #Make after reinfection graph
        aa_list = [x[0] for x in survived_after_reinf]
        pop_size_list = [x[1] for x in survived_after_reinf]
        fitness_list = [x[2] for x in survived_after_reinf]
        fig, ax = plt.subplots(figsize = (10, 5))
        plt.title('Population size and fitness of surviving population after Natural Selection - After Reinfection')
        ax2 = ax.twinx()
        ax.plot(aa_list, pop_size_list, '.', color = 'g')
        ax2.plot(aa_list, fitness_list, '.', color = 'b')

        ax.set_xlabel('Surviving populations', color = 'r')
        ax.set_ylabel('Population sizes', color = 'g')
        ax2.set_ylabel('Fitness values', color = 'b')
        plt.tight_layout()
        plt.show()

    results = list()
    for value in final_pops.values():
        results.append(value)

    today = date.today()
    now = datetime.now()
    current_time = now.strftime("__%H%M")
    date = today.strftime("_%y%m%d")
    cain_file = os.path.join(root_dir, "results" + date + current_time + ".npz")
    final = np.array(results)
    np.savez(cain_file, data=final)
    print("Immune Response Completed")
    print("Saving file", cain_file)
    print("_________________________________________________________________")
