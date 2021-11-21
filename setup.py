from setuptools import setup, find_packages

setup(
    name="monsoonToolbox",
    version="0.0.1",
    author="Li, Mengxun",
    author_email="mengxunli@whu.edu.cn",
    description="My toolbox",

    url="https://github.com/MenxLi/toolBox", 

    packages=find_packages(),

	install_requires=['numpy>=1.19', 'scipy', 'scikit-fmm', "matplotlib"],

    entry_points = {
        "console_scripts":[
            "readPickle=monsoonToolBox.cmdCall.readPickle:main",
            "createIpynb=monsoonToolBox.cmdCall.createIpynb:main",
            "pyTrail=monsoonToolBox.cmdCall.pyTrail:main"
        ]
    }
)