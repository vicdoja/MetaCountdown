from setuptools import setup

setup(
    # Needed to silence warnings (and to be a worthwhile package)
    name='MetaCountdown',
    url='https://github.com/vicdoja/MetaCountdown',
    author='Víctor Dorado Javier',
    author_email='thevidoja@gmail.com',
    # Needed to actually package something
    packages=['metacountdown'],
    # Needed for dependencies
    install_requires=['numpy', 'deap', 'simanneal'],
    # *strongly* suggested for sharing
    version='0.1',
    # The license can be anything you like
    license='GPL-3.0',
    description='A Python package to solve Countdown\'s number round using metaheuristics.',
    keywords='metaheuristic metaheuristic-optimisation optimization-algorithms countdown genetic-algorithm simmulated-annealing',
    # We will also need a readme eventually (there will be a warning)
    long_description=open('README.md').read(),
)