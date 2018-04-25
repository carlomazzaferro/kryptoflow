from xmlrpc import client


class SupervisorClient(object):
    """ Supervisor client to work with remote supervisor
    """

    def __init__(self, host='localhost', port=9001):
        self.server = client.Server('http://{}:{}/RPC2'.format(host, port))

    def start(self, process):
        """ Start process
        :process: process name as String
        """
        return self.server.supervisor.startProcess(process)

    def stop(self, process):
        """ Stop process
        :process: process name as String
        """
        return self.server.supervisor.stopProcess(process)

    def status(self, process):
        """ Retrieve status process
        :process: process name as String
        """
        return self.server.supervisor.getProcessInfo(process)  # ['statename']


if __name__ == '__main__':
    sc = SupervisorClient()
    print(sc.status('gdax_stream'))