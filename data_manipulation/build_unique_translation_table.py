## Import necessary libraries
import pandas as pd

from conn import conn

## Generate translation pairs from Compendium

translation_table = pd.read_sql_query(
    """
    -- Translation pairs from Compendium RU
SELECT DISTINCT 
'RU' AS source_language, 
'EN' AS target_language, 
title_ru_name AS source_text, 
title_latin_name AS target_text,
source AS table_name,
url as source_comment,
2 AS weight
FROM compendium_ru C
WHERE title_ru_name IS NOT NULL AND title_latin_name IS NOT NULL

    UNION ALL
SELECT DISTINCT
'EN' AS source_language,
'RU' AS target_language,
title_latin_name AS source_text,
title_ru_name AS target_text,
source AS table_name,
url as source_comment,
2 AS weight
FROM compendium_ru C
WHERE title_ru_name IS NOT NULL AND title_latin_name IS NOT NULL

    UNION ALL
        -- Translation pairs from Compendium UK
SELECT DISTINCT
'UK' AS source_language,
'EN' AS target_language,
title_uk_name AS source_text,
title_latin_name AS target_text,
source AS table_name,
url as source_comment,
2 AS weight
FROM compendium_uk C
WHERE title_uk_name IS NOT NULL AND title_latin_name IS NOT NULL

    UNION ALL

SELECT DISTINCT
'EN' AS source_language,
'UK' AS target_language,
title_latin_name AS source_text,
title_uk_name AS target_text,
source AS table_name,
url as source_comment,
2 AS weight
FROM compendium_uk C
WHERE title_uk_name IS NOT NULL AND title_latin_name IS NOT NULL

    UNION ALL
    -- Translation pairs from FIP
SELECT DISTINCT
'UK' AS source_language,
'EN' AS target_language,
activeingredient_cy AS source_text,
activeingredient AS target_text,
'FIP' AS table_name,
info_uk AS source_comment,
1 AS weight
FROM fip_equiv F
WHERE activeingredient_cy IS NOT NULL AND activeingredient IS NOT NULL

    UNION ALL

SELECT DISTINCT
'EN' AS source_language,
'UK' AS target_language,
activeingredient AS source_text,
activeingredient_cy AS target_text,
'FIP' AS table_name,
info_uk AS source_comment,
1 AS weight
FROM fip_equiv F
WHERE activeingredient_cy IS NOT NULL AND activeingredient IS NOT NULL

    UNION ALL
    
SELECT DISTINCT
'UK_BRAND_UA' AS source_language,
'EN' AS target_language,
brandname_uk_cy AS source_text,
activeingredient AS target_text,
'FIP' AS table_name,
info_uk AS source_comment,
1 AS weight
FROM fip_equiv F
WHERE brandname_uk_cy IS NOT NULL AND activeingredient IS NOT NULL

    UNION ALL

SELECT DISTINCT
'EN' AS source_language,
'UK_BRAND_UA' AS target_language,
activeingredient AS source_text,
brandname_uk_cy AS target_text,
'FIP' AS table_name,
info_uk AS source_comment,
1 AS weight
FROM fip_equiv F
WHERE brandname_uk_cy IS NOT NULL AND activeingredient IS NOT NULL

    UNION ALL

SELECT DISTINCT
'UK_BRAND_UA' AS source_language,
'UK' AS target_language,
brandname_uk_cy AS source_text,
activeingredient_cy AS target_text,
'FIP' AS table_name,
info_uk AS source_comment,
1 AS weight
FROM fip_equiv F
WHERE brandname_uk_cy IS NOT NULL AND activeingredient_cy IS NOT NULL

    UNION ALL
    
SELECT DISTINCT
'UK' AS source_language,
'UK_BRAND_UA' AS target_language,
activeingredient_cy AS source_text,
brandname_uk_cy AS target_text,
'FIP' AS table_name,
info_uk AS source_comment,
1 AS weight
FROM fip_equiv F
WHERE brandname_uk_cy IS NOT NULL AND activeingredient_cy IS NOT NULL

    UNION ALL
    
SELECT DISTINCT
'EN_BRAND_UA' AS source_language,
'EN' AS target_language,
brandname_uk_lat_merge AS source_text,
activeingredient AS target_text,
'FIP' AS table_name,
info_uk AS source_comment,
1 AS weight
FROM fip_equiv F
WHERE brandname_uk_lat_merge IS NOT NULL AND activeingredient IS NOT NULL

    UNION ALL
    
SELECT DISTINCT
'EN' AS source_language,
'EN_BRAND_UA' AS target_language,
activeingredient AS source_text,
brandname_uk_lat_merge AS target_text,
'FIP' AS table_name,
info_uk AS source_comment,
1 AS weight
FROM fip_equiv F
WHERE brandname_uk_lat_merge IS NOT NULL AND activeingredient IS NOT NULL

    UNION ALL
    
SELECT DISTINCT
'EN_BRAND_UA' AS source_language,
'UK' AS target_language,
brandname_uk_lat_merge AS source_text,
activeingredient_cy AS target_text,
'FIP' AS table_name,
info_uk AS source_comment,
1 AS weight
FROM fip_equiv F
WHERE brandname_uk_lat_merge IS NOT NULL AND activeingredient_cy IS NOT NULL

    UNION ALL
    
SELECT DISTINCT
'UK' AS source_language,
'EN_BRAND_UA' AS target_language,
activeingredient_cy AS source_text,
brandname_uk_lat_merge AS target_text,
'FIP' AS table_name,
info_uk AS source_comment,
1 AS weight
FROM fip_equiv F
WHERE brandname_uk_lat_merge IS NOT NULL AND activeingredient_cy IS NOT NULL

    UNION ALL
-- Translation pairs from UTIS
SELECT DISTINCT
'UK' AS source_language,
'EN' AS target_language,
title AS source_text,
page_name_decoded AS target_text,
'UTIS' AS table_name,
url AS source_comment,
3 AS weight
FROM utis_in_ua
WHERE title IS NOT NULL AND page_name_decoded IS NOT NULL

    UNION ALL
    
SELECT DISTINCT
'EN' AS source_language,
'UK' AS target_language,
page_name_decoded AS source_text,
title AS target_text,
'UTIS' AS table_name,
url AS source_comment,
3 AS weight
FROM utis_in_ua
WHERE title IS NOT NULL AND page_name_decoded IS NOT NULL
""",
    conn,
)
