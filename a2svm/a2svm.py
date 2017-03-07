#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ressources
import sys
import ConfigParser
import string
import random
import datetime
import subprocess
import re
from appdirs import *
from argparse import ArgumentParser
from string import Template

class a2vhost(object):
	def __init__(self):
		self.name = ""
		self.macro = ""
		self.enabled = "no"
		self.servername = ""
		self.directory = ""
		self.alias = ""


def query_yes_no(question, default="yes"):
	valid = {"yes":True,   "y":True,  "ye":True,
		"no":False,     "n":False}
	if default == None:
		prompt = " [y/n] "
	elif default == "yes":
		prompt = " [Y/n] "
	elif default == "no":
		prompt = " [y/N] "
	else:
		raise ValueError("invalid default answer: '%s'" % default)
	while 1:
		sys.stdout.write(question + prompt)
		choice = raw_input().lower()
		if default is not None and choice == '':
			return valid[default]
		elif choice in valid.keys():
			return valid[choice]
		else:
			sys.stdout.write("Please respond with 'yes' or 'no' "\
				"(or 'y' or 'n').\n")


class a2svm(object):
	appname = "a2svm"
	appauthor = ressources.__author__

	def __init__(self):
		self.name = "default"
		self.macro_path = "/etc/apache2/conf-enabled/"
		self.macro_file_filter = "macro_vhost*"
		self.vhost_config_path = "/etc/apache2/sites-available"
		self.vhost_enabled_path = "/etc/apache2/sites-enabled"
		self.vhost_enabling_command = "/usr/sbin/a2ensite"
		self.vhost_disabling_command = "/usr/sbin/a2dissite"
		self.apache_reload_command = "/etc/init.d/apache2 reload"
		self.certbot_path = "/usr/bin/certbot"
		self.certbot_mail = "root@host.local"
		self.config = ConfigParser.ConfigParser()
		self.config_file= os.path.join(user_data_dir(self.appname, self.appauthor), 'a2svm.cfg')
		self.config.read(self.config_file)

	def config_remove(self, config_id):
			remove_config=query_yes_no("Are you sure you want to remove config?")
			if (remove_config):
				self.config.remove_section(config_id)
				with open(self.config_file, 'wb') as configfile:
					self.config.write(configfile)
					print '\nConfiguration file has been update: '+os.path.abspath(self.config_file)


	def load(self, config_id):
		if (self.config.has_section(config_id)):
			try:
				self.macro_path=self.config.get(config_id, 'macro_path', 0)
				self.macro_file_filter=self.config.get(config_id, 'macro_file_filter', 0)
				self.vhost_config_path=self.config.get(config_id, 'vhost_config_path', 0)
				self.vhost_enabled_path=self.config.get(config_id, 'vhost_enabled_path', 0)
				self.vhost_enabling_command=self.config.get(config_id, 'vhost_enabling_command', 0)
				self.vhost_disabling_command=self.config.get(config_id, 'vhost_disabling_command', 0)
				self.apache_reload_command=self.config.get(config_id, 'apache_reload_command', 0)
				self.certbot_path=self.config.get(config_id, 'certbot_path', 0)
				self.certbot_mail=self.config.get(config_id, 'certbot_mail', 0)
			except ConfigParser.NoOptionError:
				print 'Invalid or outdated config'
				remove_config=query_yes_no("Do you want to remove invalid config")
				if (remove_config):
					self.config_remove(config_id)
				sys.exit(1)
		else:
			print "Please provide informations about your Apache configuration: ".center(50, "+")
			input_macro_path = raw_input("Macro folder path ("+self.macro_path+")> ")
			input_macro_file_filter = raw_input("Macro file filter ("+self.macro_file_filter+")> ")
			input_vhost_config_path = raw_input("Vhosts file path ("+self.vhost_config_path+")> ")
			input_vhost_enabled_path = raw_input("Vhosts enabled path ("+self.vhost_enabled_path+")> ")
			input_vhost_enabling_command = raw_input("Vhosts enabling command ("+self.vhost_enabling_command+")> ")
			input_vhost_disabling_command = raw_input("Vhosts disabling command ("+self.vhost_disabling_command+")> ")
			input_apache_reload_command = raw_input("Apache reload command ("+self.apache_reload_command+")> ")
			input_certbot_path = raw_input("Certbot path ("+self.certbot_path+")> ")
			input_certbot_mail = raw_input("Certbot mail ("+self.certbot_mail+")> ")
			save_config=query_yes_no("Do you want to save configuration?")
			if (save_config):
				self.config.add_section(config_id)
				self.config.set(config_id, 'name', self.name)
				if input_macro_path:
					self.config.set(config_id, 'macro_path', input_macro_path)
				else:
					self.config.set(config_id, 'macro_path', self.macro_path)
				if input_macro_file_filter:
					self.config.set(config_id, 'macro_file_filter', int(input_macro_file_filter))
				else:
					self.config.set(config_id, 'macro_file_filter', self.macro_file_filter)
				if input_vhost_config_path:
					self.config.set(config_id, 'vhost_config_path', input_vhost_config_path)
				else:
					self.config.set(config_id, 'vhost_config_path', self.vhost_config_path)
				if input_vhost_enabled_path:
					self.config.set(config_id, 'vhost_enabled_path', input_vhost_enabled_path)
				else:
					self.config.set(config_id, 'vhost_enabled_path', self.vhost_enabled_path)
				if input_vhost_enabling_command:
					self.config.set(config_id, 'vhost_enabling_command', input_vhost_enabling_command)
				else:
					self.config.set(config_id, 'vhost_enabling_command', self.vhost_enabling_command)
				if input_vhost_disabling_command:
					self.config.set(config_id, 'vhost_disabling_command', input_vhost_disabling_command)
				else:
					self.config.set(config_id, 'vhost_disabling_command', self.vhost_disabling_command)
				if input_apache_reload_command:
					self.config.set(config_id, 'apache_reload_command', input_apache_reload_command)
				else:
					self.config.set(config_id, 'apache_reload_command', self.apache_reload_command)
				if input_certbot_path:
					self.config.set(config_id, 'certbot_path', input_certbot_path)
				else:
					self.config.set(config_id, 'apache_certbot_path', self.certbot_path)
				if not os.path.exists(os.path.dirname(self.config_file)):
					os.makedirs(os.path.dirname(self.config_file))
				with open(self.config_file, 'wb') as configfile:
					self.config.write(configfile)
					print '\nConfiguration file has been saved to: '+os.path.abspath(self.config_file)

	def list(self):
		filelist=os.listdir(self.vhost_config_path)
		vhost_list = []
		for file in filelist:
			vhost=self.get_vhost_parameter(file)
			if (vhost):
				vhost_list.append(vhost)
		print "-"*119
		print '| {0:20}| {1:20}| {2:8}| {3:30}| {4:30}|'.format("Name", "Macro", "Enabled", "ServerName", "Directory")
		print "-"*119
		#print "-"*171
		#print '| {0:20}| {1:20}| {2:8}| {3:30}| {4:30}| {5:50}|'.format("Name", "Macro", "Enabled", "ServerName", "Directory", "Alias")
		#print "-"*171
		vhost_list.sort(key=lambda x: x.name)
		for vhost in vhost_list:
				print '| {0:20}| {1:20}| {2:8}| {3:30}| {4:30}|'.format(vhost.name[:20], vhost.macro[:20], vhost.enabled[:8], vhost.servername[:30], vhost.directory[:30])
		print "-"*119
		#	print '| {0:20}| {1:20}| {2:8}| {3:30}| {4:30}| {5:50}|'.format(vhost.name[:20], vhost.macro[:20], vhost.enabled[:8], vhost.servername[:30], vhost.directory[:30], vhost.alias[:50])
		#print "-"*171

	def get_vhost_parameter(self,file_name):
		expr = re.compile('(^\s*use) ([.\-\_a-zA-Z0-9_]+) ([.\-\_a-zA-Z0-9_]+) ([.\/\-\_a-zA-Z0-9_]+) ([.\/\-\_a-zA-Z0-9_]+) ([.\/\-\_\ "a-zA-Z0-9_]+)')
		filepath=os.path.join(self.vhost_config_path, file_name)
		with open(filepath, "r") as f:
			content = f.read()
			match = expr.match(content)
			if match != None:
					vhost=a2vhost()
					vhost.macro=match.group(2)
					vhost.name=match.group(3)
					enabled_path=os.path.join(self.vhost_enabled_path, file_name)
					if os.path.isfile(enabled_path):
						vhost.enabled="yes"
					vhost.servername = match.group(4)
					vhost.directory = match.group(5)
					vhost.alias = match.group(6)
					return vhost

	def make(self, vhost, opt_args):
		# check if macro file exist
		if os.path.isfile(os.path.join(self.macro_path, vhost.macro + ".conf")): pass
		else:
			print "Error, macro file not found, are you sure "+os.path.join(self.macro_path, vhost.macro + ".conf")+" exist?"
   			sys.exit(1)
		vhost_file = os.path.join(self.vhost_config_path, vhost.name + ".conf")
		macro_parameters = self.get_macro_parameter(vhost, "#a2svm_make_command:")
		opt_args_content = ""
		print "The vhost will be created using the macro named '"+vhost.macro+"' with the following arguments:"
		print " -Name: "+vhost.name
		print " -ServerName: "+vhost.servername
		print " -Directory: "+vhost.directory
		for arg in opt_args:
			 print "  *optional argument: \""+arg+"\""
			 opt_args_content = opt_args_content+" \""+arg+"\""
		print "The following command will be executed"
		print " "+'\n '.join(str(parameter) for parameter in macro_parameters)
		confirm=query_yes_no("Are you sure?")
		if not (confirm):
			sys.exit(1)
		# check number of argument required by macro
		macro_arg_number=self.count_macro_parameter(vhost.macro)
		if (len(opt_args) + 3) != (macro_arg_number):
			print "Error, this macro require "+str(macro_arg_number)+" arguments but "+str(len(opt_args) + 3)+" founds"
			sys.exit(1)
		# check vhosts if name or servername already exist
		filelist=os.listdir(self.vhost_config_path)
		for file in filelist:
			existing_vhost=self.get_vhost_parameter(file)
			if (existing_vhost):
				if existing_vhost.name == vhost.name:
					print "Error, name already exist"
					sys.exit(1)
				if existing_vhost.servername == vhost.servername:
					print "Error, servername already exist"
					sys.exit(1)
		# create vhost
		for parameter in macro_parameters:
			self.run_command(parameter," ","run:" + parameter)
		vhost_content = "use "+vhost.macro+" "+vhost.name+" "+vhost.servername+" "+vhost.directory+opt_args_content
		if not os.path.exists(os.path.dirname(vhost_file)):
			os.makedirs(os.path.dirname(vhost_file))
		with open(vhost_file, 'wb') as dest_file:
			dest_file.write(vhost_content)
		self.run_command(self.vhost_enabling_command, vhost.name, "Vhost enabled")
		self.run_command(self.apache_reload_command, " ", "Apache reloaded")

	def remove(self, vhost_name):
		vhost_file = os.path.join(self.vhost_config_path, vhost_name + ".conf")
		vhost=self.get_vhost_parameter(vhost_name + ".conf")
		macro_parameters = self.get_macro_parameter(vhost, "#a2svm_remove_command:")
		print "The vhost will be deleted"
		print " -Name: "+vhost.name
		print " -Macro: "+vhost.macro
		print " -ServerName: "+vhost.servername
		print " -Directory: "+vhost.directory
		print "The following command will be executed"
		print " "+'\n '.join(str(parameter) for parameter in macro_parameters)
		confirm=query_yes_no("Are you sure?")
		if not (confirm):
			sys.exit(1)
		self.run_command(self.vhost_disabling_command, vhost_name, "Vhost disabled")
		self.run_command(self.apache_reload_command, " ", "Apache reloaded")
		try:
			os.remove(vhost_file)
		except OSError:
			time.sleep(0.1)
			os.remove(vhost_file)
		for parameter in macro_parameters:
			self.run_command(parameter," ","run:" + parameter)

	def run_command(self,command, args, comment):
		try:
			retcode = subprocess.call(command + " " + args, shell=True)
			if retcode < 0:
				print >>sys.stderr, "Child was terminated by signal", -retcode
			else:
				print >>sys.stderr, comment
		except OSError as e:
			print >>sys.stderr, "Execution failed:", e
			sys.exit(1)

	def get_macro_parameter(self, vhost, parameter):
		macro_file = os.path.join(self.macro_path, vhost.macro + ".conf")
		expr = re.compile('(^'+parameter+') ([.\/\ \:\$\-\+\_a-zA-Z0-9_]+)')
		subdict = dict(servername=vhost.servername ,directory=vhost.directory ,name=vhost.name , macro=vhost.macro)
		parameters_list = []
		with open(macro_file, 'r') as macro_content:
			for line in macro_content:
				match = expr.match(line)
				if match != None:
					result = Template(match.group(2)).substitute(subdict)
					parameters_list.append(result)
		return parameters_list

	def count_macro_parameter(self, macro):
		macro_file = os.path.join(self.macro_path, macro + ".conf")
		expr = re.compile('(^<Macro '+macro+') ([.\/\ \:\$\-\+\_a-zA-Z0-9_]+)')
		with open(macro_file, 'r') as macro_content:
			for line in macro_content:
				match = expr.match(line)
				if match != None:
					line=line.lower()
					line=line.replace("<macro","")
					line=line.replace(">","")
					count = re.findall(" ", line)
					return len(count)-1
		return 0

	def gen_cert(self, vhost_name):
		vhost = self.get_vhost_parameter(vhost_name + ".conf")
		self.run_command(self.certbot_path, "certonly --noninteractive --agree-tos --email " + self.certbot_mail + " --webroot --expand -w /var/www/vhosts/" + vhost.directory + "/html/ -d " + vhost.servername , "Certificate update requested")

def launcher():
	parser = ArgumentParser(description=ressources.__description__,prog=ressources.__app_name__)

	parser.add_argument("-v", "--version",  action="version",   version="%(prog)s : "+ressources.__version__ ,help="Show program version.")

	subparsers = parser.add_subparsers(help='Avalaible commands')

	session=a2svm()
	session.load('Server1')

	parser_mk = subparsers.add_parser('mk',description='Create a vhost', help='Create a vhost')
	parser_mk.add_argument('mk_vhost_name', metavar='<vhost_name>', type=str, help='Name of the vhost')
	parser_mk.add_argument('mk_vhost_macro', metavar='<vhost_macro>', type=str, help='Macro used by the vhost')
	parser_mk.add_argument('mk_vhost_servername', metavar='<vhost_servername>', type=str, help='ServerName of the vhost')
	parser_mk.add_argument('mk_vhost_directory', metavar='<vhost_directory>', type=str, help='Directory of the vhost')
	parser_mk.add_argument('mk_opt_args', metavar='[optionnal_macro_arg]', nargs='*', type=str, help='Optionnal macro argument')


	parser_ls = subparsers.add_parser('ls', description='Show vhost on Apache server', help='Show vhost on Apache server')
	parser_ls.add_argument('ls_vhost_pattern', metavar='<search_pattern>', type=str, nargs='?', default='%', help='Show only vhost name matching pattern')

	parser_rm = subparsers.add_parser('rm',description='Delete a vhost', help='Delete a vhost')
	parser_rm.add_argument('rm_vhost_name', type=str, help='Name of the deleted vhost')

	parser_en = subparsers.add_parser('en',description='Enable a vhost', help='Enable a vhost')
	parser_en.add_argument('en_vhost_name', type=str, help='Name of the enabled vhost')

	parser_ds = subparsers.add_parser('ds',description='Disable a vhost', help='Disable a vhost')
	parser_ds.add_argument('ds_vhost_name', type=str, help='Name of the disabled vhost')

	parser_tls = subparsers.add_parser('tls',description='Request Let\'s Encrypt certificate for a vhost', help='Request certificate for a vhost')
	parser_tls.add_argument('-a', '--all', action='store_true', dest='tls_all', help='Request certificate for all enabled vhosts')
	parser_tls.add_argument('tls_vhost_name', metavar='<vhost_name>', nargs='?', default='', help='Name of the vhost')

	args = parser.parse_args()

	if hasattr(args,'mk_vhost_name'):
		vhost = a2vhost()
		vhost.name = args.mk_vhost_name
		vhost.macro = args.mk_vhost_macro
		vhost.servername = args.mk_vhost_servername
		vhost.directory = args.mk_vhost_directory
		session.make(vhost,args.mk_opt_args)
		sys.exit(1)

	if hasattr(args,'ls_vhost_pattern'):
		session.list()
		sys.exit(1)

	if hasattr(args,'rm_vhost_name'):
		session.remove(args.rm_vhost_name)
		sys.exit(1)

	if hasattr(args,'en_vhost_name'):
		session.run_command(session.vhost_enabling_command, args.en_vhost_name, "Vhost enabled")
		session.run_command(session.apache_reload_command, " ", "Apache reloaded")
		sys.exit(1)

	if hasattr(args,'ds_vhost_name'):
		session.run_command(session.vhost_disabling_command, args.ds_vhost_name, "Vhost disabled")
		session.run_command(session.apache_reload_command, " ", "Apache reloaded")
		sys.exit(1)

	if hasattr(args,'tls_all'):
		if args.tls_all:
			filelist=os.listdir(session.vhost_config_path)
			vhost_list = []
			for file in filelist:
				vhost=session.get_vhost_parameter(file)
				if (vhost):
					vhost_list.append(vhost)
			for vhost in vhost_list:
				if vhost.enabled == "yes":
					session.gen_cert(vhost.name)
			sys.exit(1)

	if hasattr(args,'tls_vhost_name'):
		if not args.tls_all and args.tls_vhost_name != '':
			session.gen_cert(args.tls_vhost_name)
			sys.exit(1)
		else:
			parser_tls.print_help()
			sys.exit(1)



if __name__ == "__main__":
    launcher()
