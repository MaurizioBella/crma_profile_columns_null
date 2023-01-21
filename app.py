from salesforce_connection import SalesforceConnection
import requests
import json
import os

def get_list_fields(object_name):
    ''' Lists information about limits in your org '''
    # https://developer.salesforce.com/docs/atlas.en-us.api_rest.meta/api_rest/resources_limits.htm
    result = []
    sf = SalesforceConnection.getInstance()
    
    query = "select DeveloperName from FieldDefinition where EntityDefinition.DeveloperName  = '{0}'".format(
        object_name)

    # data = sf.query_all_iter(
    #     "select DeveloperName from FieldDefinition where EntityDefinition.DeveloperName  = 'Case'")
    data = sf.query_all_iter(query)
    print("list of all fields")
    for row in data:
        # print(row["DeveloperName"])
        result.append(row["DeveloperName"])
    print(result)
    return result


def check_field_usage(dataset_id, result):
    # result = ['CaseNumber']
    import requests

    sf = SalesforceConnection.getInstance()
    url_dataset = "{0}wave/datasets/{1}".format(sf.base_url, dataset_id)
    response = requests.get(url_dataset, headers={
        "Authorization": "Bearer " + sf.session_id})
    crmaid_currentVersionId = ''

    try:
        data = json.loads(response.text)
        crmaid_currentVersionId = '{0}/{1}'.format(data.get(
            'id'), data.get('currentVersionId'))
        print("crmaid/currentVersionId: {0}".format(crmaid_currentVersionId))
    except AttributeError as ae:
        print(ae)
    except IndexError as ie:
        print(ie)

    query_count_records = {
        'query': 'q = load \"'+crmaid_currentVersionId+'\";'
        + 'q = group q by all;'
        + 'q = foreach q generate count() as \'count\';'
    }

    msgJson = json.dumps(query_count_records)

    headers = {"Authorization": "Bearer " +
               sf.session_id, "Content-Type": "application/json"}

    url_query = "{0}wave/query/".format(sf.base_url)
    r = requests.post(url_query, headers=headers, data=msgJson)
    total_records = 0
    try:
        data = json.loads(r.text)
        total_records = data.get(
            'results').get('records')[0].get('count')
    except AttributeError as ae:
        error = "AttributeError: {0}".format(ae)
    except IndexError as ie:
        error = "IndexError: {0}".format(ie)
    print("Total records in the dataset: {0}".format(total_records))
    header = "field,count_null,perc_null\n"
    print(header)
    output = []
    output.append(header)
    for i in result:
        query_null = {
            'query': 'q = load \"'+crmaid_currentVersionId+'\";'
            # + 'q = filter q by \'AccountId\' is not null;'
            + 'q = filter q by \''+i+'\' is null;'
            + 'q = group q by all;'
            + 'q = foreach q generate count() as \'count\';'
        }

        msgJson = json.dumps(query_null)
        # print(msgJson)
        headers = {"Authorization": "Bearer " +
                   sf.session_id, "Content-Type": "application/json"}

        url_query = "{0}wave/query/".format(sf.base_url)
        r = requests.post(url_query, headers=headers, data=msgJson)
        try:
            if r.status_code != 200:
                count = '-'
                percentage = '-'
            else:
                data = json.loads(r.text)
                if not data.get('results').get('records'):
                    count = 0
                else:
                    count = data.get(
                        'results').get('records')[0].get('count')
                percentage = int(count / total_records * 100)
            field_usage = '{0},{1},{2}\n'.format(i, count, percentage)
            print(field_usage)
            output.append(field_usage)
        except AttributeError as ae:
            error = "AttributeError: {0}".format(ae)
        except IndexError as ie:
            error = "IndexError: {0}".format(ie)
            print(error)
    print("check output_profile_columns_null.csv")
    with open('output_profile_columns_null.csv', 'w') as f:
        f.writelines(output)


if __name__ == '__main__':
    # object_name = 'Case'
    if os.path.exists(".env"):
        object_name = input("write the object name e.g., Case:\n")
        # Add the <Dataset Id> https://developer.salesforce.com/docs/atlas.en-us.200.0.bi_dev_guide_rest.meta/bi_dev_guide_rest/bi_resources_dataset_id.htm
        # dataset_id = '0Fb8c000000nJZvCAM'
        dataset_id = input ("write the dataset id e.g., 0Fb8c000000nJZvCAM:\n")
        result = get_list_fields(object_name)
        check_field_usage(dataset_id, result)
    else:
        print("File .env missing.")

    
