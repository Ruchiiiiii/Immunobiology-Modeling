# Immunobiology-Modeling
Using Python to design a computational model to demonstrate positive selection of immune cells with higher affinity to a pathogen

**Introduction**

B cells, as well as the antibodies produced by them, comprise a major part of the human adaptive
immune system. During the early days of their development in the bone marrow, B cells undergo genetic
recombination, in which certain segments of chromosome 14 get cut out and pasted together
randomly. These genes which get recombined are those that code for the antibody / B cell
receptor. This recombination process helps our body recognise and fight against many types of
antigens. BCRs recognise and bind to specific epitopes of antigens leading to the activation of
the B cell via a series of steps. These include a signaling pathway, T-cell co-stimulation and
co-regulation with the help of complement proteins (these will not be modeled in this project).

Activated B cells proliferate rapidly in a process called Clonal Selection. This large population of
cells has 3 possible fates: i) Plasma cells which produce antibodies which help fight the infection
in its early stages, ii) Memory cells which come into play in the case of reinfection and iii)
Germinal center cells which are present in the secondary lymphoid organs and help produce a
fine-tuned response to infection. This is facilitated by a process called Somatic Hypermutation.
GC cells proliferate rapidly and with an increased rate of mutation in those same genes which
code for the antigen-recognising site of the antibody. As a result of these mutations, binding
affinity may increase, decrease or remain the same. Since cells with higher affinity BCRs can
bind to epitopes more efficiently, they have a higher chance of surviving and natural selection
prefers them. These cells produce highly specific antibodies on a large scale to fight off the
infection.

Once the pathogen is cleared, the surviving population of cells and their high-affinity antibodies
remain in circulation and act as the initial line of defense during reinfection.
This project will model the process of somatic hypermutation occurring in the Germinal cells and
use game theory to show that those cells with high-affinity BCRs get selected naturally and have
a higher surviving population than those with low-affinity. It will also show that the response to
reinfections will be faster. It will not model the initial plasma cell response or the memory cells
involved during the process of reinfection

**Methods**

Assumptions:
1. Epitopes on antigens consists of a random string of Amino acids, and the part of the
BCR on the B cell which recognises epitopes are called Paratopes.
2. Paratopes will be randomly generated to mimic the genetic recombination process that
occurs in the early stages of B cell development to generate a range of B cells with
different BCRs.
3. Any paratope of the same length and at least one amino acid which is similar to the
epitope will recognise the epitope and undergo SH. In reality, binding between epitopes
and paratopes involve the formation of various bonds which cannot be modeled in a
simple way.
4. The strength of the bond between the epitope and paratope is proportional to the number
of amino acids which are the same. This bond strength is referred to as the fitness of the
paratope. Fitness = Number of similar aa/Total number of aa in the epitope
5. SH involves Point Accepted Mutations in genes, where single amino acids get changed
using a PAM matrix.ty

Steps:
1. Arg_Parser Code:
The code takes the following inputs:
- - e: to set the epitope amino acid sequence
- - n: to set the initial naive B cell population
- - d: to set the division rate of the antigens
- - p: to set the number of antibodies produced by each B cell
- - ex: to set the number of times B cells undergo Somatic Hypermutation
- - ri: to tell whether reinfection occurs or not
    
2. Ant_Lymph Code:
- This code organizes the properties of the antigen epitope and the B cells
- It generates multiple random paratopes of the same length as the antigen epitope.
  
3. Bcell_Selection Code:
This code models the SH process. In this process, cells undergo rapid division and mutation at
specific genes. These mutations are semi-random, and may produce cells which can either
recognise the epitope better, worse or the same amount. PAM stands for Point Accepted
Mutations, which refer to changes in a single amino acid of a protein, which is accepted by
the process of natural selection. The PAM matrix is a 20*20 matrix where each row and column
depict one amino acid. Each entry in the matrix shows the likelihood that one amino acid will
change into the other.
Under the function ‘somatic_hyp’:
1. First the epitope is stored and a dictionary of the starting population of B cells is
created, with the population number as the key, and the paratope sequence as the
value.
Example output: {0: ['MYAPS'], 1: ['IRDEA'], 2: ['VMMRH'].. 249: ['TYLTP']}
2. Then, the PAM matrix is stored as a dictionary.
3. The number of amino acids which are matching between the epitope and paratope
is calculated and stored as the fitness of each paratope.
4. The number of individuals in each paratope population, as well as the fitness of
each individual paratope is appended to the existing paratope dictionary.
Example output: Starting populations: {0: ['MYAPS', 100, 0.0], 1: ['IRDEA', 100,
0.0], 2: ['VMMRH', 100, 0.0].. 249: ['TYLTP', 100, 0.0]}
5. Now the process of somatic hypermutation can begin. We assume that each
individual in a population with a specific paratope undergoes the same type of
mutations.
6. For every type of paratope in the starting population of paratopes, we go through
every amino acid, and randomly replace it with another amino acid. The
likelihood of that amino acid being replaced is determined by their probabilities
given by the PAM matrix.
7. This is done a certain (user-set) number of times, and the fitness of each type of
paratope is calculated again at the end.
8. The dictionary with the new fitness values updated is given as the output:
Example Output: Post-mutation dictionary from B-cell Hypermutation algorithm:
{0: ['YLGGG', 100, 0.2], 1: ['LGGGG', 100, 0.2]..249: ['GIVAG', 100, 0.2]}
This dictionary contains the mutated paratopes on the B cells, the number of
antibodies produced having that paratope and their fitness.

4. Main Code:
This is the main code, which runs the game between antibodies and antigens.
Under the function ‘immune_response’:
1. The antibodies which have 0 affinity for the epitope after SH are all removed
from the dictionary.
2. From the remaining antibody populations, an agent-based game is run between
the antibody and the antigen.
3. In this, a number is randomly selected between 0 and 1, and if
    a. That number is more than the fitness of the antibody, the antigen survives
        and divides while the antibody population size decreases by one
  b. That number is less than the fitness of the antibody, the antigen population
   size decreases by one, and the antibody population size increases by 2
Although antibodies almost always die during their interactions with antigens and
are also proteins which cannot replicate themselves, here we assume that, if an
antibody wins against an antigen, it also dies but its parent B cell produces 2 more
of that type of antibody, thus the net increase is 1.
4. This game will run until all the antigens are eliminated, or until their numbers
become more than 100000, in which case the antigens have won.
5. OUTPUTS:
    a. The surviving antibodies, their population size and fitness
    b. The response time, i.e., the time taken for all the antigens to be eradicated.
6. In case reinfection by the same antigen, that is, epitope, occurs, the agent based
game is first run between the surviving antibodies and the antigen population.
7. Only if all of the antibodies die in this process, then SH of new paratope
populations occurs.
8. OUTPUTS:
    a. The surviving antibodies, their population size and fitness
    b. The response time, i.e., the time taken for all the antigens to be eradicated.
   
Running the Code:
1. Extract the folder
2. Open Arg_Parser.py code and change the first line (root_dir = ‘’). Put the path of where
the folder is saved between the quotes
3. Open cmd terminal through that folder in File Explorer
4. Run the following command:
python Main.py -e ADPFG -n 10 -d 1 -p 800 -ex 100 -ri 1
5. In case any packages need to be installed do: pip install ‘packagename’
