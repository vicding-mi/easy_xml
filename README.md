# Ingest EASY json to Dataverse

This repo contains the scripts to import/update/publish EASY social science datasets. The scripts are made to be small and atomic. The goal is to run them within flow management system, like Airflow for better presentation, automation and governance/provenance.  
`Python 3.7` recommended. `lxml==4.6.3` and `pyDataverse==0.2.1` are the version dev against. 

## Steps to follow
#### 0 prerequisite 
 0. create `dvconfig.py`
```python
base_url = 'http://localhost:8080'
api_token = 'xxx-xxx-xxx-xxx'

dataverse_name = 'dv_id'
easy_json_path = '/absolute/path/to/ds/json/folder'
```
#### A. importing (not complete, demo purpose only as migration will be done by migration team for data stations)
 1. Run `saxon in docker` to convert xml to json datasets
 2. Run `cp_all_socialsciences_ds.py` to copy all social science datasets to designated folder
 3. Run `validate_json.py` to verify and cleanse newly created json files
 4. Run `remove_file_info.py` to remove all the file info from copied json datasets
 5. Run `clean_subject.py` to set subject (also known as audience) of json datasets to 'Social Sciences'
 6. Run `import_dataset.py` to import datasets
#### B. updating ds with additional metadata files
 7. Get all additional files 
 8. Run `convert_additional_files_to_json.py` to convert all the additional files to json file. example below
 9. Run `update_dataset.py` to attach additional info
    1. Please note: before running this script, all the datasets should be in DRAFT mode
 10. Run `publish_ds.py` to publish sub dataverses and datasets, you can choose all, with additional metadata file or not. 

### Utility functions (not part of importing or updating)
 1. `check_ds_additional_metadata_json_exists.py` checks if the dataset contains the P file exists in DV
 2. `list_easy_additional_metadata_files.py` lists all the datasets with additiona P files
 3. `get_all_subject_value.py` list different subject/audience values
 4. `destroy_all_dvobjects.py` copied from [dataverse-sample-data](https://github.com/IQSS/dataverse-sample-data) and slightly modified to remove dv and its children. `python destroy_all_dvobjects.py dv_name yes`. dv_name is the dataverse you would like to delete from. and the trailing 'yes'/'no' denotes that if you want to remove the dv itself. 

### Notes
 1. when `update_dataset`, the structure should be the one below. 
 2. using `editMetadata` API for now, might have to switch to other API due to inconsistent behaviour
```
{
  "fields": [
    {
      "typeName": "title",
      "multiple": false,
      "value": "title",
      "typeClass": "primitive"
    },
    {
      "typeName": "dsDescription",
      "multiple": true,
      "typeClass": "compound",
      "value": [
        {
          "dsDescriptionValue": {
            "typeName": "dsDescriptionValue",
            "multiple": false,
            "value": "value text",
            "typeClass": "primitive"
          }
        }
      ]
    },
    {
      "typeName": "datasetContact",
      "multiple": true,
      "typeClass": "compound",
      "value": [
        {
          "datasetContacEmail": {
            "typeName": "datasetContactEmail",
            "multiple": false,
            "value": "info@dans.knaw.nl",
            "typeClass": "primitive"
          }
        }
      ]
    }
  ]
}```