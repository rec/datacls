_classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Topic :: Software Development :: Libraries',
    'Topic :: Utilities',
]

if __name__ == '__main__':
    from setuptools import setup
    import datacls

    with open('requirements.txt') as f:
        REQUIRED = f.read().splitlines()

    setup(
        name='datacls',
        author='Tom Ritchford',
        author_email='tom@swirly.com',
        classifiers=_classifiers,
        description='Slightly improved dataclasses',
        install_requires=REQUIRED,
        keywords=['dataclass'],
        license='MIT',
        long_description=open('README.rst').read(),
        py_modules=['datacls'],
        url='https://github.com/rec/datacls',
        version=datacls.__version__,
    )
