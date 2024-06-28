# This script run docking of PDBs to the map by COLORES 
# which is a part of the Situs package, needs to be installed separately.
import os
from glob import glob

#Name of the map file and parameters of the map
mrc_file = "map.mrc"
res = 8.0
cutoff = 0.009


#AlphaFold PDB files should be in the "001","002", etc subdirectories.
pdbs = []
for d in sorted(glob("00?")):
    pdbs.extend(glob(f"{d}/*pdb"))

for pdb in pdbs:

    base_dir = os.path.dirname(pdb)
    results_dir = base_dir + "_colores_results"
    os.system(f"mkdir -p {results_dir}")
    
    output_name_base = (os.path.basename(pdb)).split(".")[0]
    check_file_name = f"./{results_dir}/{output_name_base}_done.txt"
    if not os.path.isfile(check_file_name):
        os.system(f"colores {mrc_file} {pdb} -res {res} -explor 3 -cutoff {cutoff}")
        for out_file in glob("col_*"):
            new_name = output_name_base + "_" + out_file
            os.system(f"mv {out_file} ./{results_dir}/{new_name}")
        os.system(f"touch {check_file_name}")
