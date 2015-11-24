import os, sys, sqlite3, time




class Database(object):
	def __init__(self, db_filename):
		self.file_location = db_filename
		self.connection_status = False

	def start(self):
		global connection
		if(self.connection_status == False):
			connection = sqlite3.connect(self.file_location)
			connection.text_factory = str
			print ' [+] SQLITE3: Connected to ' + str(self.file_location)
			self.connection_status = True
			return connection
		else:
			print ' [!] SQLITE3 [ERROR]: Already connected.'

	def stop(self):
		if(self.connection_status == True):
			if(connection):
				connection.close()
				print ' [+] SQLITE3: Connection closed.'



class Target:
	def __init__(self, name, timestamp):
		self.name = name
		self.timestamp = timestamp

	def add(self):
		c = connection.cursor()
		c.execute("INSERT INTO TARGETS (target_name,time) VALUES (" + "'" + str(self.name) + "'" + ',' + "'" + str(self.timestamp) + "'" + ")" )
		print ' [+] SQLITE3: Added ' + str(self.name) + ' to targets table.'
		c.execute('CREATE TABLE PROFILE_' + str(self.name) + ' (ID,COMMAND,TIMESTAMP)')
		print ' [+] SQLITE3: Created profile table for ' + str(self.name) + ' named PROFILE_' + str(self.name)
		os.mkdir('targets/' + str(self.name))
		print ' [+] IO: Created folder to store logs at "targets/' + str(self.name) + '"'

	def delete(self):
		c = connection.cursor()
		c.execute('DELETE FROM TARGETS where target_name=' + "'" + str(self.name) + "'")
		print ' [-] SQLITE3: Deleted ' + str(self.name) + 'from targets table.'
		c.execute('DROP TABLE PROFILE_' + str(self.name))
		print ' [-] SQLITE3: Dropped table PROFILE_' + str(self.name)
		os.rmdir('targets/' + str(self.name))
		print ' [-] IO: Removed folder of logs at "targets/' + str(self.name) + '"'

	def select(self):
		c = connection.cursor()
		c.execute("SELECT target_name FROM TARGETS WHERE target_name LIKE " + "'%" + str(self.name) + "%'")
		if(c.fetchone() <> None):
			return True
		else:
			return False







class Program:
	global targetFunc
	global profileFunc
	name = 'Kanai'
	version = '0.0.0'
	description = 'MITM Automation'
	banner = '''
  _   __                  _ 
 | | / /                 (_)
 | |/ /  __ _ _ __   __ _ _ 
 |    \ / _` | '_ \ / _` | |
 | |\  \ (_| | | | | (_| | |
 \_| \_/\__,_|_| |_|\__,_|_|
 ___________________________
 ''' + str(description) + '\n ' + str(name) + ' v.' + str(version) + '\n\n Initialization at: ' + str(time.ctime())
 	@staticmethod
 	def clean_screen():
 		if(os.name == 'posix'):
 			os.system('clear')
		return True

	def targetFunc(arguments):
		arg_analysis = arguments.split(' ')
		if(arg_analysis[0] == 'ADD'):
			if(len(arg_analysis) > 1):
				new_target = Target(arg_analysis[1],str(time.ctime()))
				new_target.add()
				print ' [+] Done.'
		if(arg_analysis[0] == 'DEL'):
			if(len(arg_analysis) > 1):
				del_target = Target(arg_analysis[1], str(time.ctime()))
				del_target.delete()
				print ' [-] Done.'
		if(arg_analysis[0] == 'SELECT'):
			if(len(arg_analysis) > 1):
				select_target = Target(arg_analysis[1], str(time.ctime()))
				if(select_target.select() == True):
					print ' [*] ' + str(select_target.name) + ' selected.'
				else:
					print ' [!] Could not find ' + str(select_target.name) + ' to select it.'

	def profileFunc():
		print 'Profile Function.'



	
	@staticmethod
	def command(string):
		global db
		if(string == 'PROFILE'):
			profileFunc()
		elif(string[0:len('target')] == 'TARGET'):
			arguments = string[len('TARGET '):]
			targetFunc(arguments)
		elif(string == 'SQL'):
			console = True
			c = connection.cursor()

			while console == True:
			
				sqlCmd = raw_input('	SQL> ')
				sqlCmd = sqlCmd.upper()
				if(sqlCmd <> 'QUIT'):
					c.execute(sqlCmd)
					print c.fetchall()
				else:
					console = False

		elif(string == 'QUIT'):
			db.stop()
			sys.exit(0)
		else:
			print 'No valid command was given.'








def init():
	global db
	if(os.name <>'posix'):
		print 'Error: Only allowed to run in UNIX systems.'
		sys.exit(0)

	#check folders
	folders = ['targets','profiles']
	for i in folders:
		if(os.path.isdir(i)):
			print ' [+] Folder ' + str(i) + ' found.'
		else:
			print ' [!] Folder ' + str(i) + ' not found. Creating...'
			os.mkdir(i)



	db = Database('KANAI.DB')
	db.start()
	
	while 1:
		if(Program.clean_screen()):
			print Program.banner
			u_input = raw_input('\n Console:\n >>')
			u_input = str(u_input).upper()
			Program.command(u_input)
			de = raw_input('')

def main():
	init()



if __name__ == '__main__':
	main()