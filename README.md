# CRMA check null fields

- Check how many fields have null value using CRMA via [API](https://developer.salesforce.com/docs/atlas.en-us.200.0.bi_dev_guide_rest.meta/bi_dev_guide_rest/bi_resources_dataset_id.htm)
- Prereq. CRMA with at least one [Dataset](https://help.salesforce.com/s/articleView?id=sf.bi_integrate_connectors_salesforce_local.htm&type=5) synched with a Salesforce object

# install it

```
python -m venv env
source env/bin/activate
pip install -r requirements.txt
```

- Create a file .env from env_template and add credentials

# run it

```
python app.py
write the object name e.g., Case:
Case
write the dataset id e.g., 0Fb8c000000nJZvCAM:
0Fb8c000000nJZvCAM
```

# Example of output

| field            | count_null | perc_null  |
| ---------------- | ---------- | ---------- |
| Row 1, id        | Row 1, 120 | Row 1, 100 |
| Row 2, IsDeleted | Row 2, -   | Row 2, -   |

`-` means the field doesn't exist in CRMA