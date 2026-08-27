business_case = "northstar"

resource_group_name = "rg-cloud-dba-portfolio-dev"
location            = "East US"

vnet_name      = "vnet-cloud-dba-dev"
subnet_name    = "subnet-cloud-dba-dev"
nsg_name       = "nsg-cloud-dba-dev"
public_ip_name = "pip-cloud-dba-dev"
nic_name       = "nic-cloud-dba-dev"

portfolio_storage_account_name   = "stclouddbaportfolio01"
portfolio_storage_container_name = "portfolio-data"

sql_admin_login        = "sqladminnenim"
sql_server_name        = "sql-nenim-portfolio-cus-dev"
sql_server_location    = "Central US"
sql_database_name      = "CloudDBAPortfolioDB"
sql_firewall_rule_name = "Allow-My-Current-IP"
sql_firewall_ip        = "172.56.222.194"

log_analytics_name = "law-cloud-dba-dev"
key_vault_name     = "kv-nenim-cloud-dba-dev"
data_factory_name  = "adf-nenim-cloud-dba-dev"

data_lake_storage_account_name = "stnenimadlsdev01"
data_lake_containers           = ["bronze", "silver", "gold"]

databricks_name = "dbw-nenim-cloud-dba-dev"
databricks_sku  = "trial"
