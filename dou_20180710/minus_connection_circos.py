"""
This script is used to draw circos plot for the difference of two scans
To separate different signs of correlation coefficients in the first and second scans, 
the links are divided into 4 categories.
- pos2pos
- pos2neg
- neg2pos
- neg2neg
"""
import csv, copy, math
from mmdps.proc import netattr, atlas, job
from mmdps.util import loadsave
from mmdps.vis.bnv import gen_matlab, get_mesh
from mmdps.vis import braincircos
from mmdps_util import stats_utils
import numpy as np

ordinal = lambda n: "%d%s" % (n,"tsnrhtdd"[(math.floor(n/10)%10!=1)*(n%10<4)*n%10::4])

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

def pos2neg(net1, net2):
	ret1 = copy.deepcopy(net1)
	ret2 = copy.deepcopy(net2)
	mask = np.logical_not(np.logical_and(net1.data > 0, net2.data < 0))
	ratio = (mask.size - np.count_nonzero(mask))/float(mask.size)
	ret1.data[mask] = 0
	ret2.data[mask] = 0
	return(ret1, ret2, ratio)

def neg2pos(net1, net2):
	ret1 = copy.deepcopy(net1)
	ret2 = copy.deepcopy(net2)
	mask = np.logical_not(np.logical_and(net1.data < 0, net2.data > 0))
	ratio = (mask.size - np.count_nonzero(mask))/float(mask.size)
	ret1.data[mask] = 0
	ret2.data[mask] = 0
	return(ret1, ret2, ratio)

atlasobj = atlas.get('brodmann_lrce')
# subject_list = ['tanenci_20170601', 'tanenci_20170706', 'tanenci_20170814', 'tanenci_20170922', 'tanenci_20171117']
subject_list = ['wangwei_20171107', 'wangwei_20171221', 'wangwei_20180124', 'wangwei_20180211', 'wangwei_20180520']
# subject_list = ['xiezhihao_20180416', 'xiezhihao_20180524']

# load in the given subject's net
net1 = netattr.Net(loadsave.load_csvmat('Y:/BOLD/%s/brodmann_lrce/bold_net/corrcoef.csv' % subject_list[0]), atlasobj)
wd1 = netattr.Attr(loadsave.load_csvmat('Y:/BOLD/%s/brodmann_lrce/bold_net_attr/inter-region_wd.csv' % subject_list[0]), atlasobj)
# net1.data = abs(net1.data)
net2 = netattr.Net(loadsave.load_csvmat('Y:/BOLD/%s/brodmann_lrce/bold_net/corrcoef.csv' % subject_list[-1]), atlasobj)
wd2 = netattr.Attr(loadsave.load_csvmat('Y:/BOLD/%s/brodmann_lrce/bold_net_attr/inter-region_wd.csv' % subject_list[-1]), atlasobj)
# net2.data = abs(net2.data)

net1, net2, ratio = all_neg(net1, net2)
net2.data -= net1.data
# net2.data = abs(net2.data) - abs(net1.data)

wd2.data -= wd1.data

# set a threshold mask
# netList = sorted(abs(net2.data.ravel()))
# threshold = netList[int(0.95*len(netList))]
# net2.data[abs(net2.data) < threshold] = 0
builder = braincircos.CircosPlotBuilder(atlasobj, '%s 5th minus\n%s 1th all neg\nratio = %1.3f' % (subject_list[-1].replace('_', ' '), subject_list[0].replace('_', ' '), ratio), '%s/%s 51 circos all neg test.png' % (subject_list[0].split('_')[0], subject_list[0].split('_')[0]))
builder.add_circoslink(braincircos.CircosLink(net2, threshold = 0))
builder.add_circosvalue(braincircos.CircosValue(wd2))
builder.plot()
exit()
for i in range(1, len(subject_list)):
	# load in the given subject's net
	net1 = netattr.Net(loadsave.load_csvmat('Y:/BOLD/%s/brodmann_lrce/bold_net/corrcoef.csv' % subject_list[i-1]), atlasobj)
	net2 = netattr.Net(loadsave.load_csvmat('Y:/BOLD/%s/brodmann_lrce/bold_net/corrcoef.csv' % subject_list[i]), atlasobj)

	sigRegions = stats_utils.row_wise_ttest(net1, net2)
	sigAttr = netattr.Attr(sigRegions, atlasobj)

	net1, net2, ratio = neg2pos(net1, net2)
	# net2.data -= net1.data
	net2.data = abs(net2.data) - abs(net1.data)

	# set a threshold mask
	# netList = sorted(abs(net2.data.ravel()))
	# threshold = netList[int(0.95*len(netList))]
	# net2.data[abs(net2.data) < threshold] = 0
	builder = braincircos.CircosPlotBuilder(atlasobj, '%s %dth minus\n%s %dth neg 2 pos\nratio = %1.3f' % (subject_list[i].replace('_', ' '), i+1, subject_list[i-1].replace('_', ' '), i, ratio), '%s/%s %d%d circos neg 2 pos.png' % (subject_list[i].split('_')[0], subject_list[i].split('_')[0], i+1, i))
	builder.add_circoslink(braincircos.CircosLink(net2, threshold = 0))
	builder.add_circosvalue(braincircos.CircosValue(sigAttr, (0, 1)))
	builder.plot()
	