"""
This script is used to draw circos plot for the difference of two scans
The links are kept at 20% threshold. I.e., only the top 20% maximum differences are plotted
"""
import csv
from mmdps.proc import netattr, atlas, job
from mmdps.util import loadsave
from mmdps.vis.bnv import gen_matlab, get_mesh
from mmdps.vis import braincircos
import numpy as np

atlasobj = atlas.get('brodmann_lrce')
# subject_list = ['tanenci_20170601', 'tanenci_20170706', 'tanenci_20170814', 'tanenci_20170922', 'tanenci_20171117']
subject_list = ['wangwei_20171107', 'wangwei_20171221', 'wangwei_20180124', 'wangwei_20180211', 'wangwei_20180520']
subject_list = ['xiezhihao_20180416', 'xiezhihao_20180524']

# load in the given subject's net
net1 = netattr.Net(loadsave.load_csvmat('Y:/BOLD/%s/brodmann_lrce/bold_net/corrcoef.csv' % subject_list[0]), atlasobj)
net1.data = abs(net1.data)
net2 = netattr.Net(loadsave.load_csvmat('Y:/BOLD/%s/brodmann_lrce/bold_net/corrcoef.csv' % subject_list[-1]), atlasobj)
net2.data = abs(net2.data)

net2.data -= net1.data

# set a threshold mask
netList = sorted(abs(net2.data.ravel()))
threshold = netList[int(0.95*len(netList))]
net2.data[abs(net2.data) < threshold] = 0
builder = braincircos.CircosPlotBuilder(atlasobj, '%s 2th minus\n%s 1th abs top5%%' % (subject_list[-1].replace('_', ' '), subject_list[0].replace('_', ' ')), 'xiezhihao/xiezhihao 21 circos abs top5.png')
builder.add_circoslink(braincircos.CircosLink(net2, threshold = 0))
builder.plot()
exit()
for i in range(1, len(subject_list)):
	# load in the given subject's net
	net1 = netattr.Net(loadsave.load_csvmat('Y:/BOLD/%s/brodmann_lrce/bold_net/corrcoef.csv' % subject_list[i-1]), atlasobj)
	net1.data = abs(net1.data)
	net2 = netattr.Net(loadsave.load_csvmat('Y:/BOLD/%s/brodmann_lrce/bold_net/corrcoef.csv' % subject_list[i]), atlasobj)
	net2.data = abs(net2.data)

	net2.data -= net1.data

	# set a threshold mask
	netList = sorted(abs(net2.data.ravel()))
	threshold = netList[int(0.95*len(netList))]
	# net2.data[abs(net2.data) < threshold] = 0
	builder = braincircos.CircosPlotBuilder(atlasobj, '%s %dth minus\n%s %dth abs higher 0.6' % (subject_list[i].replace('_', ' '), i+1, subject_list[i-1].replace('_', ' '), i), 'wangwei/wangwei %d%d circos abs higher 0.6.png' % (i+1, i))
	builder.add_circoslink(braincircos.CircosLink(net2, threshold = 0.6))
	builder.plot()
	