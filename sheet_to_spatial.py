"""
Script to convert peat depth spreadsheet data into vector layer
Accepts xlsx/csv and can output as gpkg/shp
Note that this script assumes data in standard peat depth survey template sheet:
* top two rows are ignored
* ordering of columns is unchanged
* data is on sheet 3 of xlsx file
todo: add CLI args for sheet/rows to ignore
todo: make row selection smarter - e.g. search for index of row containing correct headers to remove upto
"""
import argparse
import pandas as pd
import geopandas as gpd


def file_read(in_path, dtype_dict):
    """selects correct file reader function based on file in/file out"""
    if in_path.endswith('.xlsx'):
        return pd.read_excel(in_path, dtype=dtype_dict, skiprows=2, sheet_name=2)
    elif in_path.endswith('.csv'):
        return pd.read_csv(in_path, dtype=dtype_dict, skiprows=2)

def file_write(out_path, geoframe, schema):
    """selects correct gpd operation to write file"""
    if out_path.endswith('.gpkg'):
        return geoframe.to_file(out_path, schema=schema, driver='GPKG')
    elif out_path.endswith('.shp'):
        return geoframe.to_file(out_path, schema=schema, driver='ESRI Shapefile')


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="Filepath of the spreadsheet to be cleaned and converted into spatial file - e.g. test_file.xlsx")
    parser.add_argument("output", help="Filepath of the spatial peat depth file to be created - e.g. test_file.shp")
   
    args = parser.parse_args()

    input_file = args.input
    output_file = args.output

    dtype = {
        'EASTING': 'int64',
        'NORTHING': 'int64',
        'GRIDREF': 'string',
        'STATION_ID': 'int64',
        'EVENT_DATE': 'object',
        'SURVEYOR': 'string',
        'GPS_ACC': 'string',
        'DEPTH': 'int64',
        'COND': 'string',
        'NOTES': 'string',
    }

    schema = {
    'geometry': 'Point',
    'properties': {
        'EASTING': 'int',
        'NORTHING': 'int',
        'GRIDREF': 'str',
        'STATION_ID': 'int',
        'EVENT_DATE': 'date',
        'SURVEYOR': 'str',
        'GPS_ACC': 'str',
        'DEPTH': 'int',
        'COND': 'str',
        'NOTES': 'str',
        'DM_NOTES': 'str'
    }}


    print('Reading input spreadsheet\n')

    df = file_read(input_file, dtype)

    print(f'Spreadsheet contains {len(df)} records\n')
    print(f'writing to {output_file}\n')

    

    gdf = gpd.GeoDataFrame(
        df, geometry=gpd.points_from_xy(df.EASTING, df.NORTHING), crs='epsg:27700')

    gdf['DM_NOTES'] = ""

    file_write(output_file, gdf, schema)

    print(f'Writing of {output_file} complete, exiting script\n')

if __name__ == "__main__":
    main()