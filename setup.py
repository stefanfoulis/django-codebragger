from setuptools import setup, find_packages


setup(
    name = "django-codebragger",
    version = __import__('codebragger').__version__,
    url = 'http://github.com/stefanfoulis/django-codebragger',
    license = 'BSD',
    platforms=['OS Independent'],
    description = "Show off your opensource code.",
    long_description = open('README.rst').read(),
    author = 'Stefan Foulis',
    author_email = 'stefan@foulis.ch',
    packages=find_packages(),
    install_requires = (
        'Django>=1.3',
        'django-filer>=0.8.1',
    ),
    include_package_data=True,
    zip_safe=False,
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
    ],
    test_suite='setuptest.SetupTestSuite',
    tests_require=(
        'django-setuptest',
    ),
)
