from setuptools import setup
def readme():
    with open('README.md') as f:
        return f.read()

setup(
    name = "TVFreak",
    version = 1.0,
    description = "A python application to extract links for TV Shows",
    author = "Ganesh Kumar M",
    author_email = "ganeshkumarm.1996@gmail.com",
    license = "GPLv2",
    url = "https://github.com/GaneshmKumar/TVFreak",
    packages = ["tvfreak"],
    install_requires=[
          'requests',
          'beautifulsoup4',
          'fuzzywuzzy',
          'termcolor',
          'python-Levenshtein',
      ],
    entry_points={
        'console_scripts':[
            'tvfreak = tvfreak.tvfreak:main'
            ]
        },
    long_description=readme(),
)
