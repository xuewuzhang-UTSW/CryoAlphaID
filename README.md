This set of scripts are designed to exhaustively search for proteins in a low-resolution cryo-EM map from a set of PDBs, such as the AlphaFold predicted structures of a proteome. This method was initially used in this publication (Chen et al, 2023), where the identities of some of the proteins in the maps were not known and the resolution of the map did not allow de novo model building. The COLORES module in the Situs package performs the docking of PDBs into the cryo-EM map (Wriggers, 2012). However, as pointed by Chen et al, the correlation coefficients from COLORES are often not a good indicator for goodness of fit. To deal with this issue, one of the scripts in this set uses EMAN2 (Tang et al, 2007) to calculate the Fourier Schell Correlation (FSC) between the docked PDB and the map, which in my experience is a much better metric for ranking the docking results. I also used DSSP to calculate the secondary structure statistics of the PDBs, which in some cases can help narrow down the candidates. This method was used to identify multiple proteins in the cryo-EM structure of mouse radial spoke 3 (RS3), a key metaboblic and regulatory hub in cilia (Zhao et al, 2025).  

Before you use the scripts, you need to install: 
Situs package (https://situs.biomachina.org/fguide.html);
DSSP (https://github.com/cmbi/hssp/releases); 
EMAN2 (https://blake.bcm.edu/emanwiki/EMAN2);
A Conda environment with Python 3, in which the Pandas package installed.

And of course, a cryo-EM map file in MRC format. It is better to crop the map to a smaller size containing the area of interest, while keeping the cubic shape with lengths of sides being an event number. This will make the calculations faster. With a box size of 50X50X50 or smaller, it should take a day or two to finish the entire mouse or human proteome, depending on how fast the computer is. 

To run the scripts:
1. Download PBDs from the AlaphaFold data base (https://alphafold.ebi.ac.uk/download#proteomes-section). Separate the PDB files into four subfolders in the current directory, named 001, 002, 003, 004 (to avoid having too many files in one directory, which makes it very slow to navigate).

2. Launch jupyter-lab or jupyter-notebook, run “get_pdb_info.ipynb” in the current directory to generate the secondary structure statistics for all the PDBs. This only need to be run once for each PDB set.

2. Run “run_colores.py” (Need to input the map file name and map parameters to the script). This will generate new directories with docked PDBs.

3. Run “sort_scores.ipynb” in jupyter, and “calculate_fsc.py” with python (need to input the map file name and parameters into the script). The end results are in this file: colores_CC_wRes.csv, which contains the ranked docking results. You can either use Excell to inspect this file, or just use Jupyter to sort and inspect the Pandas dataframe of the results. Hopefully, one of the highly ranked docking results is the correct solution.




Chen Z, Shiozaki M, Haas KM, Skinner WM, Zhao S, Guo C, Polacco BJ, Yu Z, Krogan NJ, Lishko PV et al (2023) De novo protein identification in mammalian sperm using in situ cryoelectron tomography and AlphaFold2 docking. Cell 186: 5041-5053 e5019

Tang G, Peng L, Baldwin PR, Mann DS, Jiang W, Rees I, Ludtke SJ (2007) EMAN2: an extensible image processing suite for electron microscopy. J Struct Biol 157: 38-46

Wriggers W (2012) Conventions and workflows for using Situs. Acta crystallographica 68: 344-351

Zhao, Y., K. Song, A. Tavakoli, L. Gui, A. Fernandez-Gonzalez, S. Zhang, P. P. Dzeja, S. A. Mitsialis, X. Zhang, and D. Nicastro. "Mouse Radial Spoke 3 Is a Metabolic and Regulatory Hub in Cilia." Nat Struct Mol Biol  (Jun 27 2025). https://dx.doi.org/10.1038/s41594-025-01594-6.

