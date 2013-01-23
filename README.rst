**********************************************
a2svm  - Apache 2 Simple Virtualhost Manager  
**********************************************

**a2svm** is a Simple CLI tool to create and delete easily virtualhosts in Apache.

usage: a2svm [-h] [-v] {mk,ls,rm,en,ds} ...


a2svm commands are:

* **mk**         Create a virtualhosts
* **ls**         Show managed virtualhosts on Apache server
* **rm**         Delete a virtualhosts
* **en**         Enable a virtualhosts
* **ds**         Disable a virtualhosts

See 'a2svm <command> -h' for more information on a specific command.

PyPI package `<http://pypi.python.org/pypi/a2svm>`__ 

Sources `<https://github.com/cypx/a2svm>`__ 
 
Requirements
##############

a2svm need apache mod_macro which could be installed on debian 6 by the following command

.. code-block:: bash

	$ aptitude install libapache2-mod-macro

Once mod_macro is avalaible some template could be created for use by a2svm like this one

.. code-block:: 

	<Macro vhost_standard $name $servername $directory>
	  <VirtualHost *:80>

	    ServerName $servername

	    DocumentRoot /var/www/$directory/public

	    <Directory /var/www/$directory>
	        Options  FollowSymLinks MultiViews
	        AllowOverride All
	        Order allow,deny
	        allow from all
	    </Directory>

	    ErrorLog /var/www/$directory/log/error.log

	    # Possible values include: debug, info, notice, warn, error, crit,
	    # alert, emerg.
	    LogLevel warn

	    CustomLog /var/www/$directory/log/access.log combined
	  </VirtualHost>
	</Macro>

	#Comments beginning by "a2svm_make_command" are used to run external commands before vhost is created 
	#a2svm_make_command: /bin/mkdir -p /var/www/$directory/public /var/www/$directory/log
	#a2svm_make_command: /bin/chown -R cyp:www-data /var/www/$directory
	#Comments beginning by "a2svm_remove_command" are used to run external commands after vhost is removed 
	#a2svm_remove_command: /bin/tar czf /var/www/archive/$servername.tgz /var/www/$directory
	#a2svm_remove_command: /bin/rm -rf /var/www/$directory

	

Installation
##############

Install it easily:

Using pip
**************

.. code-block:: bash

	$ pip install a2svm

Using easy_install
*********************

On most Linux distribution 

.. code-block:: bash

	$ easy_install a2svm

But on some, prerequisites are required, for example, on Debian 6

.. code-block:: bash

	$ aptitude install python-pip



