create table BENEFICIARY_COST(
    CONTRACT_ID varchar(5),
    PLAN_ID int,
    SEGMENT_ID int,
    COVERAGE_LEVEL float,
    TIER int,
    DAYS_SUPPLY int,
    COST_TYPE_PREF float,
    COST_AMT_PREF float,
    COST_MIN_AMT_PREF float,
    COST_MAX_AMT_PREF float,
    COST_TYPE_NONPREF float,
    COST_AMT_NONPREF float,
    COST_MIN_AMT_NONPREF float,
    COST_MAX_AMT_NONPREF float,
    COST_TYPE_MAIL_PREF float,
    COST_AMT_MAIL_PREF float,
    COST_MIN_AMT_MAIL_PREF float,
    COST_MAX_AMT_MAIL_PREF float,
    COST_TYPE_MAIL_NONPREF float,
    COST_AMT_MAIL_NONPREF float,
    COST_MIN_AMT_MAIL_NONPREF float,
    COST_MAX_AMT_MAIL_NONPREF float,
    TIER_SPECIALTY_YN varchar(1),
    DED_APPLIES_YN varchar(1),
    GAP_COV_TIER int
);

create table GEOGRAPHIC_LOCATOR(
    COUNTY_CODE int(5),
    STATENAME varchar,
    COUNTY varchar,
    MA_REGION_CODE int,
    MA_REGION varchar,
    PDP_REGION_CODE int,
    PDP_REGION varchar
);

create table PLAN_INFO(
    CONTRACT_ID varchar(5),
    PLAN_ID int,
    SEGMENT_ID int,
    CONTRACT_NAME varchar,
    PLAN_NAME varchar,
    FORMULARY_ID varchar,
    PREMIUM float,
    DEDUCTIBLE float,
    IC float,
    MA_REGION_CODE int,
    PDP_REGION_CODE int,
    STATE varchar(2),
    COUNTY_CODE int,
    SNP int,
    PLAN_SUPPRESSED_YN varchar(1)
);

create table ZIP_STATE_COUNTY(
    ZIPCODE varchar,
    LATITUDE float,
    LONGITUDE float,
    CITY varchar,
    STATE varchar(2),
    STATENAME varchar,
    COUNTY varchar,
    ZIPCLASS varchar
);

create table NCPDP(
    NCPDP int,
    NPI int,
    PHARMACY_NAME varchar,
    CITY varchar,
    STATE varchar(2),
    ZIPCODE varchar,
    PHONE int
);

create table FORMULARY_DATA(
    FORMULARY_ID varchar,
    FORMULARY_VERSION int(1),
    CONTRACT_YEAR int(4),
    RXCUI int,
    NDC varchar,
    TIER_LEVEL_VALUE int,
    QUANTITY_LIMIT_YN varchar(1),
    QUANTITY_LIMIT_AMOUNT int,
    QUANTITY_LIMIT_DAYS int,
    PRIOR_AUTHORIZATION_YN varchar(1),
    STEP_THERAPY_YN varchar(1)
);

create table NDC_DATA(
    PRODUCTID varchar,
    PRODUCTNDC varchar,
    PRODUCTTYPENAME varchar,
    PROPRIETARYNAME varchar,
    PROPRIETARYNAMESUFFIX varchar,
    NONPROPRIETARYNAME varchar,
    DOSAGEFORMNAME varchar,
    ROUTENAME varchar,
    STARTMARKETINGDATE varchar,
    ENDMARKETINGDATE varchar,
    MARKETINGCATEGORYNAME varchar,
    APPLICATIONNUMBER int,
    LABELERNAME varchar,
    SUBSTANCENAME varchar,
    ACTIVE_NUMERATOR_STRENGTH float,
    ACTIVE_INGRED_UNIT varchar,
    PHARM_CLASSES varchar,
    DEASCHEDULE varchar
);

create table RXCUI_DATA(
    RXCUI varchar,
    GENERIC_RXCUI varchar,
    TTY varchar,
    FULL_NAME varchar,
    RXN_DOSE_FORM varchar,
    FULL_GENERIC_NAME varchar,
    BRAND_NAME varchar,
    DISPLAY_NAME varchar,
    ROUTE varchar,
    NEW_DOSE_FORM varchar,
    STRENGTH varchar,
    SUPPRESS_FOR varchar,
    DISPLAY_NAME_SYNONYM varchar,
    IS_RETIRED varchar,
    SXDG_RXCUI varchar,
    SXDG_TTY varchar,
    SXDG_NAME varchar,
    PSN varchar
);

.mode csv
.import '../data/2018 Beneficiary Cost file.csv' BENEFICIARY_COST
.import '../data/2018 Geographic locator file.csv' GEOGRAPHIC_LOCATOR
.import '../data/2018 Plan information.csv' PLAN_INFO
.import '../data/2018 Zip State County.csv' ZIP_STATE_COUNTY
.import '../data/FORMULARY_DATA.csv' FORMULARY_DATA
.import '../data/NDC_DRUG_FILE_LIST_UTF8.csv' NDC_DATA
.import '../data/2018NCPDPFILE_CLEAN.csv' NCPDP
.import '../data/RXCUI_DATA.csv' RXCUI_DATA
