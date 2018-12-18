
import argparse
import os

import yaml

# mof_dir = '/ihome/cwilmer/kbs37/MOFs/CoRE6000'
# output_dir = '/ihome/cwilmer/kbs37/git/autografs/scratch/mofs'


def type_cifs(path, output_dir, ff):
    os.makedirs(output_dir, exist_ok=True)

    if not os.path.isdir(path):
        # only do single file
        mof_atom_types = type_mof(path, output_dir, ff)
        print(mof_atom_types)
    else:
        # process all files in directory
        err_mofs = []
        mof_atom_types = {}
        mof_list = os.listdir(path)

        for idx, filename in enumerate(mof_list, start=1):
            print('%i | %s' % (idx, filename))
            try:
                mof_atom_types[mof_name] = type_mof(os.path.join(path, filename), output_dir, ff)
                # # Save atom types for each mof
                # with open(os.path.join(output_dir, '%s.yaml' % mof_name), 'w') as f:
                #     yaml.dump([str(i) for i in types], f)
            except Exception as e:
                err_mofs.append(filename)
                print("!!!ERROR -> {0}".format(e))

        # Save unique atom types
        with open(os.path.join(output_dir, "%s_%s_atom_types.yaml" % (package, ff)), 'w') as f:
            yaml.dump(mof_atom_types, f)

        # Save error MOFs
        with open(os.path.join(output_dir, "%s_%s_err_mofs.yaml" % (package, ff)), 'w') as f:
            yaml.dump(err_mofs, f)


# def cmdline():
parser = argparse.ArgumentParser("./atom_types.py")
parser.add_argument('mof_dir_path', help="Path to directory with MOF CIF files in it")
parser.add_argument('output_dir', default="./", help="Path to directory to output all atom types and summaries")
parser.add_argument('package', help="package to use: can be autografs / boyd_smit / openbabel")
parser.add_argument('forcefield', help="forcefield to use: can be UFF or UFF4MOF")
parser.add_argument('--output_files', default=True, help="output data file so geometry can be determined (specific to algorithm)")
args = parser.parse_args()

if args.package.lower() == "autografs":
    from autografs_type_mofs import type_mof
elif args.package.lower() == "boyd_smit":
    from boyd_smit_type_mofs import type_mof
elif args.package.lower() == "openbabel":
    from openbabel_type_mofs import type_mof
else:
    raise Exception("Package %s not implemented yet" % args.package)

type_cifs(args.mof_dir_path, args.output_dir, args.forcefield, args.output_files)
