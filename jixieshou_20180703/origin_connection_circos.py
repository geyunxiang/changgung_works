"""
This script is used to draw circos plot for the origin value of two scans
The links are kept at different threshold (top 5% or higher 0.6).
"""
import csv
from mmdps.proc import netattr, atlas, job
from mmdps.util import loadsave
from mmdps.vis.bnv import gen_matlab, get_mesh
from mmdps.vis import braincircos
import numpy as np

atlasobj = atlas.get('brodmann_lrce')
subject_list = ['tanenci_20170601', 'tanenci_20170706', 'tanenci_20170814', 'tanenci_20170922', 'tanenci_20171117']
# subject_list = ['wangwei_20171107', 'wangwei_20171221', 'wangwei_20180124', 'wangwei_20180211', 'wangwei_20180520']
# subject_list = ['xiezhihao_20180416', 'xiezhihao_20180524']

for i in range(0, len(subject_list)):
	# load in the given subject's net
	net1 = netattr.Net(loadsave.load_csvmat('Y:/BOLD/%s/brodmann_lrce/bold_net/corrcoef.csv' % subject_list[i-1]), atlasobj)
	# net1.data = abs(net1.data)

	# set a threshold mask
	netList = sorted(abs(net1.data.ravel()))
	threshold = netList[int(0.95*len(netList))]
	net1.data[abs(net1.data) < threshold] = 0
	builder = braincircos.CircosPlotBuilder(atlasobj, '%s %dth orig top 5%%' % (subject_list[i].replace('_', ' '), i+1), '%s/%s %dth circos orig top 5%%.png' % (subject_list[i].split('_')[0], subject_list[i].replace('_', ' '), i+1))
	builder.add_circoslink(braincircos.CircosLink(net1, threshold = 0))
	builder.plot()
	