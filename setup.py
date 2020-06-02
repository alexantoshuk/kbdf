from setuptools import setup, find_packages

setup(
    name='kbdf',
    version='0.1',
    packages=find_packages(exclude=['tests*']),
    license='MIT',
    description='Python script to translate text that was typed accidentally in wrong keyboard layout.',
    long_description=open('README.MD').read(),
    install_requires=['pyperclip', 'pyautogui'],
    url='https://github.com/alexantoshuk/kbdf',
    author='Alexander Antoshuk',
    author_email='alexander.antoshuk@gmail.com'
)
