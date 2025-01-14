from airflow.plugins_manager import AirflowPlugin
from facebook_ads_plugin.hooks.facebook_ads_hook import FacebookAdsHook
from facebook_ads_plugin.operators.facebook_ads_to_gcs_operator import (
    FacebookAdsInsightsToGCSOperator,
)


class FacebookAdsPlugin(AirflowPlugin):
    name = "FacebookAdsPlugin"
    hooks = [FacebookAdsHook]
    operators = [FacebookAdsInsightsToGCSOperator]
    executors = []
    macros = []
    admin_views = []
    flask_blueprints = []
    menu_links = []
