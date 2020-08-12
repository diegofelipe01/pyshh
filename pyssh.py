import paramiko
import pprint
import admin

from guietta import _, Gui, Quit
from os import getcwd

#everything in uppercase is for configuration and therefore should be changed

host = 'HOST_IP'
port = 22
username = 'USERNAME'
password = 'PASSWORD'


def ssh_connection():
	global ssh
	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	ssh.connect(host, port, username, password)


def command(command):
	global stdin, stdout, stderr
	stdin, stdout, stderr = ssh.exec_command(command)


def ftp_connection():
	global ftp
	ftp = ssh.open_sftp()


if(__name__ == '__main__'):
	ssh_connection()

	gui = Gui(

	  [  'Command: ', '__command__'  ,['Run'] ],
	  [  'Result: '  ,   'result'   ,    _    ],
	  [    _     ,    ['Copy']     ,   Quit   ]
	)

	with gui.Copy:
		ftp_connection()
		ftp.get(gui.command, getcwd() + '\\copy.txt')
		ftp.close()

	with gui.Run:
		command(gui.command)
		gui.result = stdout.readlines()

	gui.run()