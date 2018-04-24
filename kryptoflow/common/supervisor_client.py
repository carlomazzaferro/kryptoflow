import supervisor.xmlrpc
from xmlrpc import client

p = client.ServerProxy('localhost',
                          transport=supervisor.xmlrpc.SupervisorTransport(
                              None, None,
                              'unix:///home/carlo/lib/supervisor/tmp/supervisor.sock'))

if __name__ == '__main__':
    print(p.supervisor.getState())