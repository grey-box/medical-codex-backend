from app.algorithms.search_medication_with_image import search_medication_with_image
from app.dummy_database import dummy_database

#dummy_medications = [
#    "acetaminophen", "ibuprofen", "aspirin", "amoxicillin", "azithromycin",
#    "metformin", "atorvastatin", "omeprazole", "albuterol", "lisinopril",
#    "hydrochlorothiazide", "simvastatin", "metoprolol", "losartan", "furosemide",
#    "gabapentin", "prednisone", "levothyroxine", "sertraline", "pantoprazole",
#    "citalopram", "tramadol", "clonazepam", "amlodipine", "doxycycline",
#    "loratadine", "fluoxetine", "naproxen", "tamsulosin", "clindamycin",
#    "warfarin", "cetirizine", "cyclobenzaprine", "propranolol", "bupropion",
#    "venlafaxine", "meloxicam", "diazepam", "montelukast", "rosuvastatin",
#    "duloxetine", "cephalexin", "spironolactone", "pravastatin", "buspirone",
#    "lansoprazole", "glipizide", "nifedipine", "diclofenac", "hydralazine",
#    "tizanidine", "carvedilol", "etoposide", "hydroxyzine", "esomeprazole",
#    "pioglitazone", "atenolol", "erythromycin", "finasteride", "labetalol",
#    "famotidine", "ranitidine", "oxycodone", "insulin", "haloperidol",
#    "rivaroxaban", "apixaban", "terbinafine", "nitrofurantoin", "levetiracetam",
#    "topiramate", "valacyclovir", "acyclovir", "mirtazapine", "allopurinol",
#    "aripiprazole", "methotrexate", "ondansetron", "zolpidem", "nystatin",
#    "dexamethasone", "fluticasone", "guaifenesin", "meclizine", "benzonatate",
#    "clopidogrel", "digoxin", "modafinil", "amitriptyline", "oxcarbazepine",
#    "baclofen", "quetiapine", "risperidone", "lamotrigine", "nitroglycerin",
#    "phenazopyridine", "sildenafil", "tadalafil", "donepezil", "memantine"
#]

dummy_medications = dummy_database()
results = search_medication_with_image(
    "uk",
    0.85,
    dummy_medications,
    10,
    5,
    5
)

print("-----------------------")
for result in results:
    print(str(result.distance) + " " + result.matching_name)