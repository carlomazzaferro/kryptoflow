# Installation 

Virtualenvs are always encouraged. I recommend [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/index.html) 
with python 3.6. Python 3.5 is also supported.

```bash
$ mkvirtualenv kryptoflow
$ workon kryptoflow
```

Proceed with the installation

```bash
$ pip install kryptoflow
```
 
NOTE: you may need some additional dependencies. Namely, `librdkafka`:

On mac, with [homebrew](https://brew.sh/):

```bash
$ brew install librdkafka
```
 
On linux, with apt: 

```bash
$ wget -qO - 'https://packages.confluent.io/deb/4.0/archive.key' | apt-key add - 
$ add-apt-repository "deb [arch=amd64] https://packages.confluent.io/deb/4.0 stable main" 
$ apt-get install -y librdkafka-dev librdkafka1
```

Optionally, you may need NLTK for processing tweets and reddit comments/posts. You may do so by
downloading a couple of datasets with [NLTK](https://www.nltk.org/) (which will be installed with kryptoflow):

```bash
$ python3 -c "import nltk; nltk.download('vader_lexicon'); nltk.download('punkt')"
```


### Kafka, TensorFlow, et. al.

The default installation will install vanilla tensorflow. For installing tensorflow with GPU support, 
visit the OS-specific installation guide on [tensorflow's website](https://www.tensorflow.org/install/)

Kafka's set up is pretty much dealt with automatically. If you're running Kafka locally (which is currently
the only supported way), you may need to do one more tweak:

Edit your `/etc/hosts` file by running:

```bash
sudo nano /etc/hosts
```

and adding the following line to it:

```bash
127.0.0.1  localhost kafka1
```

That's it! Head over to the [quick start](quickstart.html) to get to work.
