from setuptools import setup, find_packages

# Read the contents of your README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="app",  # Replace with your app's name
    version="1.0.0",  # Initial release version
    author="Your Name",  # Your name or organization
    author_email="your.email@example.com",  # Your email address
    description="A short description of your app",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/my_app",  # Link to your project's repository
    packages=find_packages(),  # Automatically find and include all packages
    include_package_data=True,  # Include non-code files specified in MANIFEST.in
    install_requires=[
        "gspread",
        "google-auth",
        "google-auth-oauthlib",
        "google-auth-httplib2",
        "google-api-python-client",
        "guizero",
        "pygame",
        "requests"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    entry_points={
        'console_scripts': [
            'app=app.gui.main_window:main',  # Adjusted to launch the frontend first
        ],
    },
)
