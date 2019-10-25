# Airflow Plugin - Facebook Ads
This plugin moves data from the Facebook Ads API to GCS based on the specified object

## Hooks
### Facebook Ads Hook
This hook handles the authentication and request to Facebook Ads.

### GCSHook
Contrib Airflow GCSHook with the standard boto dependency.

## Operators
### FacebookAdsToGCSOperator
This operator composes the logic for this plugin. It queries Facebook Ads Insights and drops the results in an GCS bucket. It accepts the following parameters:
``` Facebook Ads Insights To GCS Operator
    :param facebook_conn_id:        The source facebook connection id.
    :type gcs_conn_id:               string
    :param gcs_conn_id:              The destination gcs connection id.
    :type gcs_conn_id:               string
    :param gcs_bucket:               The destination gcs bucket.
    :type gcs_bucket:                string
    :param gcs_key:                  The destination gcs key.
    :type gcs_key:                   string
    :param account_ids:             An array of Facebook Ad Account Ids strings which
                                    own campaigns, ad_sets, and ads.
    :type account_ids:              array
    :param insight_fields:          An array of insight field strings to get back from
                                    the API.  Defaults to an empty array.
    :type insight_fields:           array
    :param breakdowns:              An array of breakdown strings for which to group insights.abs
                                    Defaults to an empty array.
    :type breakdowns:               array
    :param since:                   A datetime representing the start time to get Facebook data.
                                    Can use Airflow template for execution_date
    :type since:                    datetime
    :param until:                   A datetime representing the end time to get Facebook data.
                                    Can use Airflow template for next_execution_date
    :type until:                    datetime
    :param time_increment:          A string representing the time increment for which to get data,
                                    described by the Facebook Ads API. Defaults to 'all_days'.
    :type time_increment:           string
    :param level:                   A string representing the level for which to get Facebook Ads data,
                                    can be campaign, ad_set, or ad level.  Defaults to 'ad'.
    :type level:                    string
    :param limit:                   The number of records to fetch in each request. Defaults to 100.
    :type limit:                    integer```
