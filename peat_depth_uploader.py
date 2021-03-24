"""
Script to upload peat depth survey points to postgres database.
Takes any spatial file type

Todo - Improve error handling
Todo - Check for existing data to avoid duplication
"""

from config import *
from sqlalchemy import create_engine
import argparse
import geoalchemy2
import geopandas as gpd
import sys
import re

def query_yes_no(question, default="yes"):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".
    """
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError(f"invalid default answer: {default}")

    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")

def main():

    # create sqlalchemy engine to connect to db, note you will need to enter credentials in config.py
    conn_str = f"postgresql://{user}:{password}@{host}/{database}"
    engine = create_engine(conn_str, echo=False)
    connection = engine.connect()
    schema = 'test_data_model'
    table = 'peat_depth'


    field_dict = {
        'STATION_ID': 'sample_id',
        'EVENT_DATE': 'survey_date',
        'SURVEYOR': 'surveyor',
        'GPS_ACC': 'gps_accuracy',
        'DEPTH': 'peat_depth',
        'COND': 'peat_condition',
        'NOTES': 'notes',
        'geometry':'geometry'
    }


    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="Filepath of the spatial data to be imported e.g. test_file.shp")
    parser.add_argument("survey_id", help="The id of the peat depth survey - e.g. PDS1234")
    parser.add_argument("global_id", help="The global_id for the peat depth data - ensure this is already present in the database (pa_metadata.global_id table)")


    args = parser.parse_args()

    vector_file = args.filename 
    survey_id = args.survey_id 
    global_id = args.global_id


    if len(sys.argv) < 4:
        print("\nNot enough arguments, enter file path and peatdepth survey ID (e.g. PDS1235)\n")
        print("Exiting script\n")
    elif len(sys.argv) > 4:
        print(f"Note: Too many arguments entered, only {vector_file}, {survey_id} and {global_id} will be included\n")
    else:
        pass


    # regex to check peat depth survey id fits format of PDS###
    if re.match(r"pds\d{1,}", survey_id.lower()):
        pass
    else:
        print("\nInvalid peat depth survey ID, please enter in format 'PDS###'")
        print("\nExiting script")
        exit()


    # read in file as geodataframe
    gdf = gpd.read_file(vector_file)


    # Allow user prompt to check information is correct
    print("File information")
    print(f"File name: {vector_file}")
    print(f"Global ID: {global_id}")
    print(f"Number of records: {len(gdf)}")


    if query_yes_no("Is this correct?", default="yes") == False:
        print("\nExiting script")
        exit()
    else:
        pass


    # delete unecessary columns
    for col in gdf:
        if col not in field_dict:
            del gdf[col]


    # insert peat depth survey id as 
    gdf.insert(0, 'survey_id', survey_id)
    gdf.insert(0, 'global_id', global_id)
    gdf = gdf.rename(columns=field_dict)


    """
    Todo - improve error handling and check for existing table references
    Base = declarative_base()
    Base.metadata.schema = 'test_data_model'
    Session = sessionmaker(bind=engine)

    session = Session

    class PeatDepth(Base):
        __table__ = Table(table, Base.metadata, 
        autoload=True, autoload_with=engine)

    class GlobalReference(Base):
        __table__ = Table('global_reference', Base.metadata, 
        autoload=True, autoload_with=engine)
    """


    # export to database using gpd.to_postgis, note this will drop existing table and replace
    gdf.rename_geometry("geom").to_postgis(name=table, schema=schema, con=engine, if_exists='append', index=False)


    print(f"\n{len(gdf)} records successfully uploaded to {schema}.{table}")

if __name__ == "__main__":
    main()