from setuptools import find_packages, setup

package_name = 'cv_launcher'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/cv_launcher/launch', ['launch/cv_window_launch.py']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='jonathan0209',
    maintainer_email='jonathanlim0209@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'cv_window_node = cv_launcher.cv_window_node:main',
        ],
    },
)
