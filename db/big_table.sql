create table BIG_RXCUI_TABLE as
select FORMULARY_DATA.RXCUI as MED,
       PLAN_INFO.PDP_REGION_CODE as PDP_REGION_CODE,
       PLAN_INFO.FORMULARY_ID as FORMULARY_ID
from FORMULARY_DATA join PLAN_INFO
  on substr(FORMULARY_DATA.FORMULARY_ID, 4) = PLAN_INFO.FORMULARY_ID
join BENEFICIARY_COST
  on PLAN_INFO.CONTRACT_ID = BENEFICIARY_COST.CONTRACT_ID and
     PLAN_INFO.PLAN_ID = BENEFICIARY_COST.PLAN_ID and
     cast(FORMULARY_DATA.TIER_LEVEL_VALUE as integer) =
            cast(BENEFICIARY_COST.TIER as integer)
where
  PLAN_INFO.CONTRACT_ID like 'S%' and
  (cast(BENEFICIARY_COST.COVERAGE_LEVEL as integer) = 0 or
   cast(BENEFICIARY_COST.COVERAGE_LEVEL as integer) = 1) and
  BENEFICIARY_COST.DAYS_SUPPLY = 1 and
  cast(BENEFICIARY_COST.COST_TYPE_PREF as integer) = 1;
