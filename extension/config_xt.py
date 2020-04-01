import yaml
import argparse
from termcolor import colored

class ConfigXT(object):
    def __init__(self, config_file=None):
        parser = None
        if config_file is None:
            parser = argparse.ArgumentParser()
            parser.add_argument('-f', '--file', type=str, default='./config/default.yml')
            namespace, _ = parser.parse_known_args()
            config_file = namespace.file

        self.load(config_file)
        self.parse(parser)
    
    def load(self, filename):
        yaml_file = open(filename, 'r')
        yaml_dict = yaml.safe_load(yaml_file)
        
        vars(self).update(yaml_dict)

    def save(self, filename=None, verbose=False):
        yaml_dict = dict()
        for var in vars(self):
            if var not in ['file', 'verbose']:
                value = getattr(self, var)
                yaml_dict[var] = value

        with open(filename, 'w') as yaml_file:
            yaml.dump(yaml_dict, yaml_file, sort_keys=False)
            if verbose:
                print('Configuration file is saved to \'%s\'' % (filename))

    def parse(self, parser):
        if parser is not None:
            for var in vars(self):
                value = getattr(self, var)
                argument = '--' + var
                if type(value) is list:
                    parser.add_argument(argument, nargs="*", type=type(value[0]), default=value)
                else:
                    parser.add_argument(argument, type=type(value), default=value)

            parser.add_argument('-v', '--verbose', action='store_true')
            args = parser.parse_args()
            self.verbose(args.verbose)

            for var in vars(args):
                if var not in ['f', 'v']:
                    setattr(self, var, getattr(args, var))
            
    def verbose(self, v):
        if v:
            print(colored('[ Configurations ]', 'green'))
            for var in vars(self):
                value = getattr(self, var)
                print(colored('| ', 'green') + colored(var, 'blue') + ': ' + str(value))

            print('\n')

def main():
    config = ConfigXT()

if __name__ == "__main__":
    main()