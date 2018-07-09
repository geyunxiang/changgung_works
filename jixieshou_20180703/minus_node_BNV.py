"""
This script is used to prepare BNV node file for the difference of two scans
The node attribute can be 'inter-region_wd.csv'
"""
import csv
from mmdps.proc import netattr, atlas, job
from mmdps.util import loadsave
from mmdps.vis.bnv import gen_matlab, get_mesh
import numpy as np

# load in the given subject's attributes
atlasobj = atlas.get('brodmann_lrce')
subject_list = ['tanenci_20170601', 'tanenci_20170706', 'tanenci_20170814', 'tanenci_20170922', 'tanenci_20171117']
# subject_list = ['wangwei_20171107', 'wangwei_20171221', 'wangwei_20180124', 'wangwei_20180211', 'wangwei_20180520']

attr1 = netattr.Attr(loadsave.load_csvmat('Y:/BOLD/xiezhihao_20180416/brodmann_lrce/bold_net_attr/inter-region_wd.csv'), atlasobj)
attr2 = netattr.Attr(loadsave.load_csvmat('Y:/BOLD/xiezhihao_20180524/brodmann_lrce/bold_net_attr/inter-region_wd.csv'), atlasobj)

attr2.data -= attr1.data

# prepare BNV node file
atlasobj.bnvnode.change_value(attr2.data)
atlasobj.bnvnode.change_modular([int(d) for d in (attr2.data > 0)])
atlasobj.bnvnode.write('E:/Changgung works/jixieshou_20180703/xiezhihao/xiezhihao 21 node.node')
mstr = gen_matlab('E:/Changgung works/jixieshou_20180703/xiezhihao/xiezhihao 21 node.node', '', 'abc', 'E:/Changgung works/jixieshou_20180703/xiezhihao/xiezhihao 21 node.png', get_mesh('ch2cere'), 'E:/Changgung works/jixieshou_20180703/BNV_diffnode_options.mat')
j = job.MatlabJob('bnv', mstr)
j.run()
exit()

for i in range(1, len(subject_list)):
	attr1 = netattr.Attr(loadsave.load_csvmat('Y:/BOLD/%s/brodmann_lrce/bold_net_attr/inter-region_wd.csv' % subject_list[i-1]), atlasobj)
	attr2 = netattr.Attr(loadsave.load_csvmat('Y:/BOLD/%s/brodmann_lrce/bold_net_attr/inter-region_wd.csv' % subject_list[i]), atlasobj)

	attr2.data -= attr1.data

	# prepare BNV node file
	atlasobj.bnvnode.change_value(attr2.data)
	atlasobj.bnvnode.change_modular([int(d) for d in (attr2.data > 0)])
	atlasobj.bnvnode.write('E:/Changgung works/jixieshou_20180703/tanenci/tanenci %d%d node.node' % (i+1, i))
	mstr = gen_matlab('E:/Changgung works/jixieshou_20180703/tanenci/tanenci %d%d node.node' % (i+1, i), '', 'abc', 'E:/Changgung works/jixieshou_20180703/tanenci/tanenci %d%d node.png' % (i+1, i), get_mesh('ch2cere'), 'E:/Changgung works/jixieshou_20180703/BNV_diffnode_options.mat')
	j = job.MatlabJob('bnv', mstr)
	j.run()