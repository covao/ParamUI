from setuptools import setup, find_packages

setup(
    name='paramui',
    version='0.9.0',
    author='covao, Koichi Koabayshi',
    license='MIT',
    author_email='',
    url='https://github.com/covao/ParamUI'
    description='Create UI from Parameter Table',
    packages=find_packages(),
    python_requires='>=3.7',
    install_requires=[
        'numpy',
        'tkinter',
        'threading',
        'types',
        're',
   ]
)