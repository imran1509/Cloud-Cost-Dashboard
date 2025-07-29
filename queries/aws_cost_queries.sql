select
  account_id,
  service,
  region,
  usage_type,
  usage_quantity,
  unblended_cost,
  start_time
from
  aws_billing_monthly_service;

