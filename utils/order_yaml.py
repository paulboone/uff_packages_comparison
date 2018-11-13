# resorts a yaml file, if necessary (shouldn't be, any more)
#

import os

import yaml

def order_yaml_key(filename):
    config=yaml.load(open(filename))

    dh = {k:[str(i) for i in sorted(set(config[k]))] for k in config}

    with open(filename + "ordered", 'w') as f:
        yaml.dump(dh, f)

order_yaml_key('output/boyd_smit_uff/boyd_smit_uff_atom_types.yaml')
order_yaml_key('output/boyd_smit_uff4mof/boyd_smit_uff4mof_atom_types.yaml')
