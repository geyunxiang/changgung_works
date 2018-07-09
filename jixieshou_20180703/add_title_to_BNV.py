"""
This script is used to add title (texts) to BNV plots
"""

from PIL import  Image, ImageDraw, ImageFont
import os

subject_list_tanenci = ['tanenci_20170601', 'tanenci_20170706', 'tanenci_20170814', 'tanenci_20170922', 'tanenci_20171117']
subject_list_wangwei = ['wangwei_20171107', 'wangwei_20171221', 'wangwei_20180124', 'wangwei_20180211', 'wangwei_20180520']
subject_list_xiezhihao = ['xiezhihao_20180416', 'xiezhihao_20180524']

for filename in os.listdir('xiezhihao'):
	if filename.find('node') == -1:
		continue
	title = filename.split(' ')[0] + ' ' + filename.split(' ')[1] + ' ' + filename.split(' ')[2]
	# timepart = filename.split(' ')[1] # filename = 'tanenci 32 node.png'
	# timepart = (int(timepart[0]), int(timepart[1]))
	generatedpng = os.path.join('xiezhihao', filename)
	img = Image.open(generatedpng)
	draw = ImageDraw.Draw(img)
	font = ImageFont.truetype('arial.ttf', 64)
	draw.text((50, 0.85*img.height), title, (0, 0, 0), font=font)
	# draw.text((50, 0.85*img.height+64), '%s %dth' % (subject_list_tanenci[timepart[1]-1].replace('_', ' '), timepart[1]), (0, 0, 0), font=font)
	newpng = generatedpng[:-4] + '_decorated.png'
	img.save(newpng)