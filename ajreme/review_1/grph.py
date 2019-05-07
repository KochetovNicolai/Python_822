from json import load
from mkwrld import CreateWorld
from argparse import ArgumentParser


parser = ArgumentParser(description='World creator')

parser.add_argument('--example', nargs='?', type=str,
                    default=None, help='# of example to show.\
                    Other arguments will be ignored.')
parser.add_argument('--N', type=int, nargs='?',
                    default=None, help='# of rows in world')
parser.add_argument('--M', type=int, nargs='?',
                    default=None, help='# of columns in world')
parser.add_argument('--seed', type=int, default=None,
                    nargs='?', help='world seed')
parser.add_argument('--sea_level', nargs='?', type=float,
                    default=None, help='sea level')
parser.add_argument('--biome_table_name', nargs='?', type=str,
                    default=None, help='.csv name')
parser.add_argument('--file_name', nargs='?', type=str,
                    default=None, help='\"show\" by default or \
                    save with name file_name. Example: \'file.jpeg\'')

args = dict(parser.parse_args()._get_kwargs())
if args['example'] is not None:
    with open('examples/example' + str(args['example']) + '.json', 'r') as ex:
        CreateWorld(**load(ex))
elif args['N'] is not None and args['M'] is not None:
    args = [*filter(lambda x: x[1] is not None, args.items())]
    CreateWorld(**dict(args))
else:
    print('args --N and --M must be specified.')
