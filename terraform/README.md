# lilly-iac-flask
poc project to demo iac and flask container deploy to az functions
<!-- BEGINNING OF PRE-COMMIT-TERRAFORM DOCS HOOK -->
## Requirements

| Name | Version |
|------|---------|
| <a name="requirement_azurerm"></a> [azurerm](#requirement\_azurerm) | ~>3.0 |

## Providers

| Name | Version |
|------|---------|
| <a name="provider_azurecaf"></a> [azurecaf](#provider\_azurecaf) | 1.2.26 |
| <a name="provider_azurerm"></a> [azurerm](#provider\_azurerm) | 3.75.0 |

## Modules

No modules.

## Resources

| Name | Type |
|------|------|
| [azurecaf_name.acr](https://registry.terraform.io/providers/aztfmod/azurecaf/latest/docs/resources/name) | resource |
| [azurecaf_name.stor](https://registry.terraform.io/providers/aztfmod/azurecaf/latest/docs/resources/name) | resource |
| [azurerm_container_registry.acr](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/container_registry) | resource |
| [azurerm_key_vault.this](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/key_vault) | resource |
| [azurerm_linux_function_app.this](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/linux_function_app) | resource |
| [azurerm_resource_group.this](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/resource_group) | resource |
| [azurerm_role_assignment.fnapp_to_acr](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/role_assignment) | resource |
| [azurerm_role_assignment.fnapp_to_kv](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/role_assignment) | resource |
| [azurerm_service_plan.this](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/service_plan) | resource |
| [azurerm_storage_account.blob_storage](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/storage_account) | resource |
| [azurerm_storage_account.this](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/storage_account) | resource |
| [azurerm_storage_container.blob_container](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/storage_container) | resource |
| [azurerm_client_config.current](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/data-sources/client_config) | data source |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_application_name"></a> [application\_name](#input\_application\_name) | Name of the application | `string` | `"lilly-poc2"` | no |
| <a name="input_cost_center"></a> [cost\_center](#input\_cost\_center) | Cost center of the resources | `string` | `"12345"` | no |
| <a name="input_enable_blob_storage"></a> [enable\_blob\_storage](#input\_enable\_blob\_storage) | Feature flag to control the creation of Blob Storage | `bool` | `false` | no |
| <a name="input_environment"></a> [environment](#input\_environment) | Environment of the resources | `string` | `"dev"` | no |
| <a name="input_location"></a> [location](#input\_location) | Location of the resources | `string` | `"eastus"` | no |
| <a name="input_owner"></a> [owner](#input\_owner) | Owner of the resources | `string` | `"jdoe@contoso.com"` | no |
| <a name="input_project"></a> [project](#input\_project) | Project of the resources | `string` | `"azfnflaskdemo"` | no |
| <a name="input_python_version"></a> [python\_version](#input\_python\_version) | Python version to use for the Function App | `string` | `"3.9"` | no |

## Outputs

| Name | Description |
|------|-------------|
| <a name="output_acr_id"></a> [acr\_id](#output\_acr\_id) | n/a |
| <a name="output_acr_login_server"></a> [acr\_login\_server](#output\_acr\_login\_server) | n/a |
| <a name="output_function_app_url"></a> [function\_app\_url](#output\_function\_app\_url) | n/a |
| <a name="output_key_vault_id"></a> [key\_vault\_id](#output\_key\_vault\_id) | n/a |
<!-- END OF PRE-COMMIT-TERRAFORM DOCS HOOK -->
