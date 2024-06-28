#This script caculates the FSC between the map and the docked PDB
#Two thresholds are used: 0.2 and 0.5
#Run the first cell of "sort_scores.ipynb" before running this
#EMAN2 must be installed

import os
from glob import glob
import pandas as pd

#Map files name and the parameters of the map.
apix = 2.158
box_size = 20
ref_map = "map.mrc"

pdb_done = []
if os.path.isfile("resolution_scores.txt"):
    with open("resolution_scores.txt", 'r') as f:
        for l in f:
            pdb_done.append(l.split()[0])

out_res_scores = open("resolution_scores.txt", 'a')

pdbs = []
with open("colores_CC.csv","r") as cc:
    for line_number, line in enumerate(cc):
        if line_number>=1:
            name, folder = line.split()[0:2]
            if name not in pdb_done:
                pdbs.append(f"{folder}/{name}")


for index_pdb, pdb in enumerate(pdbs):
    folder_name, pdb_basename = pdb.split("/")
    print(f"\n*******working on {pdb}, Number {index_pdb+1:5d} of {len(pdbs)}********")
    out = open('tmp.pdb','w')
    with open(pdb,'r') as f:
        for line in f:
            if line.startswith("ATOM"):
                x = float(line[30:38]) - box_size*apix/2
                y = float(line[38:46]) - box_size*apix/2
                z = float(line[46:54]) - box_size*apix/2
                line = "".join([line[:30], f"{x:8.3f}", f"{y:8.3f}", f"{z:8.3f}",line[54:]])                                      
            out.write(f"{line}")
    out.close()

#EMAN2 must be installed and the EMAN2 comands must be in path
    os.system(f"e2pdb2mrc.py --res 7 --apix {apix} --box {box_size} --quick tmp.pdb tmp.mrc")
    os.system(f"e2fsc.py --threads 10 --apix {apix} {ref_map} tmp.mrc")
    with open('fsc.txt','r') as fsc:
        fsc05_res = 200
        fsc02_res = 200
        fsc05_set = False
        for fsc_line in fsc:
            fsc_res, fsc_score = map(float, fsc_line.split())
            if fsc_score <= 0.5 and fsc05_set is False:
                fsc05_res = 1/fsc_res
                fsc05_set = True
            if fsc_score <= 0.2:
                fsc02_res = 1/fsc_res
                out_res_scores.write(f"{pdb_basename} {folder_name} {fsc05_res:5.1f} {fsc02_res:5.1f}\n")
                print(f"{pdb_basename}  resolution(fsc05): {fsc05_res:5.1f}; resolution(fsc02): {fsc02_res:5.1f}\n")
                break
            

out_res_scores.close()


