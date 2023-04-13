import sys
import psycopg2 as pg
import os
from io import open
import pandas as pd


procedures = set()

from_env = sys.argv[2]
to_env = sys.argv[3]

def addCommitedFile(commit_item):
	if commit_item.endswith('.sql'):
		if commit_item.find('/procedures/') > 0:
			procedures.add(commit_item)			
def datashare_rename(file_name):
	conn = pg.connect(host=sys.argv[1], user=sys.argv[4], password=sys.argv[5], database=sys.argv[2], port=sys.argv[3], sslmode="require")
	lines = []
	print("entered into datashare replace")
	df = pd.read_sql('select * from data_gov.em_db_map', conn)
	df = df.loc[(df['rs_env_qa'].notnull())&(df['rs_env_prod'].notnull())] #added new line
	df = df.loc[(df['rs_env_qa'].str.lower()!='not in use')&(df['rs_env_prod'].str.lower()!='not in use')] #added new line
	DevDict = dict(zip(df['rs_env_qa'],df['rs_env_prod']))
	print(DevDict)
	InputContent = open(file_name,'r')
	for datashare_name in DevDict.keys():
		print("datashare_name :-",datashare_name)
		for line in InputContent:
			line = line.replace(datashare_name,DevDict[datashare_name])
			lines.append(line)
	InputContent.close()

	with open(file_name,'w') as output_file:
		for line in lines:
			# print(line)
			output_file.write(str(line))
def main():
	try:

		commit_file = "/tmp/git_diff_files_" + sys.argv[6]
		git_commit_list = []	
		with open(commit_file) as f:	
			for line in f.read().splitlines():
				git_commit_list.append('.' + os.sep + line)			  								
		print(git_commit_list)

		for commit_item in git_commit_list:
			#Ignore missing files for now. Deleted files on GIT are breaking the job
			if os.path.isfile(commit_item) == False:
				print("File could not be found: " + commit_item + ". Skipping...")
			if os.path.isfile(commit_item) == True:
				addCommitedFile(commit_item)

			else:
				print("File not found: " +  commit_item)
		print(procedures)

		for file_name in procedures:
			print("file_name:"+file_name)
			datashare_rename(file_name)



	except Exception as e:
		print(":" + getattr(e, 'strerror', str(e)))
		sys.exit(200)

	finally:
		print("done")

	print("Done")
	sys.exit(0)


if __name__ == '__main__':
	main()