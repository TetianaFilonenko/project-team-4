from setuptools import setup, find_namespace_packages

setup(
    name="console_bot",
    version="1.3",
    description="Console bot that will help you with everything",
    url="https://github.com/TetianaFilonenko/project-team-4.git",
    author="Kobzar Coders",
    author_email="flyingcircus@example.com",
    license="MIT",
    packages=find_namespace_packages(),
    install_requires=["faker", "prompt_toolkit"],
    include_package_data=True,
    package_data={
        "console_bot": ["quotes.txt"],
    },
    entry_points={
        "console_scripts": ["run-console-bot = console_bot.console_bot:main"]
    },
)
