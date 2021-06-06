import argparse
import sys
from pyDataverse.api import Api
import dvconfig
import requests

base_url = dvconfig.base_url
api_token = dvconfig.api_token

api = Api(base_url, api_token)
print('API status: ' + api.status)

dataverse_ids = []
dataset_ids = []


def main(hosting_dv='king', delete_self=False):
    print("Finding dataverses and datasets to destroy...")
    find_children(hosting_dv)
    dataset_ids.sort(reverse=True)
    for dataset_id in dataset_ids:
        print('Deleting dataset id ' + str(dataset_id))
        print('Preemptively deleting dataset locks for dataset id ' + str(dataset_id))
        resp = requests.delete(base_url + '/api/datasets/' + str(dataset_id) + '/locks?key=' + api_token)
        print(resp)
        resp = requests.delete(base_url + '/api/datasets/' + str(dataset_id) + '/destroy?key=' + api_token)
        print(resp)
    dataverse_ids.sort(reverse=True)
    for dataverse_id in dataverse_ids:
        print('Deleting dataverse id ' + str(dataverse_id))
        resp = api.delete_dataverse(dataverse_id)
        print(resp)
    if delete_self:
        print('Deleting current hosting dataverse ' + str(hosting_dv))
        resp = api.delete_dataverse(hosting_dv)
        print(resp)
    print("Done.")


def find_children(dataverse_database_id):
    query_str = '/dataverses/' + str(dataverse_database_id) + '/contents'
    params = {}
    resp = api.get_request(query_str, params=params, auth=True)
    for dvobject in resp.json()['data']:
        dvtype = dvobject['type']
        dvid = dvobject['id']
        if 'dataverse' == dvtype:
            find_children(dvid)
            dataverse_ids.append(dvid)
        else:
            dataset_ids.append(dvid)


def str2bool(v):
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


if __name__ == '__main__':
    hosting_dv = sys.argv[1]
    delete_self = str2bool(sys.argv[2])

    main(hosting_dv, delete_self)

