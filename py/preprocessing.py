#!/usr/bin/env python
# coding: utf-8

import json
import os
import pandas as pd
from datetime import datetime, timedelta
import awswrangler as wr
import boto3
import io
from pyathena import connect

conn = connect(s3_staging_dir="s3://s3-data-dev-athena--cost-aws-opsnow/tbil_aws_d/",
               region_name="ap-northeast-2")

data = pd.read_sql_query('''
    select
        CompanyID          as cmpn_id,
        PayerAccountID     as payr_acc_id,
        LinkedAccountID    as lnkd_acc_id,
        ProductCode        as service_nm,
        Region             as region,
        UsageType          as usage_type,
        Operation          as operation,
        UsageDate          as use_st_dt,
        sum(UsageQuantity) as quantity,
        sum(Cost)          as cost,
        LineItemType       as charge_type
    from (
        select
            ak.CMPN_ID            as CompanyID,
            de.PAYR_ACC_ID        as PayerAccountID,
            de.LNKD_ACC_ID        as LinkedAccountID,
            case when de.SUB_PROD_NM = 'AWS Data Transfer' then 'AWSDataTransfer'
                else de.PROD_CD
            end                  as ProductCode,
            coalesce(de.RGN_CF, 'Global') as Region,
            de.USE_TYPE           as UsageType,
            de.OPRT_NM            as Operation,
            date(de.USE_ST_DT)    as UsageDate,
            de.USE_QNT            as UsageQuantity,
            de.UN_BLND_COST       as Cost,
            de.CUR_RCRD_TYPE      as LineItemType
        from
            dev_cost_aws_opsnow.tbil_aws_d de
        inner join
            dev_cost_aws_meta.company_list ak
        on
            de.LNKD_ACC_ID = ak.LNKD_ACC_ID
        where
            de.APLY_YN = 'Y'
            and de.CHRG_YEAR >= cast(YEAR(date_add('week', -3, now())) as varchar)
            and de.CHRG_MNTH >= lpad(cast(MONTH(date_add('week', -3, now())) as varchar), 2, '0')
            and de.USE_ST_DT >= date_add('week', -3, now()) )
    group by
        CompanyID,
        PayerAccountID,
        LinkedAccountID,
        ProductCode,
        Region,
        UsageType,
        Operation,
        UsageDate,
        LineItemType
        ''',
    conn)

data = data.fillna(
    value={
        'cost'        : 0,
        'charge_type' : 'N/A',
        'usage_type'  : 'N/A',
        'service_nm'  : 'N/A',
        'region'      : 'N/A',
        'operation'   : 'N/A'
    }
)

usage_data = data[data['charge_type'].isin(['Usage', 'DiscountedUsage'])]

usage_df = usage_data[['cmpn_id','use_st_dt']].drop_duplicates()

input_data = data[~data['charge_type'].isin(['Credit', 'Refund'])]

usage_data_max_date = usage_data.groupby('cmpn_id', as_index=False).agg({'use_st_dt': 'max'})

usage_merged = input_data.merge(
    usage_df,
    on=['cmpn_id', 'use_st_dt'],
    how='outer', 
    indicator=True
)

usage_include_sp_merged = usage_merged[usage_merged['_merge'] == 'both'].drop(columns=['_merge'])

max_date_merged = usage_include_sp_merged.merge(
    usage_data_max_date,
    on=['cmpn_id', 'use_st_dt'],
    how='outer', 
    indicator=True
)

usage_data_without_max_date = max_date_merged[max_date_merged['_merge'] == 'left_only'].drop(columns=['_merge'])

usage_data_without_max_date = usage_data_without_max_date[(usage_data_without_max_date.charge_type !='Credit') & 
        (usage_data_without_max_date.charge_type != 'Refund') & 
        (usage_data_without_max_date.charge_type != 'SavingsPlanCoveredUsage') & 
        (usage_data_without_max_date.charge_type != 'SavingsPlanNegation')]

usage_data_without_max_date['use_st_dt'] = pd.to_datetime(usage_data_without_max_date['use_st_dt'])

batch_date = datetime.today().strftime('%Y-%m-%d')
length = 7*2
horizon = 7
levels = [0.01,0.1,0.2]

cost_var = usage_data_without_max_date.groupby('cmpn_id', as_index=False).agg({'cost': 'var'}).rename(columns={"cost":"cost_var"}) 

zero_var = cost_var[cost_var['cost_var'] == 0]

zero_var_merged = usage_data_without_max_date.merge(
    zero_var['cmpn_id'],
    on=['cmpn_id'],
    how='outer', 
    indicator=True
)

pca_usage_data = zero_var_merged[zero_var_merged['_merge'] == 'left_only'].drop(columns=['_merge'])

zero_var_data = zero_var_merged[zero_var_merged['_merge'] == 'both'].drop(columns=['_merge'])

fcst_usage_data = usage_data_without_max_date

pca_usage_data['ProductNameCode'] = pca_usage_data['cmpn_id']+'%%%'+pca_usage_data['payr_acc_id']+'%%%'+pca_usage_data['lnkd_acc_id']+'%%%'+ pca_usage_data['service_nm']+'%%%'+pca_usage_data['region']+'%%%'+pca_usage_data['charge_type']+'%%%'+pca_usage_data['usage_type']+'%%%'+pca_usage_data['operation']

S3_BUCKET = 's3-dev-cost-anomaly--aiml'
PREFIX = 'input'
FCST_INPUT_FILENAME = 'fcst_usage_data.csv'
PCA_INPUT_FILENAME = 'pca_usage_data.csv'

url = 's3://{}/{}/{}'.format(S3_BUCKET, PREFIX, FCST_INPUT_FILENAME)
wr.s3.to_csv(fcst_usage_data, path=url, index=False)
url = 's3://{}/{}/{}'.format(S3_BUCKET, PREFIX, PCA_INPUT_FILENAME)
wr.s3.to_csv(pca_usage_data, path=url, index=False)
