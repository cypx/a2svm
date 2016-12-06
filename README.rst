**********************************************
A2SVM  - Apache 2 Simple Virtualhost Manager
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

.. code-block:: xml

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

	    ErrorLog ${APACHE_LOG_DIR}/error-$name.log

	    # Possible values include: debug, info, notice, warn, error, crit,
	    # alert, emerg.
	    LogLevel warn

	    CustomLog ${APACHE_LOG_DIR}/access-$name.log combined
	  </VirtualHost>
	</Macro>

	#Comments beginning by "a2svm_make_command" are used to run external commands
	#when vhost is created
	#a2svm_make_command: /bin/mkdir -p /var/www/$directory/public /var/www/$directory/log
	#a2svm_make_command: /bin/chown -R cyp:www-data /var/www/$directory
	#Comments beginning by "a2svm_remove_command" are used to run external commands
	#when vhost is removed
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


Upgrade
##########

Using pip
**************

.. code-block:: bash

	$ pip --upgrade a2svm

Using easy_install
*********************

.. code-block:: bash

	$ easy_install --upgrade a2svm

From sources
***************

.. code-block:: bash

    $ git clone https://github.com/cypx/a2svm
    $ cd a2svm
    $ python setup.py install

Reminder
***************

To publish package on pypi

.. code-block:: bash

    $ pip install twine
		$ rm -rf dist
		$ python setup.py sdist bdist_wheel
    $ twine upload dist/*
