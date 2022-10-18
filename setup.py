from setuptools import setup

setup(
        name='hexi',
        version='0.1',
        packages=[
            'hexi/core/intent',
            'hexi/interfaces/motor', 
            'hexi/interfaces/camera', 
            'hexi/interfaces/speaker', 
            'hexi/interfaces/display',  
            'hexi/speech', 
            'hexi/telegram', 
            'hexi/auth/', 
            'hexi/config/', 
            'hexi/features/'],
        package_data={'assets': ['audio/*.mp3', 'face/*.png', 'face/*.gif']}
)

