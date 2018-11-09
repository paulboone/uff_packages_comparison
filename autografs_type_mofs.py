"""
Type (UFF) list of MOF (cif) files using Autografs.
"""
from autografs.utils.mmanalysis import analyze_mm
import ase
import yaml
import os


mof_dir = '/ihome/cwilmer/kbs37/MOFs/CoRE6000'
type_dir = '/ihome/cwilmer/kbs37/git/autografs/scratch/mofs'
mof_atom_types = {}
mof_list = os.listdir(mof_dir)
n_mofs = len(mof_list)
err_mofs = []

for idx, cif in enumerate(mof_list, start=1):
    print('%i | %s' % (idx, cif)) 
    try:
        mof = ase.io.read(os.path.join(mof_dir, cif))
        bonds, types = analyze_mm(mof, library="rappe")
        uniq_types = sorted(set(types))
        mof_name = cif.split('_')[0]
        mof_atom_types[mof_name] = [str(i) for i in uniq_types]

        # Save atom types for each mof
        with open(os.path.join(type_dir, '%s.yaml' % mof_name), 'w') as f:
            yaml.dump([str(i) for i in types], f)
    except Exception as e:
        err_mofs.append(cif)
        print('!!!ERROR -> %s' % e) 

# Save unique atom types
with open('autografs_atom_types.yaml','w') as f:
    yaml.dump(mof_atom_types, f)

# Save error MOFs
with open('autografs_err_mofs.yaml','w') as f:
    yaml.dump(err_mofs, f)
