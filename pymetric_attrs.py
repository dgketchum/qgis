# ===============================================================================
# Copyright 2018 dgketchum
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ===============================================================================

import os
from copy import deepcopy

from fiona import collection
from fiona import open as fopen
from numpy import nan
from pandas import read_csv, concat


def attribute_shapefile(shp, *results):
    df = None

    out = shp.replace('.shp', '_pym.shp')

    agri_schema = {'geometry': 'Polygon',
                   'properties': {
                       'OBJECTID': 'int',
                       'Supply': 'str',
                       'Acres': 'float',
                       'System': 'str',
                       'Crop': 'str'}}

    first = True

    for r in results:
        year = int(r[-8:-4])
        c = read_csv(r)
        c['MONTH'][c['MONTH'] < 4] = nan
        c['MONTH'][c['MONTH'] > 10] = nan
        c.dropna(axis=0, how='any', inplace=True)

        c = c.groupby('OBJECTID').agg({'NDVI': 'mean',
                                       'ETRF': 'mean',
                                       'ETR_MM': 'sum',
                                       'ET_MM': 'sum',
                                       'PPT_MM': 'sum'}).reset_index()

        renames = {'NDVI': 'NDVI_mean_{}'.format(year),
                   'ETRF': 'ETRF_mean_{}'.format(year),
                   'ETR_MM': 'ETR_mm_{}'.format(year),
                   'ET_MM': 'ET_mm_{}'.format(year),
                   'PPT_MM': 'PPT_mm_{}'.format(year)}

        c.rename(columns=renames, inplace=True)

        if first:
            df = deepcopy(c)
            first = False
        else:
            concat([df, c], join='outer')

        schema_dict = {'NDVI_mean_{}'.format(year): 'float',
                       'ETRF_mean_{}'.format(year): 'float',
                       'ETR_mm_{}'.format(year): 'float',
                       'ET_mm_{}'.format(year): 'float',
                       'PPT_mm_{}'.format(year): 'float'}

        agri_schema['properties'].update(schema_dict)


    with fopen(shp, 'r') as src:
        src_crs = src.crs
        src_driver = src.driver

        with collection(out, mode='w', driver=src_driver,
                        schema=agri_schema, crs=src_crs) as output:
            for rec in src:
                props = {'OBJECTID': rec['properties']['OBJECTID'],
                          'Supply': rec['properties']['Supply_Sou'],
                          'Acres': rec['properties']['Acres'],
                          'System': rec['properties']['System_Typ'],
                          'Crop': rec['properties']['Crop_Type']}
                props.update(df[df['OBJECTID'] == rec['properties']['OBJECTID']].to_dict('records')[0])

                output.write({'geometry': rec['geometry'],
                              'properties': props})


if __name__ == '__main__':
    home = os.path.expanduser('~')
lolo = os.path.join(home, 'IrrigationGIS', 'lolo')
s = os.path.join(lolo, 'lolo_vector', 'Lolo_Project_Irrigation.shp')
r = os.path.join(lolo, 'ET', 'LINEAR_ZONES', 'monthly_zonal_stats_2016.csv')
attribute_shapefile(s, r)
# ========================= EOF ====================================================================
