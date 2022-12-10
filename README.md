# Asset Management
Asset Management is an application developed using Django Framework. The purpose of this app is to track corporate assets such as phones, laptops, tablets and other gears handed out to the employees.

It has mainly two components (or "app" in Django jargon) - the user management which deals with different level of users and their permissions and access. Then there's the asset management that deals with the assets and tracks their history and current state.

To run the project, clone the repository to your local machine or in the cloud. Create a Python virtual environment using conda or Pip or any of your favorite methods using the `requirements.txt` provided. Most of the pacakges mentioned here are actually deafult requirements for Django and Python and Pip. Other than that I have explicitly used only the Django REST Framework and drf-yasg for automatic API documentation.

# Quick Start
```
git clone https://github.com/farhanfuad35/asset_management/branches
cd asset_management
conda create --name repliq_asset_management python=3.10.8 --no-default-packages
conda install pip
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

However, before running migrations, you will need to configure the database by modifying the settings.py file. The environment was prepared to work with MySQL database. You may need to download additional packages for other DBMS.