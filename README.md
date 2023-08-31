# UCLA Health OHIA Data Governance Internship Project
### Hannah Chiou, June - August 2023

### Background
The UCLA Health DEV Clinical Data Mart domain contains 2600 assets of the most used data tables with each asset including a name and attributes such as description, source tags, and start and end dates. Some assets are column types, which have the attribute ‘Transformation Logic Code’ that contains the SQL code that migrates the data from the original source database. The DEV Discovery Data Repository (DDR) domain has 593 column assets, much less than the Clinical DM assets because it is meant for more public use by researchers and has filtered out columns with Protected Health Information (PHI). The DDR domain is essentially meant to be a pared down version of the Clinical DM domain. However, the DDR domain assets did not have all the exact attributes filled out. Specifically, some assets in DDR were missing the ‘Transformation Logic’ attribute. The goal of this project was to migrate the transformation logic from Clinical DM columns to the appropriate corresponding DDR column.

### Scope
The scope of this project was relatively small, encompassing two Collibra DEV domains. 

#### Requirements
1. An understanding of the Collibra architecture and how different building blocks were related to each other within the platform
2. Knowledge of REST APIs, API integration, and the [Collibra Data Governance Core APIs](https://developer.collibra.com/api/rest/data-governance#/)
3. The Python ‘requests’ package was used as the API platform

### Process
#### Solution
See code for further detail.

**1. get_asset_ids**
* This function takes a Collibra domain ID as input and creates and returns a list of dictionaries containing the lowercased name of one column asset as the key and the column asset ID as the value. The function makes use of the requests get call.

**2. get_logic**
* The function checks a list of IDs (formatted as dictionaries as specified in the get_asset_ids description) for column assets that have transformation logic. The logic was checked using the response get function. 
* This was done because out of the 2600 Clinical DM columns, only 100 actually had transformation logic. To make the program faster, it was necessary to decrease the number of Clinical DM columns that had to be checked. 
* The columns that do contain transformation logic are added to a list that contains the lowercased name of the column as the key and the transformation logic code as the value. The list is then returned.

**3. post_logic**
* The final function uses get_asset_ids and get_logic as helper functions. After obtaining the asset IDs from the Clinical DM and the DDR and the columns with transformation logic from the Clinical DM, the DDR column names are compared to the Clinical DM column names with transformation logic. 
* Note that the code does not check every DDR column to see if there is already transformation logic – it is assumed that the logic needs to be filled in for every DDR column.
* If the Clinical DM and DDR asset have the same name, then the DDR transformation logic attribute is filled in with the transformation logic from the Clinical DM using the requests post function. 

#### Solution Assumptions
1. Generally, the code assumes a user is familiar with the [Collibra platform architecture](https://productresources.collibra.com/docs/collibra/latest/Content/Architecture/ref_dgc-building-blocks.htm) and is attempting to change attributes of specific assets within two Collibra domains. The user will then in turn need the domain IDs (see below), the asset type IDs they would like to examine within the domains, the asset limit, and the attribute type IDs they would like to change. The code further assumes that the user knows how to find all the IDs.
2. The code assumes a user is transferring information from one domain to another and that the domain IDs for both of these domains is known. Currently, the config file includes the domain IDs from the UCLA Health DEV Collibra site for the Clinical and Discovery Data Marts. 
3. The code assumes the user has the correct access to the domains they are attempting to get information from (in other words, the user’s ‘Authorization’ key is valid and they have the permission to view, read, and modify Collibra data from the domains). Similarly, it is assumed the user knows how to find this information (from [Postman](https://www.postman.com/product/what-is-postman/), the developer docs, etc). 

### Future Improvements
1. Expansion on config file for flexibility and privacy
2. Streamlined way to get type IDs, domain IDs, user authorization keys, etc. to allow for easier usage and potentially more use cases -> Write code using the GET call from the requests package to get IDs within the code or automatically find the IDs using search tools or NLP
4. Try / except errors and troubleshooting built into code
5. More efficient comparison method than nested for loops to compare DDR and Clinical DM transformation logic (consider runtime)

