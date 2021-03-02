from setuptools import setup, find_packages

requirements = [
    'earthengine-api',
    'intake-stac',
    'jupyter',
    'folium',
    'geopandas',
    'rasterio',
    'geoviews',
    'scipy',
    'msgpack',
    'toolz',
    'intake-geopandas',
]

setup_requirements = [
    'setuptools_scm',
    'pytest-runner',
]

test_requirements = [
    'pytest-cov',
]

extras = {
    'test': test_requirements,
}

packages = find_packages(include=['gee_processing'])

package_dir = {}

package_data = {}

setup(
    name='gee-processing',
    use_scm_version=True,
    author="Matthieu Bernard",
    author_email='matth.bernard@gmail.com',
    description="Dummy Python library.",
    url='https://gitlab.meteoswiss.ch/ber/gee-processing',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD-3-Clause License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.8',
    ],
    keywords='gee_processing',
    entry_points={
        'intake.catalogs': [
            'gee = gee_processing:cat',
        ]
    },
    scripts=[],
    license="BSD-3-Clause license",
    long_description=open('README.md').read() + '\n\n' +
    open('HISTORY.rst').read(),
    include_package_data=True,
    zip_safe=False,
    test_suite='test',
    py_modules=['gee-processing'],
    packages=packages,
    install_requires=requirements,
    package_dir=package_dir,
    package_data=package_data,
    setup_requires=setup_requirements,
    tests_require=test_requirements,
    extras_require=extras,
)
