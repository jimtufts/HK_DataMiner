__author__ = 'stephen'
# ===============================================================================
# GLOBAL IMPORTS:
import os,sys
import numpy as np
import argparse

# ===============================================================================
# LOCAL IMPORTS:
#HK_DataMiner_Path = os.path.relpath(os.pardir)
#HK_DataMiner_Path = os.path.abspath("/home/stephen/Dropbox/projects/work-2016.8/hk_dataminer/")
HK_DataMiner_Path = os.path.relpath(os.pardir)
print(HK_DataMiner_Path)
sys.path.append(HK_DataMiner_Path)
from cluster import KCenters
#from lumping import PCCA, PCCA_Standard, SpectralClustering, Ward
from utils import XTCReader, plot_cluster, utils, split_assignments
# ===============================================================================
cli = argparse.ArgumentParser()
cli.add_argument('-t',   '--trajListFns', default = 'trajlist',
                 help='List of trajectory files to read in, separated by spaces.')
cli.add_argument('-a', '--atomListFns', default='atom_indices',
                 help='List of atom index files to read in, separated by spaces.')
cli.add_argument('-g',   '--topology', default='native.pdb', help='topology file.')
cli.add_argument('-o',   '--homedir',  help='Home dir.', default=".", type=str)
cli.add_argument('-e',   '--iext', help='''The file extension of input trajectory
                 files.  Must be a filetype that mdtraj.load() can recognize.''',
                 default="xtc", type=str)
cli.add_argument('-n',   '--n_clusters', help='''n_clusters.''',
                 default=100, type=int)
cli.add_argument('-m',   '--n_macro_states', help='''n_macro_states.''',
                 default=6, type=int)
cli.add_argument('-s',   '--stride', help='stride.',
                 default=None, type=int)

args = cli.parse_args()
trajlistname = args.trajListFns
atom_indicesname = args.atomListFns
trajext = args.iext
File_TOP = args.topology
homedir = args.homedir
n_clusters = args.n_clusters
n_macro_states = args.n_macro_states
stride = args.stride
# ===========================================================================
# Reading Trajs from XTC files
print("stride:", stride)
trajreader = XTCReader(trajlistname, atom_indicesname, homedir, trajext, File_TOP, nSubSample=stride)
trajs = trajreader.trajs
traj_len = trajreader.traj_len
np.savetxt("./traj_len.txt", traj_len, fmt="%d")

if os.path.isfile("./phi_angles.txt") and os.path.isfile("./psi_angles.txt") is True:
    phi_angles = np.loadtxt("./phi_angles.txt", dtype=np.float32)
    psi_angles = np.loadtxt("./psi_angles.txt", dtype=np.float32)
    phi_psi = np.column_stack((phi_angles, psi_angles))
else:
    phi_angles, psi_angles = trajreader.get_phipsi(trajs, psi=[6, 8, 14, 16], phi=[4, 6, 8, 14])
    #phi_psi = np.column_stack((phi_angles, psi_angles))
    np.savetxt("./phi_angles.txt", phi_angles, fmt="%f")
    np.savetxt("./psi_angles.txt", psi_angles, fmt="%f")
#phi_angles, psi_angles = trajreader.get_phipsi(trajs, psi=[6, 8, 14, 16], phi=[4, 6, 8, 14])
#phi_psi=np.column_stack((phi_angles, psi_angles))

# ===========================================================================
# do Clustering using KCenters method
#cluster = KCenters(n_clusters=n_clusters, metric="euclidean", random_state=0)
cluster = KCenters(n_clusters=n_clusters, metric="rmsd", random_state=0)
print(cluster)
#cluster.fit(phi_psi)
cluster.fit(trajs)

labels = cluster.labels_
print(labels)
n_microstates = len(set(labels)) - (1 if -1 in labels else 0)
print('Estimated number of clusters: %d' % n_microstates)

cluster_centers_ = cluster.cluster_centers_
# plot micro states
clustering_name = "kcenters_n_" + str(n_microstates)
splited_assignments =split_assignments(labels, traj_len)
#np.savetxt("assignments_"+clustering_name+".txt", labels, fmt="%d")
np.savetxt("assignments_"+clustering_name+".txt", splited_assignments , fmt="%d")
np.savetxt("cluster_centers_"+clustering_name+".txt", cluster_centers_, fmt="%d")
plot_cluster(labels=labels, phi_angles=phi_angles, psi_angles=psi_angles, name=clustering_name)
trajs[cluster_centers_].save("cluster_centers.pdb")
#trajs_sub_atoms[cluster_centers_].save("cluster_centers_sub_atoms.pdb")
