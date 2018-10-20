INIT_FILE = 'polyaxonfile.yml'

INIT_FILE_MODEL_TEMPLATE = """---
version: 1

kind: experiment

logging:
  level: INFO

model:
  # set you model
  
"""

INIT_SECRETS_FILE = """
reddit:
  client_id: "XXXXXXXXXX"
  client_secret: "XXXXXXXXXX"
  username: "reddit_user_name"
  password: "reddit_password"
  user_agent: "testscript by /u/reddit_user_name"

twitter:
  consumer_key: "XXXXXXXXXX"
  consumer_secret": "XXXXXXXXXX"
  access_token: "XXXXXXXXXX"
  access_secret: "XXXXXXXXXX"

gdax:
  API_key: "XXXXXXXXXX"
  API_secret: "XXXXXXXXXXXX"
  passphrase: "XXXXXXXX"
"""

TEMPLATE_PROJECT_FILES = [
    'template/.gitignore',
    'template/docker-compose.yaml',
    'template/Dockerfile',
    'template/Dockerfile.tfserving',
    'template/secrets.yaml',
    'template/model.py',
    'template/kafka/count_messages.sh',
    'template/kafka/set_topics_config.sh',
    'template/kafka/server.properties',
    'template/kafka/schemas/reddit.avsc',
    'template/kafka/schemas/twitter.avsc',
    'template/kafka/schemas/gdax.avsc',
    'template/kafka/schemas/keyschema.avsc',
    'template/kafka/logs/.gitkeep',
    'template/supervisor/supervisord.conf',
    'template/kryptoflow/gdax.py',
    'template/kryptoflow/reddit.py',
    'template/kryptoflow/twitter.py'
]

TEMPLATE_PROJECT_DIRS = [
    'kafka/logs',
    'kafka/schemas',
    'kafka/backups',
    'serialized',
    'supervisor',
    'dist/assets',
    'kryptoflow'
]
