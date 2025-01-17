import paramiko

from guietta import _, Gui, Quit
from os import getcwd

#everything in uppercase is for configuration and therefore should be changed

host = 'HOSTNAME'
port = HOSTPORT
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


def sftp_connection():
	global sftp
	sftp = ssh.open_sftp()


if(__name__ == '__main__'):
	ssh_connection()

	gui = Gui(

	  [  'Command: ', '__command__'  ,['Run'] ],
	  [  'Result: '  ,   'result'   ,    _    ],
	  [    _     ,    ['Copy']     ,   Quit   ]
	)

	with gui.Copy:
		sftp_connection()
		sftp.get(gui.command, getcwd() + '\\copy.txt')
		sftp.close()

	with gui.Run:
		command(gui.command)
		gui.result = stdout.readlines()

	gui.run()