import pandas as pd
import pydantic

from conn import conn
from sqlalchemy import create_engine, select, table, union_all, and_, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from fastapi_backend.models import UniqueTranslationsORM
from fastapi_backend.schemas import UniqueTranslationsPYD

# Declare base
Base = declarative_base()

# Create engine
engine = create_engine('sqlite://', creator=lambda: conn)

# setup the session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = SessionLocal()

# Define tables to use in the query here
compendium_ru = Base.metadata.tables['compendium_ru']
compendium_uk = Base.metadata.tables['compendium_uk']
fip_equiv = Base.metadata.tables['fip_equiv']
utis_in_ua = Base.metadata.tables['utis_in_ua']
wikidata_names = Base.metadata.tables['wikidata_names']

query = union_all(
    
    # BEGIN Translation Pairs from compendium_ru
    select([
        'ru', 'en', compendium_ru.c.title_ru_name, compendium_ru.c.title_latin_name,
        compendium_ru.c.source, compendium_ru.c.url, 2
    ]).where(and_(
        compendium_ru.c.title_ru_name.isnot(None),
        compendium_ru.c.title_latin_name.isnot(None)
    )),
    
    select([
        'en', 'ru', compendium_ru.c.title_latin_name, compendium_ru.c.title_ru_name,
        compendium_ru.c.source, compendium_ru.c.url, 2
    ]).where(and_(
        compendium_ru.c.title_ru_name.isnot(None),
        compendium_ru.c.title_latin_name.isnot(None)
    )),
    # END Transltaion pairs from compendium_ru
    
    # BEGIN Translation paris from compendium_uk
    select([
        'uk', 'en', compendium_uk.c.title_uk_name, compendium_uk.c.title_latin_name,
        compendium_uk.c.source, compendium_uk.c.url, 2
    ]).where(and_(
        compendium_uk.c.title_uk_name.isnot(None),
        compendium_uk.c.title_latin_name.isnot(None)
    )),

    select([
        'en', 'uk', compendium_uk.c.title_latin_name, compendium_uk.c.title_uk_name,
        compendium_uk.c.source, compendium_uk.c.url, 2
    ]).where(and_(
        compendium_uk.c.title_uk_name.isnot(None),
        compendium_uk.c.title_latin_name.isnot(None)
    )),
    # END Translation paris from compendium_uk

    # BEGIN Translation pairs from FIP
    select([
        'uk', 'en', fip_equiv.c.activeingredient_cy, fip_equiv.c.activeingredient,
        'FIP', fip_equiv.c.info_uk, 1
    ]).where(and_(
        fip_equiv.c.activeingredient.isnot(None), 
        fip_equiv.c.activeingredient_cy.isnot(None)
    )),

    select([
        'en', 'uk', fip_equiv.c.activeingredient, fip_equiv.c.activeingredient_cy,
        'FIP', fip_equiv.c.info_uk, 1
    ]).where(and_(
        fip_equiv.c.activeingredient.isnot(None), 
        fip_equiv.c.activeingredient_cy.isnot(None)
    )),
    
    select([
        'uk_brand_ua', 'en', fip_equiv.c.brandname_uk_cy, fip_equiv.c.activeingredient,
        'FIP', fip_equiv.c.info_uk, 1
    ]).where(and_(
        fip_equiv.c.brandname_uk_cy.isnot(None), 
        fip_equiv.c.activeingredient.isnot(None)
    )),

    select([
        'en', 'uk_brand_ua', fip_equiv.c.activeingredient, fip_equiv.c.brandname_uk_cy,
        'FIP', fip_equiv.c.info_uk, 1
    ]).where(and_(
        fip_equiv.c.brandname_uk_cy.isnot(None), 
        fip_equiv.c.activeingredient.isnot(None)
    )),

    select([
        'uk_brand_ua', 'uk', fip_equiv.c.brandname_uk_cy, fip_equiv.c.activeingredient_cy,
        'FIP', fip_equiv.c.info_uk, 1
    ]).where(and_(
        fip_equiv.c.brandname_uk_cy.isnot(None), 
        fip_equiv.c.activeingredient_cy.isnot(None)
    )),

    select([
        'uk', 'uk_brand_ua', fip_equiv.c.activeingredient_cy, fip_equiv.c.brandname_uk_cy,
        'FIP', fip_equiv.c.info_uk, 1
    ]).where(and_(
        fip_equiv.c.brandname_uk_cy.isnot(None), 
        fip_equiv.c.activeingredient_cy.isnot(None)
    )),
    
    select([
        'en_brand_ua', 'en', fip_equiv.c.brandname_uk_lat_merge, fip_equiv.c.activeingredient,
        'FIP', fip_equiv.c.info_uk, 1
    ]).where(and_(
        fip_equiv.c.activeingredient.isnot(None),
        fip_equiv.c.brandname_uk_lat_merge.isnot(None) 
    )),
    
    select([
        'en', 'en_brand_ua', fip_equiv.c.activeingredient, fip_equiv.c.brandname_uk_lat_merge,
        'FIP', fip_equiv.c.info_uk, 1
    ]).where(and_(
        fip_equiv.c.activeingredient.isnot(None),
        fip_equiv.c.brandname_uk_lat_merge.isnot(None) 
    )),

    select([
        'en_brand_ua', 'uk', fip_equiv.c.brandname_uk_lat_merge, fip_equiv.c.activeingredient_cy,
        'FIP', fip_equiv.c.info_uk, 1
    ]).where(and_(
        fip_equiv.c.activeingredient_cy.isnot(None),
        fip_equiv.c.brandname_uk_lat_merge.isnot(None) 
    )),

    select([
        'uk', 'en_brand_ua', fip_equiv.c.activeingredient_cy, fip_equiv.c.brandname_uk_lat_merge,
        'FIP', fip_equiv.c.info_uk, 1
    ]).where(and_(
        fip_equiv.c.activeingredient_cy.isnot(None),
        fip_equiv.c.brandname_uk_lat_merge.isnot(None) 
    )),
    # END Translation Pairs from FIP

    # BEGIN Translation Pairs from UTIS
    select([
        'uk', 'en', utis_in_ua.c.title, utis_in_ua.c.page_name_decoded,
        'UTIS', utis_in_ua.c.url, 3
    ]).where(and_(
        utis_in_ua.c.title.isnot(None),
        utis_in_ua.c.page_name_decoded.isnot(None),
    )),
    
    select([
        'en', 'uk', utis_in_ua.c.page_name_decoded, utis_in_ua.c.title,
        'UTIS', utis_in_ua.c.url, 3
    ]).where(and_(
        utis_in_ua.c.title.isnot(None),
        utis_in_ua.c.page_name_decoded.isnot(None),
    )),
    # END Translation paris from UTIS
    
    # BEGIN Translation pairs from Wikidata
    select([
        'uk', 'en', wikidata_names.c.label_uk, wikidata_names.c.label_en,
        'wikidata', func.concat('https://www.wikidata.org/wiki/', wikidata_names.c.id), 2 
    ]).where(and_(
        wikidata_names.c.label_uk.isnot(None),
        wikidata_names.c.label_en.isnot(None),
    )),

    select([
        'en', 'uk', wikidata_names.c.label_en, wikidata_names.c.label_uk,
        'wikidata', func.concat('https://www.wikidata.org/wiki/', wikidata_names.c.id), 2 
    ]).where(and_(
        wikidata_names.c.label_uk.isnot(None),
        wikidata_names.c.label_en.isnot(None),
    )),

    select([
        'ru', 'en', wikidata_names.c.label_ru, wikidata_names.c.label_en,
        'wikidata', func.concat('https://www.wikidata.org/wiki/', wikidata_names.c.id), 2 
    ]).where(and_(
        wikidata_names.c.label_ru.isnot(None),
        wikidata_names.c.label_en.isnot(None),
    )),

    select([
        'en', 'ru', wikidata_names.c.label_en, wikidata_names.c.label_ru,
        'wikidata', func.concat('https://www.wikidata.org/wiki/', wikidata_names.c.id), 2 
    ]).where(and_(
        wikidata_names.c.label_ru.isnot(None),
        wikidata_names.c.label_en.isnot(None),
    )),

).distinct()

#Fetch all the fancy goodness
results = session.execute(query).fetchall()

translations = []
for result in results:
    result_data = UniqueTranslationsORM(
        source_language = result[0],
        target_language = result[1],
        source_text = result[2],
        target_text = result[3],
        table_name = result[4],
        source_comment = result[5],
        weight = result[6],
    )

    translations.append(result_data)

# Convert and validate with pydantic model
pydantic_translations = [UniqueTranslationsPYD.from_orm(translation) for translation in translations]

# Convert to dataframe and remove duplicates
df = pd.DataFrame([translation.dict() for translation in pydantic_translations])
df = df.drop_duplicates()
df = df.sort_values(by=['weight'])


# Output to csv
df.to_csv("unique_translations.csv", index=False, lineterminator='\n')

#close the session
session.close()


