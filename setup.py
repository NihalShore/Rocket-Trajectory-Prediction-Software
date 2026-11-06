from setuptools import setup, find_packages

setup(
    name="rocket-traj",
    version="0.2.0",
    description="Multistage rocket trajectory prediction (atmosphere, drag, thrust)",
    author="Nihal",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.8",
    install_requires=[
        "numpy>=1.20",
        "matplotlib>=3.4",
        "PyYAML>=5.4",
    ],
    extras_require={
        "dev": ["pytest>=6.0"],
    },
    entry_points={
        "console_scripts": [
            "rocket-traj=rocket_traj.cli:main",
        ],
    },
    include_package_data=True,
)
