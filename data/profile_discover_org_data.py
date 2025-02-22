from data.data_util import *
pd.options.mode.chained_assignment = None


def profile_discover_org_data(df):

    # remove duplicate companies
    df.drop_duplicates(inplace=True)

    # clean column headers
    df.columns = [clean_string(c) for c in df.columns]

    # available categorical columns to dummy
    impute_cols = [
        'company_primary_industry',
        'company_it_budget_mil',
        'company_fi_budget_mil',
        'company_mk_budget_mil',
        'company_ownership',
        'company_business_model_b2bb2cb2g',
        'company_technologies_excludes_hg_data_technologies',
        'company_technologies_excludes_hg_data_technologies_cont1',
        'company_technologies_excludes_hg_data_technologies_cont2',
        'advertising',
        'agency_of_record',
        'business_intelligencebig_data',
        'collaboration',
        'crm__marketing_automation',
        'data_management',
        'data_storage',
        'databases',
        'ecommerce',
        'enterprise_applications',
        'erp',
        'finance',
        'hardwareossystems_environment',
        'hr',
        'itsm',
        'languages',
        'medical',
        'mobility',
        'networking',
        'programming_tools',
        'security',
        'servers',
        'service_providers',
        'telecommunications',
        'virtualization',
        'company_record_type'
    ]

    # clean the categorical columns
    for i in impute_cols:
        try:
            df[i] = clean_categorical(df[i])
        except Exception as e:
            print(i, e)

    # put the count of times appeared in dataset as the imputation for each category
    global_map_dict = {}
    for i in impute_cols:
        map_dict = df[i].value_counts().to_dict()
        df[i] = df[i].map(map_dict)
        global_map_dict[i] = map_dict

    for i in impute_cols:

        # develop a missing column flag
        df[i + '_missing_flag'] = np.where(
            df[i].isnull(),
            1,
            0
        )

        # handle sparse categories
        df[i] = np.where(
            df[i] >= np.median(df[i]),
            df[i],
            0
        )

    # percent of missing categories across all data
    missing_flags = [c for c in df.columns if 'missing' in c]
    df['pct_missing'] = df[missing_flags].mean(axis=1)

    # years old feature
    current_year = 2020
    df['company_age'] = current_year - df['year_founded']

    # linked in flag
    df['linkedin_flag'] = np.where(
        df['company_linkedin_url'].isnull(),
        0,
        1
    )

    # drop columns that we do not need for modeling
    drop_cols = [
        'company_id',
        'company_name',
        'company_website',
        'company_hq_phone',
        'company_description',
        'company_secondary_industries',
        'my_notes_on_company',
        'company_profile_url',
        'company_linkedin_url',
        'company_other_names',
        'company_sic_codes',
        'company_naics_codes',
        'fiscal_year_end',
        'year_founded',
        'hq_address_1',
        'hq_address_2',
        'hq_city',
        'hq_state',
        'hq_postal_code',
        'hq_county',
        'hq_country',
        'hospital_beds',
        'audit',
        'technologies_searched'
    ]
    df.drop(drop_cols, axis=1, inplace=True)

    # filter out company domains with multiple hits
    df = df[df.company_email_domain.map(df.company_email_domain.value_counts()) <= 1]

    return df, global_map_dict
