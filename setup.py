from setuptools import setup

setup(
        name='hexi',
        version='0.1',
        packages=['hexi/core', 'hexi/core/intent', 'hexi/interfaces/motor', 'hexi/speech'],
        package_data={'assets': ['audio/*.mp3', 'face/*.png', 'face/*.gif']}
)

