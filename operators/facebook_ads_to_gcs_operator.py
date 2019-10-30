import json
import os
from datetime import datetime

from airflow.contrib.hooks.gcs_hook import GoogleCloudStorageHook
from airflow.models import BaseOperator

from facebook_ads_plugin.hooks.facebook_ads_hook import FacebookAdsHook


class FacebookAdsInsightsToGCSOperator(BaseOperator):
    """
    Facebook Ads Insights To GCS Operator
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
    :type limit:                    integer
    """

    template_fields = ("gcs_key", "since", "until")

    def __init__(
        self,
        facebook_conn_id,
        gcs_conn_id,
        gcs_bucket,
        gcs_key,
        account_ids,
        insight_fields,
        breakdowns,
        since,
        until,
        time_increment="all_days",
        level="ad",
        limit=1000,
        *args,
        **kwargs
    ):
        super().__init__(*args, **kwargs)

        self.facebook_conn_id = facebook_conn_id
        self.gcs_conn_id = gcs_conn_id
        self.gcs_bucket = gcs_bucket
        self.gcs_key = gcs_key
        self.account_ids = account_ids
        self.insight_fields = insight_fields
        self.breakdowns = breakdowns
        self.since = since
        self.until = until
        self.time_increment = time_increment
        self.level = level
        self.limit = limit

    def execute(self, context):
        facebook_conn = FacebookAdsHook(self.facebook_conn_id)
        gcs_conn = GoogleCloudStorageHook(self.gcs_conn_id)

        time_range = {
            "since": datetime.strptime(self.since, "%Y-%m-%d %H:%M:%S").strftime(
                "%Y-%m-%d"
            ),
            "until": datetime.strptime(self.until, "%Y-%m-%d %H:%M:%S").strftime(
                "%Y-%m-%d"
            ),
        }

        file_name = "/tmp/{key}.jsonl".format(key=self.gcs_key)
        with open(file_name, "w") as insight_file:
            for account_id in self.account_ids:
                insights = facebook_conn.get_insights_for_account_id(
                    account_id,
                    self.insight_fields,
                    self.breakdowns,
                    time_range,
                    self.time_increment,
                    self.level,
                    self.limit,
                )

                if len(insights) > 0:
                    for insight in insights[:-1]:
                        insight_file.write(json.dumps(insight) + "\n")
                    insight_file.write(json.dumps(insights[-1:][0]))
                else:
                    return

        gcs_conn.upload(
            filename=file_name, bucket=gcs_bucket, object=gcs_key, gzip=True
        )
        os.remove(file_name)
