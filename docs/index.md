# Refining and Merging Medprices Data with Brand Name Data
The medprices-ng app contains drug data, a list of json objects each containing 
a drug name, it's form, strength and price. Merging this data with the brand name 
data sourced from http://rxnigeria.com/en/items involves finding a point of intersection 
between the two data sets which would be the _active ingredient_ in the brand_names
data and the _name_ in the medprices data.

Before doing the latter however, the brand_names data needs to be refined. Some
of these refinements involve removing the word _"See"_ from active ingredient(which
is placed when there's spelling variations) and replacing _"plus"_ with "+" in order to
suit the medprices data as it is currently. This can be done using Google/Open Refine
and applying the operations in the file `brand_names_open_refine_operations.json`.

Once the above is done, you can replace the data in the `brand_names.json` file with
the refined data. After this, run `add_brand_names_to_medprices.py` to merge the two data sets. Ensure you 
have the files `medprices.json` and `brand_names.json` in the same directory. This script first groups brand names that
have a similar _active ingredient_ and then goes through medprices and adds the brand names to
each medication that has that active ingredient as its name. This is output to a file `medprices_ext.json`
