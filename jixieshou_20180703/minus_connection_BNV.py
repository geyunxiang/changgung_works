"""
This script is used to prepare BNV edge file for the difference of two scans
The links are kept at 20% threshold. I.e., only the top 20% maximum differences are plotted
"""
import csv
from mmdps.proc import netattr, atlas, job, parabase
from mmdps.util import loadsave
from mmdps.vis.bnv import gen_matlab, get_mesh
import numpy as np

atlasobj = atlas.get('brodmann_lrce')
# subject_list = ['tanenci_20170601', 'tanenci_20170706', 'tanenci_20170814', 'tanenci_20170922', 'tanenci_20171117']
subject_list = ['wangwei_20171107', 'wangwei_20171221', 'wangwei_20180124', 'wangwei_20180211', 'wangwei_20180520']

# load in the given subject's net
net1 = netattr.Net(loadsave.load_csvmat('Y:/BOLD/xiezhihao_20180416/brodmann_lrce/bold_net/corrcoef.csv'), atlasobj)
net2 = netattr.Net(loadsave.load_csvmat('Y:/BOLD/xiezhihao_20180524/brodmann_lrce/bold_net/corrcoef.csv'), atlasobj)

net2.data -= net1.data

# set a threshold mask
netList = sorted(abs(net2.data.ravel()))
threshold = netList[int(0.8*len(netList))]
net2.data[abs(net2.data) < threshold] = 0
loadsave.save_csvmat('E:/Changgung works/jixieshou_20180703/xiezhihao/xiezhihao 21 link.edge', net2.data, delimiter = '\t')
mstr = gen_matlab('E:/MMDPSoftware/mmdps/atlas/brodmann_lrce/brodmann_lrce_samesize.node', 'E:/Changgung works/jixieshou_20180703/xiezhihao/xiezhihao 21 link.edge', 'abc', 'E:/Changgung works/jixieshou_20180703/xiezhihao/xiezhihao 21 link.png', get_mesh('ch2cere'), 'E:/Changgung works/jixieshou_20180703/BNV_diffedge_options.mat')
j = job.MatlabJob('bnv', mstr)
j.run()
exit()

jobList = []
for i in range(1, len(subject_list)):
	# load in the given subject's net
	net1 = netattr.Net(loadsave.load_csvmat('Y:/BOLD/%s/brodmann_lrce/bold_net/corrcoef.csv' % subject_list[i-1]), atlasobj)
	net2 = netattr.Net(loadsave.load_csvmat('Y:/BOLD/%s/brodmann_lrce/bold_net/corrcoef.csv' % subject_list[i]), atlasobj)

	net2.data -= net1.data

	# set a threshold mask
	netList = sorted(abs(net2.data.ravel()))
	threshold = netList[int(0.8*len(netList))]
	net2.data[abs(net2.data) < threshold] = 0
	loadsave.save_csvmat('E:/Changgung works/jixieshou_20180703/wangwei/wangwei %d%d link.edge' % (i+1, i), net2.data, delimiter = '\t')
	# mstr = gen_matlab(nodepath, edgepath, self.title, self.outfilepath, bnv_mesh, bnv_cfg)
	mstr = gen_matlab('E:/MMDPSoftware/mmdps/atlas/brodmann_lrce/brodmann_lrce_samesize.node', 'E:/Changgung works/jixieshou_20180703/wangwei/wangwei %d%d link.edge' % (i+1, i), 'abc', 'E:/Changgung works/jixieshou_20180703/wangwei/wangwei %d%d link.png' % (i+1, i), get_mesh('ch2cere'), 'E:/Changgung works/jixieshou_20180703/BNV_diffedge_options.mat')
	j = job.MatlabJob('bnv', mstr)
	jobList.append(j.run)
	j.run()
