import os
import subprocess
import yaml

def get_types_from_lammps_data_file(path):
    proc = subprocess.run("awk '/Masses/,/Bond Coeffs/'  %s | ggrep -Po '.+# \K.+' | tr '\n' ' '" % path, \
                            shell=True, stdout=subprocess.PIPE, universal_newlines=True)
    atom_types = proc.stdout.split()
    atom_types.sort()
    return atom_types

rundir = "run6"
results = {}
for dir in os.listdir(rundir):
     if dir.endswith(".1"):
         mofname = dir[:-2]
         mofdatafile = os.path.join(rundir, dir, mofname + ".data")
         atom_types = get_types_from_lammps_data_file(mofdatafile)
         results[mofname] = atom_types

print(yaml.dump(results))
