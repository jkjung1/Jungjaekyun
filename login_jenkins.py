import jenkins

url = 'http://12.81.225.104:8100'
username = 'testworks'
password = 'test2015!'

server = jenkins.Jenkins(url, username=username, password=password)
user = server.get_whoami()
version = server.get_version()
print('Hello %s from Jenkins %s\n\n' % (user['fullName'], version))
