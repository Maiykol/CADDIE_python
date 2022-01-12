from setuptools import setup

setup(
    name='caddiepy',
    version='0.2.1',
    author='Maiykol',
    author_email='michael.hartung@uni-hamburg.de',
    packages=['caddiepy', 'caddiepy.examples', 'caddiepy.file_utils', 'caddiepy.utils'],
    scripts=[],
    url='http://pypi.python.org/pypi/caddiepy/',
    license='LICENSE',
    description='The python package to the Cancer Driver Drug Interaction Explorer (CADDIE)',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    install_requires=[
        "numpy==1.21.2",
        "pandas==1.3.2",
        "requests==2.26.0",
        "scipy==1.7.1",
        "seaborn==0.11.2",
        "openpyxl==3.0.7"
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        # 'License :: OSI Approved :: BSD License',  
        # 'Operating System :: POSIX :: Linux',        
        # 'Programming Language :: Python :: 2',
        # 'Programming Language :: Python :: 2.7',
        # 'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
    ],
)