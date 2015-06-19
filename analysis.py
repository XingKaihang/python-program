"""
edit by Xing Kaihang
date: 2015-06-18
take exactly 2 parameters, the first one is the root path, the second one is the target files' pattern

"""

import sys
import os
import re
import time
import datetime
target_file_list = []
saved_file_name = "result.txt"
result = open(saved_file_name,'w')
standerd_time = time.strptime("15:30:00","%H:%M:%S")
sort_list = []
result_directory = {}

"""judge a file's name format"""
def judge_filename(path_filename, pattern):
	global target_file_list
	path,filename = os.path.split(path_filename)
	if re.match(pattern,filename) is not None:
		target_file_list.append(os.path.abspath(path_filename))



""" find all the files that needed to be analysed, and return their pathes in a list"""
def find_all_target_files(root, pattern):
	for item in os.listdir(root):
		path_item = os.path.join(root,item)
		if os.path.isfile(path_item):
			judge_filename(path_item,pattern)
		if os.path.isdir(path_item):
			find_all_target_files(path_item,pattern)


"""convert and save into sort list"""
def convert_save(line_list):
	global standerd_time,sort_list
	line_date = time.strptime(line_list[0],"%Y-%m-%d")
	line_week = time.strftime("%w",line_date)
	line_time = time.strptime(line_list[1].split('.')[0],"%H:%M:%S")
	result_date = line_list[0]
	if line_time > standerd_time:
		if line_week == 5:
			date = datetime.datetime(line_date[0], line_date[1],line_date[2]) + datetime.timedelta(days =3)
			result_date = str(date)
			result_date = result_date.split(' ')[0]
		else:
			date = datetime.datetime(line_date[0], line_date[1],line_date[2]) + datetime.timedelta(days =1)
			result_date = str(date)
			result_date = result_date.split(' ')[0]
	result_pnl = round(float(line_list[3]),1)
	sort_list.append( line_list[0]+line_list[1]+', '+result_date+', '+line_list[2]+', '+str(int(line_list[4]))+', '+str(result_pnl))


"""analyse 1 file"""
def analysis(single_file):
	f = open(single_file,'r')
	for line in f:
		line_list = line.split(' ')
		if line_list[7]=="pos=0":
			line_list_afterFilter = []
			line_list_afterFilter.append(line_list[0].replace('[',''))
			line_list_afterFilter.append(line_list[1].replace(']',''))
			line_list_afterFilter.append(line_list[4].replace('[','').replace(']',''))
			line_list_afterFilter.append(line_list[5].replace('CloseProfit=',''))
			line_list_afterFilter.append(line_list[8].replace('tot_volume=',''))
			# print line_list_afterFilter
			convert_save(line_list_afterFilter)
	f.close()


"""filter the sorted results, and save them to the result file"""
def save_to_file():
	global sort_list,result_directory
	for item in sort_list:
		item_list = item.split(', ')
		
		if result_directory.has_key(item_list[1]+item_list[2]):
			temp_list = result_directory[item_list[1]+item_list[2]]
			if int(temp_list[2]) < int(item_list[3]):
				result_directory[item_list[1]+item_list[2]] = [item_list[1],item_list[2],item_list[3],item_list[4],temp_list[4],temp_list[5]]
			else:
				result_directory[item_list[1]+item_list[2]] = [item_list[1],item_list[2],item_list[3],item_list[4],str(int(temp_list[4])+int(temp_list[2])),str(float(temp_list[5])+float(temp_list[3]))]
		else:
			#date,id,volume,pnl,base_volume,base_pnl
			result_directory[item_list[1]+item_list[2]] = [item_list[1],item_list[2],item_list[3],item_list[4],0,0]
		# if item_list[2]=="cu1508":
		# 	print result_directory[item_list[1]+item_list[2]]
	temp_list = []
	for key,value in result_directory.items():
		#print value
		temp_list.append( value[0] +', '+ value[1] +', '+ str(int(value[2])+int(value[4])) +', '+ str(round(float(value[3])+float(value[5]),1)) )
	temp_list.sort()
	for item in temp_list:
		result.write(item+"\n")
	statistics_information(temp_list)


"""print out statistics information"""
def statistics_information(temp_list):
	length = len(temp_list)
	if length>0:
		print "From "+ temp_list[0].split(", ")[0] +" to "+ temp_list[length-1].split(", ")[0]
		print "id\tvolume\tpnl"
		directory = {}
		for line in temp_list:
			list_line = line.split(", ")
			if directory.has_key(list_line[1]):
				directory[list_line[1]] = [directory[list_line[1]][0]+int(list_line[2]), directory[list_line[1]][1]+float(list_line[3])]
			else:
				directory[list_line[1]] = [int(list_line[2]),float(list_line[3])]
		for key,value in directory.items():
			print key+"\t"+str(value[0])+"\t"+str(value[1])


if __name__=="__main__":
	result.write("date,id,volume,pnl\n")
	root = sys.argv[1]
	pattern = sys.argv[2]
	find_all_target_files(root,pattern)
	for single_file in target_file_list:
		analysis(single_file)
	sort_list.sort()
	# for item in sort_list:
	# 	print item
	save_to_file()
	result.close()
	print "\nresults have been written to "+saved_file_name




