drop table PNF_DATA;
create table PNF_DATA(
    CONTRACT_ID varchar,
    PLAN_ID varchar,
    SEGMENT_ID varchar,
    PHARMACY_NUMBER varchar,
    PHARMACY_ZIPCODE varchar,
    PREFERRED_STATUS_RETAIL varchar,
    PREFERRED_STATUS_MAIL varchar,
    PHARMACY_RETAIL varchar,
    PHARMACY_MAIL varchar,
    IN_AREA_FLAG varchar,
    BRAND_DISPENSING_FEE_30 varchar,
    BRAND_DISPENSING_FEE_60 varchar,
    BRAND_DISPENSING_FEE_90 varchar,
    GENERIC_DISPENSING_FEE_30 varchar,
    GENERIC_DISPENSING_FEE_60 varchar,
    GENERIC_DISPENSING_FEE_90 varchar
);
.separator "|"
.import "./pnf/1.txt" PNF_DATA
.import "./pnf/2.txt" PNF_DATA
.import "./pnf/3.txt" PNF_DATA
.import "./pnf/4.txt" PNF_DATA
.import "./pnf/5.txt" PNF_DATA

