import json


def remove_duplicates_from_medprices():
    '''
    Remove duplicate drugs from the medprices list
    '''
    with open("medprices.json", "r") as medprices_file:
        medprices = json.loads(medprices_file.read())

    for drug in medprices:
        for med in medprices:
            # if duplicate and not self
            if drug["name"] == med["name"] and drug["form"] == med["form"] and\
                drug["strength"] == med["strength"] and\
                    drug["id"] != med["id"]:
                medprices.remove(med)

    print len(medprices)
    with open("medprices.json", "w") as medprices_file:
        medprices_file.write(json.dumps(medprices))


def merge_top_demand_with_brand_names():
    '''
    Merge the top demand spreadsheet with the brand name data sent
    by Nkechi
    '''
    with open("brand_names.json", "r") as brand_names_file:
        brand_names = json.loads(brand_names_file.read())

    with open("top_demand.json", "r") as top_demand_file:
        top_demand = json.loads(top_demand_file.read())['results']

    ids = [drug['id'] for drug in brand_names]
    brand_names = {drug['brand_names'].lower(): drug for drug in brand_names}
    top_demand = {drug['BRAND'].lower(): drug for drug in top_demand}

    data_for_merge = {}
    for brand_name in top_demand:
        if brand_name not in brand_names:
            data_for_merge[top_demand[brand_name][
                'BRAND']] = top_demand[brand_name]

    ids.sort()
    last_id = ids[-1]
    for drug in data_for_merge:
        brand_names[drug] = {
            "id": last_id,
            "brand_names": data_for_merge[drug]['BRAND'],
            "company_name": data_for_merge[drug]['MANUFACTURER'],
            "theraputic_class": data_for_merge[drug]['DRUG CLASS'],
            "active_ingredient": data_for_merge[drug]['GENERIC NAME']
        }

    with open("brand_names_extended.json", "w") as new_brand_names_file:
        new_brand_names_file.write(json.dumps(brand_names.values()))

    print "Brand names merged with top demand sheet length: ", len(brand_names.keys())


merge_top_demand_with_brand_names()


def add_brand_names_to_medprices():
    '''
    Add brand names to each medprice
    '''
    with open("medprices.json", "r") as medprices_file:
        medprices = json.loads(medprices_file.read())

    with open("brand_names_extended.json", "r") as brand_names_file:
        brand_names = json.loads(brand_names_file.read())

    grouped_brand_names = {}  # brand names grouped according to active_ingredient
    for med in brand_names:
        active_ingredient = med["active_ingredient"].lower()
        if active_ingredient not in grouped_brand_names:
            grouped_brand_names[active_ingredient] = []

        brand_name = med["brand_names"]
        drug = grouped_brand_names[active_ingredient]

        if brand_name not in drug:
            drug.append(brand_name)

    meds_with_brand_names = 0
    for drug in medprices:
        drug["brand_names"] = []
        for med in grouped_brand_names:
            if drug["name"].lower() == med:
                drug['brand_names'] += grouped_brand_names[med]
                meds_with_brand_names += 1

    with open("medprices_ext.json", "w") as new_medprices_file:
        new_medprices_file.write(json.dumps(medprices))
    print "Added brand names to {} meds".format(meds_with_brand_names)

add_brand_names_to_medprices()