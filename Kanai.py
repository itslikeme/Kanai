import os, sys

class Program:
	name = 'Kanai'
	version = '0.1'




def init():
	print Program.name + ' v.' + str(Program.version)


def main():
	init()



if __name__ == '__main__':
	main()