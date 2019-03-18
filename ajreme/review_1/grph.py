import argparse
from mkwrld import CreateWorld


parser = argparse.ArgumentParser(description='World creator')
    
parser.add_argument('N', type=int, help='# of rows in world')
parser.add_argument('M', type=int, help='# of columns in world')
parser.add_argument('seed', type=int, nargs='?', help='world seed')
parser.add_argument('sea_level', nargs='?', type=float, help='sea level')
parser.add_argument('biome_table_name', nargs='?', type=str, help='.csv name')

args = [*filter(lambda x: x[1] != None, parser.parse_args()._get_kwargs())]
CreateWorld(**dict(args))