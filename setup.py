from setuptools import setup

setup(
    name='kbdf',
    version='0.6.0',
    scripts=['scripts/kbdf.pyw'],
    license='MIT',
    description='Python script to translate text that was typed accidentally in wrong keyboard layout.',
    long_description=open('README.MD').read(),
    install_requires=['pyperclip', 'pyautogui'],
    url='https://github.com/alexantoshuk/kbdf',
    author='Alexander Antoshuk',
    author_email='alexander.antoshuk@gmail.com',
)
