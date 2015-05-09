

from setuptools import setup, find_packages


setup(
    name='pimento',
    version='0.2.0',
    description='Simple CLI Menus',
    long_description='Python Menus.  Make an interactive menu with a default, pre- and post-prompts, partial argument matching, indexing, etc.',
    url='https://github.com/toejough/pimento',
    author='toejough',
    author_email='toejough@gmail.com',
    license='MIT',
    classifiers=[
            # How mature is this project? Common values are
            #   3 - Alpha
            #   4 - Beta
            #   5 - Production/Stable
            'Development Status :: 4 - Beta',

            # Indicate who your project is intended for
            'Intended Audience :: Developers',

            # Pick your license as you wish (should match "license" above)
             'License :: OSI Approved :: MIT License',

            # Specify the Python versions you support here. In particular, ensure
            # that you indicate whether you support Python 2, Python 3 or both.
            'Programming Language :: Python :: 2.7',
    ],
    keywords="menu cli",
    packages = find_packages(),
    install_requires = []
)
