import argparse

root_dir = '/Users/Sanchitha/OneDrive/Documents/My Docs/Ashoka/Monsoon 2022/Comp Bio/Project/CAIN'


def ant_lymph_parser():
    parser = argparse.ArgumentParser(description='Set population paramters for antigens and lymphocytes.',
                                     add_help=True)
    req_args = parser.add_argument_group('Required Arguments')
    req_args.add_argument('-e', dest='epitope',
                          help='REQUIRED: Set the desired linear epitope for the antigen [Example: ACDEFGHIKLM].',
                          required=True)
    req_args.add_argument('-n', dest='pop_size',
                          help='REQUIRED: Set how many antibodies are produced by B cell [Example: 100].',
                          required=True)
    req_args.add_argument('-d', dest='division_rate',
                          help='REQUIRED: Set the division rate of the antigen [Example: 2].',
                          required=True)
    req_args.add_argument('-p', dest='pop_num',
                          help='REQUIRED: Set the number of B cell populations.',
                          required=True)
    req_args.add_argument('-ex', dest='exchange_iter',
                          help='REQUIRED: Set the desired number of iterations for Somatic Hypermutaion.',
                          required=True)
    req_args.add_argument('-ri', dest='is_reinf',
                          help='REQUIRED: Set 1 if reinfection occurs, else 0',
                          required=True)
    return parser
