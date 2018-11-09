
import argparse
import os

import yaml

# mof_dir = '/ihome/cwilmer/kbs37/MOFs/CoRE6000'
# output_dir = '/ihome/cwilmer/kbs37/git/autografs/scratch/mofs'
def type_cifs(mof_dir_path, output_dir, package, ff):

    os.makedirs(output_dir, exist_ok=True)

    if package.lower() == "autografs":
        from autografs_type_mofs import autografs_type_mofs
        mof_atom_types, err_mofs = autografs_type_mofs(mof_dir_path, output_dir, ff)
    else:
        raise Exception("Package %s not implemented yet" % package)

    # Save unique atom types
    with open(os.path.join(output_dir, "autografs_%s_atom_types.yaml" % ff), 'w') as f:
        yaml.dump(mof_atom_types, f)

    # Save error MOFs
    with open(os.path.join(output_dir, "autografs_%s_err_mofs.yaml" % ff), 'w') as f:
        yaml.dump(err_mofs, f)


# def cmdline():
parser = argparse.ArgumentParser("./atom_types.py")
parser.add_argument('mof_dir_path', help="Path to directory with MOF CIF files in it")
parser.add_argument('output_dir', help="Path to directory to output all atom types and summaries")
parser.add_argument('package', help="package to use: can be autografs or smit")
parser.add_argument('forcefield', help="forcefield to use: can be UFF or UFF4MOF")
args = parser.parse_args()

type_cifs(args.mof_dir_path, args.output_dir, args.package, args.forcefield)
