from kryptoflow.managers.dashboard import DashBoardManager
import click


@click.command()
@click.option('--host', '-h', help='Host on which to server', default='0.0.0.0')
@click.option('--port', '-p', help='Port on which to expose app', default=8000)
@click.option('--env', '-e', help='Environment (dev, test, or prod)', default='prod')
def dashboard(host, port, env):
    DashBoardManager.run(host, port, env)
