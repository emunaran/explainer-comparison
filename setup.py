from setuptools import setup, find_packages

setup(
    name='xai-compare',  # This will be the short name used for pip install
    version='0.1.0',
    author='Ran Emuna',
    author_email='emuna.ran@gmail.com',
    description='This repository aims to provide tools for comparing different explainability methods, enhancing the '
                'interpretation of machine learning models.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/emunaran/xai-compare.git',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[
        'jupyter==1.0.0',
        'lime==0.2.0.1',
        'matplotlib==3.9.1',
        'notebook==7.2.1',
        'numpy==2.0.0',
        'pandas==2.2.2',
        'scikit-learn==1.5.1',
        'scipy==1.14.0',
        'seaborn==0.13.2',
        'shap==0.46.0',
        'interpret==0.6.2',
    ],
)
