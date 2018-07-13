"""
This script is used to draw circos plot of connections that have the same signs over
all scanning sessions. 
"""
import csv, copy
from mmdps.proc import netattr, atlas, job
from mmdps.util import loadsave
from mmdps.vis.bnv import gen_matlab, get_mesh
from mmdps.vis import braincircos
from mmdps_util import stats_utils, io_utils
import numpy as np

def all_pos(net1, net2):
	ret1 = copy.deepcopy(net1)
	ret2 = copy.deepcopy(net2)
	mask = np.logical_not(np.logical_and(net1.data > 0, net2.data > 0))
	ratio = (mask.size - np.count_nonzero(mask))/float(mask.size)
	ret1.data[mask] = 0
	ret2.data[mask] = 0
	return(ret1, ret2, ratio)

def all_neg(net1, net2):
	ret1 = copy.deepcopy(net1)
	ret2 = copy.deepcopy(net2)
	mask = np.logical_not(np.logical_and(net1.data < 0, net2.data < 0))
	ratio = (mask.size - np.count_nonzero(mask))/float(mask.size)
	ret1.data[mask] = 0
	ret2.data[mask] = 0
	return(ret1, ret2, ratio)

atlasobj = atlas.get('brodmann_lrce')
# scan_list = ['tanenci_20170601', 'tanenci_20170706', 'tanenci_20170814', 'tanenci_20170922', 'tanenci_20171117']
scan_list = ['wangwei_20171107', 'wangwei_20171221', 'wangwei_20180124', 'wangwei_20180211', 'wangwei_20180520']
# scan_list = ['xiezhihao_20180416', 'xiezhihao_20180524']

net_list = io_utils.loadAllNets('Y:/BOLD/', atlasobj, scanList = scan_list)

for i in range(1, len(scan_list)):
	net_list[i-1], net_list[i], _ = all_pos(net_list[i-1], net_list[i])

# net_list[-1] contains the final all same sign net
# net_list[-1].data[net_list[-1].data != 0] = 1

# plot this net
builder = braincircos.CircosPlotBuilder(atlasobj, '%s all positive' % (scan_list[0].split('_')[0]), '%s/%s all positive.png' % (scan_list[0].split('_')[0], scan_list[0].split('_')[0]))
builder.add_circoslink(braincircos.CircosLink(net_list[-1], threshold = 0))
builder.plot()
