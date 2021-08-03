# Peat depth survey uploader

# NOTE: This has now been folded into [pa_restoration_data_model](https://github.com/Scottish-Natural-Heritage/pa_restoration_data_model)

Python script to upload peat depth survey data to postgres database.

## Overview

This project formats and uploads files (gpkg, shp) containing peat depth survey and condition data. It uses geopandas, sqlalchemy and geoalchemy2. An accompanying helper script `sheet_to_spatial.py` is included to convert excel files into spatial vector format.

---

## Instructions

I recommend creating a conda enviroment to run the script. Conda is an open source package management system, in short it makes the creation and management of virtual environments very easy. As a result it is particularly popular within the field of data science. While this may seem a bit of a pain to get installed, once up and running it will make things much easier in the long run. It is also the easiest way to install the open source spatial stack as a virtual environment, which means you can access libraries like geopandas.

### Installing conda

Conda comes in two forms, the full Anacdona package that comes with  or Miniconda, which only features the essentials. You should use miniconda as we will only need to install the packages we want for a given environment.

[Link to miniconda installer](https://docs.conda.io/en/latest/miniconda.html#windows-installers) - Select python3.8 and Windows 64bit version.

Download miniconda and install in your user (e.g. "C:\joe\miniconda")

Once installed, press ![Win key](http://i.stack.imgur.com/T0oPO.png "Windows key") and start typing `miniconda`, this should bring up the Anaconda prompt(miniconda) application, open it and you should be greeted with a command line interface with something like the following:

```
(base) C:\Users\CLJB3>
```

`(base)` refers to your current activate environment and the file path to your current directory. It is best practice to leave `base` solely for conda and create new environments for projects, which is what we will do next.

### Creating a new environment using environments file

First we will create a new environment called `gis_env` using the `environments.yml` file. First navigate to the repo directory using the `cd` (change directory) command:

```
cd path/to/repository
```

then enter the following:

```
conda env create -f environment.yml
```

This command will use the environments file to first create an environment then install the packages required. This process may take a while as the requirements are installed, once complete you will have your new environment loaded with the relevant spatial and database depencines. You can activate the environment using the following command:

```
conda activate gis_env
```

Notice that `gis_env` has replaced `base` in the command line:

```
(gis_env) C:\Users\CLJB3>
```

## sheet_to_spatial helper script

This is a simple script that converts excel files into shapefile or geopackage with the correct headers for the `peat_depth_uploader.py` script.

Ensure you are in correct directory and have activate `gis_env` then run as below:

```
python sheet_to_spatial.py path/to/excel.xlsx path/to/shapefile.shp
```

Note that at present it assumes the following to be true

* Top two rows of sheet are ignored to skip whitespace and verbose field names
* Ordering of columns is unchanged - this is important as it renames using column index
* Data is on sheet 3 of xlsx file - this is to read correct sheet as dataframe

## Running peat_depth_uploader

There are a few things you will need to do before you can use the script to upload peat depth.

* Create a `config.py` file - this must be in the same directory as the python postgis_write.py and should take the following format:

```
host = "localhost"
port = 5432
database = "peatland_action"
user = "user_name"
password = "password"
```

* Ensure you have an active tunnel client running to enable connection to the database

Once these are resolved, you can run the script in the following way:

```
python peath_depth_uploader.py path/to/file.shp PDS123 globalid
```

This will then upload the file to the postgres database.

If an error occours it should be explained within the output, if you want information about the commands needed you can do using

```
python peat_depth_uploder.py -h
```
