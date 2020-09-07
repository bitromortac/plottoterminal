import re, setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open('./plottoterminal/__init__.py', 'r') as f:
    MATCH_EXPR = "__version__[^'\"]+(['\"])([^'\"]+)"
    VERSION = re.search(MATCH_EXPR, f.read()).group(2)

# package:
# (venv) pip install pep517 setuptools wheel sdist twine
# (venv) python3 -m pep517.build --source --binary .
# upload:
# (venv) twine upload --repository testpypi dist/*
setuptools.setup(
    name="plottoterminal",
    version=VERSION,
    author="bitromortac",
    author_email="bitromortac@protonmail.com",
    description="Plotting library for the terminal.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bitromortac/plottoterminal",
    packages=setuptools.find_packages(),
    install_requires=['wheel'],
    setup_requires=['wheel'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        "console_scripts": [
            "plottoterminal = plottoterminal.main:main",
        ]
    },
)
