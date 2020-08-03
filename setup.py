from setuptools import setup, find_packages

long_description = """
* Nori in Apache Lucene is a korean morpological analyzer based on Mecab.
* Pynori is a python-version of nori (Apache Lucene is written in Java).
* The analysis results are the same (All test cases are passed). 
* Pynori maybe a little slower than nori because of python script language and less optimized data structures.
* Pynori includes mecab-ko-dic-2.1.1-20180720 for system dictionary.
* Pynori is compatible with Python 3.7 and is distributed under the Apache License 2.0.
* it will probably work in various python versions.
* See, the left Homepage link, to see how to use this project.
* See, the original nori at: https://github.com/apache/lucene-solr/tree/master/lucene/analysis/nori
* See, mecab-ko-dic at: https://bitbucket.org/eunjeon/mecab-ko-dic
"""

setup(
    name='bage-pynori',
    version='0.3.3',

    url='https://github.com/bage79/python-nori',
    author='Yeongsu Kim',
    author_email='gritmind@gmail.com',

    description='Lucene Nori, Korean Mopological Analyzer, in Python',
    # long_description=open('README.md', encoding='utf-8').read(),
    long_description=long_description,
    long_description_content_type='text/markdown',

    license='Apache 2.0',

    install_requires=['cython'],
    zip_safe=False,

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[

        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',

        # Specify the Python versions you support
        'Programming Language :: Python :: 3.7',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: Apache Software License',
    ],

    # What does your project relate to?
    # keywords='',

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=find_packages(exclude=['tests']),

    # If there are data files included in your packages that need to be
    # installed, specify them here.  If using Python 2.6 or less, then these
    # have to be included in MANIFEST.in as well.
    package_data={
        '': ['pynori/resources/*'],
        '': ['pynori/config.ini']
    },
    include_package_data=True,

    # Although 'package_data' is the preferred approach, in some case you may
    # need to place data files outside of your packages. See:
    # http://docs.python.org/3.4/distutils/setupscript.html#installing-additional-files # noqa
    # In this case, 'data_file' will be installed into '<sys.prefix>/my_data'
    data_files=[],

)
