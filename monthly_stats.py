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
from pandas import read_csv, DataFrame


def organize_monthly_stats(csv_list):
    first = True
    for f in csv_list:

        df = read_csv(f)

        if first:
            mdf = DataFrame(columns=list(df.columns))
            first = False

        for m in range(4, 11):
            month = df[df['MONTH'] == m]
            try:
                s = month.loc[month['ETRF'].idxmax()]
            except TypeError:
                pass
            mdf = mdf.append(s, ignore_index=True)

    mdf = mdf[mdf['ETRF'] > 1.05]
    mdf.to_csv('/home/dgketchum/Downloads/Lolo_Irrigation_Debug_16DEC2019.csv')


if __name__ == '__main__':
    d = os.path.join(os.path.dirname(__file__), 'data', 'zonal_7JAN2020')
    files_ = [os.path.join(d, x) for x in os.listdir(d)]
    files_.sort()
    organize_monthly_stats(files_)
# ========================= EOF ====================================================================
