from sqlalchemy import Column, ForeignKey
from sqlalchemy.types import String, Integer
from database import Base, engine


class Master(Base):
    __tablename__ = 'master'
    id = Column(Integer, primary_key=True)
    utis_id = Column(Integer, ForeignKey('utis_in_ua.utis_id'))
    compendium_uk_id = Column(Integer, ForeignKey('compendium_uk.compendium_uk_id'))
    compendium_ru_id = Column(Integer, ForeignKey('compendium_ru.compendium_ru_id'))
    productcode = Column(String, ForeignKey('fda_product_code_classification.productcode'))
    drugbank_id = Column(String, ForeignKey('drugbank_vocabulary.drugbank_id'))
    atc_code = Column(String, ForeignKey('who_essential.atc_classification'))
    rxcui = Column(Integer, ForeignKey('drugbank_vocabulary.drugbank_id'))


class DrugbankVocabulary(Base):
    __tablename__ = 'drugbank_vocabulary'
    drugbank_id = Column(String, primary_key=True)
    common_name = Column(String)
    cas = Column(String)
    unii = Column(String)
    standard_inchi_key = Column(String)
    accession_number = Column(String)
    synonyms = Column(String)


class WhoEssential(Base):
    __tablename__ = 'who_essential'
    medicine_name = Column(String)
    eml_section = Column(String)
    formulations = Column(String)
    indication = Column(String)
    combined_with = Column(String)
    status = Column(String)
    atc_classification = Column(String, primary_key=True)
    source = Column(String)


class WikidataNames(Base):
    __tablename__ = 'wikidata_names'

    id = Column(String)
    label_uk = Column(String)
    label_ru = Column(String)
    label_fr = Column(String)
    label_en = Column(String)
    alias_list_uk = Column(String)
    alias_list_ru = Column(String)
    alias_list_fr = Column(String)
    alias_list_en = Column(String)
    chembl_id = Column(String)
    chebi_id = Column(String)
    atc_code = Column(String, primary_key=True)
    rxnorm = Column(String)
    ukwiki_sitelink = Column(String)
    frwiki_sitelink = Column(String)
    ruwiki_sitelink = Column(String)
    enwiki_sitelink = Column(String)
    tallman_name = Column(String)


class UtisINUA(Base):
    __tablename__ = 'utis_in_ua'

    utis_id = Column(Integer, primary_key=True)
    url = Column(String)
    title = Column(String)
    page_name_decoded = Column(String)


class RxTermsIng(Base):
    __tablename__ = 'rxterms_ing'

    rxcui = Column(Integer, primary_key=True)
    ingredient = Column(String)
    ing_rxcui = Column(Integer)


class FIPEquiv(Base):
    __tablename__ = 'fip_equiv'

    atc_classification = Column(String, primary_key=True)
    activeingredient = Column(String)
    activeingredient_cy = Column(String)
    brandname_uk_cy = Column(String)
    brandname_uk_lat = Column(String)
    manufacturer = Column(String)
    dosage_cy = Column(String)
    dosage = Column(String)
    info_uk = Column(String)
    brandname_uk_lat_translit = Column(String)
    brandname_uk_lat_merge = Column(String)


class FDAProductClassificationCode(Base):
    __tablename__ = 'fda_product_code_classification'

    review_panel = Column(String)
    medicalspecialty = Column(String)
    productcode = Column(String, primary_key=True)
    devicename = Column(String)
    deviceclass = Column(String)
    unclassified_reason = Column(String)
    gmpexemptflag = Column(String)
    thirdpartyflag = Column(String)
    reviewcode = Column(String)
    regulationnumber = Column(String)
    submission_type_id = Column(String)
    definition = Column(String)
    physicalstate = Column(String)
    technicalmethod = Column(String)
    targetarea = Column(String)
    implant_flag = Column(String)
    life_sustain_support_flag = Column(String)
    summarymalfunctionreporting = Column(String)


class CompendiumUK(Base):
    __tablename__ = 'compendium_uk'

    compendium_uk_id = Column(Integer, primary_key=True)
    url = Column(String)
    title = Column(String)
    source = Column(String)
    language = Column(String)
    page_name = Column(String)
    title_latin_name = Column(String)
    title_latin_name_has_ampersand = Column(String)
    title_latin_name_has_asterisk = Column(String)
    title_uk_name = Column(String)


class CompendiumRU(Base):
    __tablename__ = 'compendium_ru'

    compendium_ru_id = Column(Integer, primary_key=True)
    url = Column(String, primary_key=True)
    title = Column(String)
    source = Column(String)
    language = Column(String)
    page_name = Column(String)
    title_latin_name = Column(String)
    title_latin_name_has_ampersand = Column(String)
    title_latin_name_has_asterisk = Column(String)
    title_ru_name = Column(String)


class RxtermsTerms(Base):
    __tablename__ = 'rxterms_terms'

    rxcui = Column(String, primary_key=True)
    generic_rxcui = Column(String)
    tty = Column(String)
    full_name = Column(String)
    rxn_dose_form = Column(String)
    full_generic_name = Column(String)
    brand_name = Column(String)
    display_name = Column(String)
    route = Column(String)
    new_dose_form = Column(String)
    strength = Column(String)
    suppress_for = Column(String)
    display_name_synonym = Column(String)
    is_retired = Column(String)
    sxdg_rxcui = Column(String)
    sxdg_tty = Column(String)
    sxdg_name = Column(String)
    psn = Column(String)


# Create all tables
Base.metadata.create_all(engine)
