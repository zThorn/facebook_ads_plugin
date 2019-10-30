from urllib.parse import urlencode
import requests
import time

from airflow.hooks.base_hook import BaseHook


class FacebookAdsHook(BaseHook):
    def __init__(self, facebook_ads_conn_id="facebook_ads_default"):
        self.facebook_ads_conn_id = facebook_ads_conn_id
        self.connection = self.get_connection(facebook_ads_conn_id)

        self.base_uri = "https://graph.facebook.com"
        self.api_version = self.connection.extra_dejson["apiVersion"] or "4.0"
        self.access_token = (
            self.connection.extra_dejson["accessToken"] or self.connection.password
        )

    def get_insights_for_account_id(
        self,
        insight_fields,
        breakdowns,
        time_range,
        account_id=None,
        campaign_id=None,
        adset_id=None,
        ad_id=None,
        time_increment="all_days",
        level="ad",
        limit=1000,
    ):
        payload = urlencode(
            {
                "access_token": self.access_token,
                "breakdowns": ",".join(breakdowns),
                "fields": ",".join(insight_fields),
                "time_range": time_range,
                "time_increment": time_increment,
                "level": level,
                "limit": limit,
            }
        )

        if account_id is not None:
            api_method = "act_{0}".format(account_id)
        elif campaign_id or adset_id or ad_id is not None:
            # Get the first non-None id, the FB API method is the same for all 3.
            api_method = next((x for x in [campaign_id, adset_id, ad_id] if x), None)
        else:
            # Return empty list, this will cause the operator to error out in this scenario
            return []

        response = requests.get(
            "{base_uri}/v{api_version}/act_{account_id}/insights?{payload}".format(
                base_uri=self.base_uri,
                api_version=self.api_version,
                api_method=api_method,
                payload=payload,
            )
        )

        response.raise_for_status()
        response_body = response.json()
        insights = []

        while "next" in response_body.get("paging", {}):
            time.sleep(0.25)
            insights.extend(response_body["data"])
            response = requests.get(response_body["paging"]["next"])
            response.raise_for_status()
            response_body = response.json()

        insights.extend(response_body["data"])

        return insights
