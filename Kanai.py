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
		c.execute("INSERT INTO TARGETS (id,target_name,time) VALUES (NULL," + "'" + str(self.name) + "'" + ',' + "'" + str(self.timestamp) + "'" + ")" )
		print ' [+] SQLITE3: Added ' + str(self.name) + ' to targets table.'
		c.execute('CREATE TABLE PROFILE_' + str(self.name) + ' (ID INTEGER PRIMARY KEY,NAME,COMMAND,TIMESTAMP)')
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

	class Profile:
		"""This class is responsible for managing profiles operations."""
		def __init__(self, owner, name, command, timestamp):
			super(Profile, self).__init__()
			self.owner = owner
			self.name = name
			self.command = command
			self.timestamp = timestamp
			print self.name, self.command, self.timestamp

		@classmethod
		def add(self, owner, name, command, timestamp):
			self.owner = owner
			self.name = name
			self.command = command
			self.timestamp = timestamp
			c.execute("INSERT INTO PROFILE_" + str(owner) + " VALUES (NULL," + "'" + str(name) + "','" + str(command) + "','" + str(timestamp) + "')")
			print ' [+] Added ' + str(command) + ' to profile ' + str(name) + ' of ' + str(owner) + '.'
			return True

		@classmethod
		def delete(self, owner, name):
			self.owner = owner
			self.name = name
			c.execute("DELETE FROM PROFILE_" + str(owner) + " WHERE NAME=" + "'" + str(name) + "'")
			print ' [-] Deleted ' + str(name) + ' from ' + str(owner) + '.'



		





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
				global select_target
				select_target = Target(arg_analysis[1], str(time.ctime()))
				if(select_target.select() == True):

					print ' [*] ' + str(select_target.name) + ' selected.'
				else:
					print ' [!] Could not find ' + str(select_target.name) + ' to select it.'

	def profileFunc(arguments):
		arg_analysis = arguments.split(' ')
		if(arg_analysis[0] == ''):
			if(select_target <> None):
				c = connection.cursor()
				c.execute("SELECT Count(*) FROM PROFILE_" + str(select_target.name))
				profiles = c.fetchall()
				print ' ' + select_target.name + ' has ' + str(profiles[0])[1:-2] + ' profiles.'
			else:
				print ' [!] Error: You need to select a target using TARGET SELECT <TARGETNAME>'
		if(arg_analysis[0] == 'ADD'):
			if(select_target <> None):
				#CODIGO PRA CRIAR UM PROFILE
				#AQUI VAI SER ONDE SERA GERADO O COMANDO PARA O USUARIO 
				#VOU FAZER UMA CLASSE PRA ISSO COM CADA PARAMETRO ESSENCIAL E OPCIONAL
		if(arg_analysis[0] == 'DEL'):
			if(select_target <> None):
				#CODIGO PRA DELETAR UM PROFILE
		if(arg_analysis[0] == 'RUN'):
			if(select_target <> None):
				#CODIGO PRA EXECUTAR UM PROFILE
			


	
	@staticmethod
	def command(string):
		global db
		if(string[0:len('profile')] == 'PROFILE'):
			arguments = string[len('PROFILE '):]
			profileFunc(arguments)
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
			print ' No valid command was given.'








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
	global select_target
	select_target = None
	
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