## Import necessary libraries
import pandas as pd

from conn import conn

## Generate translation pairs from Compendium

translation_table = pd.read_sql_query(
    """
SELECT DISTINCT * FROM (
    -- Translation pairs from Compendium RU
SELECT 
'ru' AS source_language, 
'en' AS target_language, 
title_ru_name AS source_text, 
title_latin_name AS target_text,
source AS table_name,
url as source_comment,
2 AS weight
FROM compendium_ru C
WHERE title_ru_name IS NOT NULL AND title_latin_name IS NOT NULL

    UNION ALL
SELECT
'en' AS source_language,
'ru' AS target_language,
title_latin_name AS source_text,
title_ru_name AS target_text,
source AS table_name,
url as source_comment,
2 AS weight
FROM compendium_ru C
WHERE title_ru_name IS NOT NULL AND title_latin_name IS NOT NULL

    UNION ALL
        -- Translation pairs from Compendium UK
SELECT
'uk' AS source_language,
'en' AS target_language,
title_uk_name AS source_text,
title_latin_name AS target_text,
source AS table_name,
url as source_comment,
2 AS weight
FROM compendium_uk C
WHERE title_uk_name IS NOT NULL AND title_latin_name IS NOT NULL

    UNION ALL

SELECT
'en' AS source_language,
'uk' AS target_language,
title_latin_name AS source_text,
title_uk_name AS target_text,
source AS table_name,
url as source_comment,
2 AS weight
FROM compendium_uk C
WHERE title_uk_name IS NOT NULL AND title_latin_name IS NOT NULL

    UNION ALL
    -- Translation pairs from FIP
SELECT
'uk' AS source_language,
'en' AS target_language,
activeingredient_cy AS source_text,
activeingredient AS target_text,
'FIP' AS table_name,
info_uk AS source_comment,
1 AS weight
FROM fip_equiv F
WHERE activeingredient_cy IS NOT NULL AND activeingredient IS NOT NULL

    UNION ALL

SELECT
'en' AS source_language,
'uk' AS target_language,
activeingredient AS source_text,
activeingredient_cy AS target_text,
'FIP' AS table_name,
info_uk AS source_comment,
1 AS weight
FROM fip_equiv F
WHERE activeingredient_cy IS NOT NULL AND activeingredient IS NOT NULL

    UNION ALL
    
SELECT
'uk_brand_ua' AS source_language,
'en' AS target_language,
brandname_uk_cy AS source_text,
activeingredient AS target_text,
'FIP' AS table_name,
info_uk AS source_comment,
1 AS weight
FROM fip_equiv F
WHERE brandname_uk_cy IS NOT NULL AND activeingredient IS NOT NULL

    UNION ALL

SELECT
'en' AS source_language,
'uk_brand_ua' AS target_language,
activeingredient AS source_text,
brandname_uk_cy AS target_text,
'FIP' AS table_name,
info_uk AS source_comment,
1 AS weight
FROM fip_equiv F
WHERE brandname_uk_cy IS NOT NULL AND activeingredient IS NOT NULL

    UNION ALL

SELECT
'uk_brand_ua' AS source_language,
'uk' AS target_language,
brandname_uk_cy AS source_text,
activeingredient_cy AS target_text,
'FIP' AS table_name,
info_uk AS source_comment,
1 AS weight
FROM fip_equiv F
WHERE brandname_uk_cy IS NOT NULL AND activeingredient_cy IS NOT NULL

    UNION ALL
    
SELECT
'uk' AS source_language,
'uk_brand_ua' AS target_language,
activeingredient_cy AS source_text,
brandname_uk_cy AS target_text,
'FIP' AS table_name,
info_uk AS source_comment,
1 AS weight
FROM fip_equiv F
WHERE brandname_uk_cy IS NOT NULL AND activeingredient_cy IS NOT NULL

    UNION ALL
    
SELECT
'en_brand_ua' AS source_language,
'en' AS target_language,
brandname_uk_lat_merge AS source_text,
activeingredient AS target_text,
'FIP' AS table_name,
info_uk AS source_comment,
1 AS weight
FROM fip_equiv F
WHERE brandname_uk_lat_merge IS NOT NULL AND activeingredient IS NOT NULL

    UNION ALL
    
SELECT
'en' AS source_language,
'en_brand_ua' AS target_language,
activeingredient AS source_text,
brandname_uk_lat_merge AS target_text,
'FIP' AS table_name,
info_uk AS source_comment,
1 AS weight
FROM fip_equiv F
WHERE brandname_uk_lat_merge IS NOT NULL AND activeingredient IS NOT NULL

    UNION ALL
    
SELECT
'en_brand_ua' AS source_language,
'uk' AS target_language,
brandname_uk_lat_merge AS source_text,
activeingredient_cy AS target_text,
'FIP' AS table_name,
info_uk AS source_comment,
1 AS weight
FROM fip_equiv F
WHERE brandname_uk_lat_merge IS NOT NULL AND activeingredient_cy IS NOT NULL

    UNION ALL
    
SELECT
'uk' AS source_language,
'en_brand_ua' AS target_language,
activeingredient_cy AS source_text,
brandname_uk_lat_merge AS target_text,
'FIP' AS table_name,
info_uk AS source_comment,
1 AS weight
FROM fip_equiv F
WHERE brandname_uk_lat_merge IS NOT NULL AND activeingredient_cy IS NOT NULL

    UNION ALL
-- Translation pairs from UTIS
SELECT
'uk' AS source_language,
'en' AS target_language,
title AS source_text,
page_name_decoded AS target_text,
'UTIS' AS table_name,
url AS source_comment,
3 AS weight
FROM utis_in_ua
WHERE title IS NOT NULL AND page_name_decoded IS NOT NULL

    UNION ALL
    
SELECT
'en' AS source_language,
'uk' AS target_language,
page_name_decoded AS source_text,
title AS target_text,
'UTIS' AS table_name,
url AS source_comment,
3 AS weight
FROM utis_in_ua
WHERE title IS NOT NULL AND page_name_decoded IS NOT NULL

    UNION ALL
-- Translation pairs from Wikidata
SELECT
'uk' AS source_language,
'en' AS target_language,
label_uk AS source_text,
label_en AS target_text,
'wikidata' AS table_name,
'https://www.wikidata.org/wiki/' || id AS source_comment,
2 AS weight
FROM wikidata_names
WHERE label_uk IS NOT NULL AND label_en IS NOT NULL
    UNION ALL
SELECT
'ru' AS source_language,
'en' AS target_language,
label_ru AS source_text,
label_en AS target_text,
'wikidata' AS table_name,
'https://www.wikidata.org/wiki/' || id AS source_comment,
2 AS weight
FROM wikidata_names
WHERE label_ru IS NOT NULL AND label_en IS NOT NULL

    UNION ALL
    
SELECT
'en' AS source_language,
'uk' AS target_language,
label_en AS source_text,
label_uk AS target_text,
'wikidata' AS table_name,
'https://www.wikidata.org/wiki/' || id AS source_comment,
2 AS weight
FROM wikidata_names
WHERE label_uk IS NOT NULL AND label_en IS NOT NULL
    
    UNION ALL
    
SELECT
'en' AS source_language,
'ru' AS target_language,
label_en AS source_text,
label_ru AS target_text,
'wikidata' AS table_name,
'https://www.wikidata.org/wiki/' || id AS source_comment,
2 AS weight
FROM wikidata_names
WHERE label_ru IS NOT NULL AND label_en IS NOT NULL
)
""",
    conn,
)

## %% clean up the translation table by removing duplicates and rows with an empty of short source and target text
translation_table = translation_table.drop_duplicates().query(
    "source_text != '' and target_text != '' and source_text.str.len() >= 3 and target_text.str.len() >= 3"
)

## %% save the translation table to a CSV file
translation_table.to_csv("prepared_data/unique_translation_table.csv", index=False)
