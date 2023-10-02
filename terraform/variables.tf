variable "application_name" {
  description = "Name of the application"
  type        = string
  default     = "lilly-poc2"
}

variable "location" {
  description = "Location of the resources"
  type        = string
  default     = "eastus"
}

variable "environment" {
  description = "Environment of the resources"
  type        = string
  default     = "dev"
}

variable "cost_center" {
  description = "Cost center of the resources"
  type        = string
  default     = "12345"
}

variable "project" {
  description = "Project of the resources"
  type        = string
  default     = "azfnflaskdemo"
}

variable "owner" {
  description = "Owner of the resources"
  type        = string
  default     = "jdoe@contoso.com"

  validation {
    condition     = can(regex("^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$", var.owner))
    error_message = "The owner must be a valid email address."
  }
}

variable "python_version" {
  description = "Python version to use for the Function App"
  type        = string
  default     = "3.9"
}

variable "enable_blob_storage" {
  description = "Feature flag to control the creation of Blob Storage"
  type        = bool
  default     = false # By default, it's set to false (disabled).
}
