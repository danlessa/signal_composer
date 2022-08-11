from setuptools import setup, find_packages


setup(
    name='signal_composer',
    version='0.1',
    license='MIT',
    author="Danilo Lessa Bernardineli",
    author_email='danilo@japu.xyz',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/danlessa/signal_composer',
    keywords='signals',
    install_requires=[
          'numpy',
          'scipy'
      ],

)