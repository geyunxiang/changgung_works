"""
This script is used to load in t-test result and prepare BNV edge file
"""

import csv
from mmdps.proc import netattr, atlas
from mmdps.util import loadsave
import numpy as np
# read in the significant difference csv file
sigConnections = [] # a list of tuples
with open('Z:/changgeng/jixieshou/controlexperimental/bold_net/net_ttest/original_value/patientE_after-before_paired_ttest_report.csv') as f:
	reader = csv.DictReader(f, delimiter = ',')
	for row in reader:
		connection = (row['RegionA'], row['RegionB'])
		reversedConnection = (row['RegionB'], row['RegionA'])
		if connection in sigConnections or reversedConnection in sigConnections:
			continue
		sigConnections.append(connection)

# load in the given subject's net
atlasobj = atlas.get('brodmann_lrce')
net = netattr.Net(loadsave.load_csvmat('Y:/BOLD/wangwei_20171107/brodmann_lrce/bold_net/corrcoef.csv'), atlasobj)

# find the appropriate nodes and links and output as BNV expected
plotNet = netattr.Net(np.zeros((atlasobj.count, atlasobj.count)), atlasobj) # all zero matrix
for connection in sigConnections:
	plotNet.data[atlasobj.ticks.index(connection[0]), atlasobj.ticks.index(connection[1])] = 1.0
	plotNet.data[atlasobj.ticks.index(connection[1]), atlasobj.ticks.index(connection[0])] = 1.0
loadsave.save_csvmat('E:/Changgung works/jixieshou_20180703/wangwei_20171107_link.edge', plotNet.data)
