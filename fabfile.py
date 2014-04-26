from fabric.api import *

prod_server = 'eroesch@eroesch.webfactional.com'



def prod():
    env.hosts = [prod_server]
    env.remote_app_dir = '~/webapps/django/mywww'
    env.remote_apache_dir = '~/webapps/django/apache2'


def commit():
    message = raw_input("Enter a git commit message:  ")
    local("git add -A && git commit -m \"%s\"" % message)
    local("git push origin master")
    print "Changes have been pushed to remote repository..."


def collectstatic():
    require('hosts', provided_by=[prod])
    run("cd %s; python2.7 manage.py collectstatic --noinput" % env.remote_app_dir)


def restart():
    """Restart apache on the server."""
    require('hosts', provided_by=[prod])
    require('remote_apache_dir', provided_by=[prod])

    run("%s/bin/restart;" % (env.remote_apache_dir))


def deploy():
    require('hosts', provided_by=[prod])
    require('remote_app_dir', provided_by=[prod])

    # First lets commit changes to bitbucket
    commit()
    # Now lets pull the changes to the server
    run("cd %s; git pull" % env.remote_app_dir)
    # And lastly update static media files
    collectstatic()