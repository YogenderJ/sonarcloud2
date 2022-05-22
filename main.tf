terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3.27"
    }
  }

  required_version = ">= 1.1.0"
}

provider "aws" {
  profile = "default"
  region  = "us-west-1"
  #shared_config_file      = ["/home/ubuntu/.aws/config"]
  shared_credentials_file = "/home/ubuntu/.aws/credentials"
}

resource "aws_instance" "app_server" {
  #ami             = "ami-051f3cc34c1a9acf1"
  ami             = "ami-0f2e8890d8ce924e6"
  instance_type   = "t2.micro"
  subnet_id       = "subnet-00a0426959e893667"
  security_groups = ["sg-0f4f94173b985c38e"]
#  key_name        = "Yogender_account_keypair"
  key_name        = "Yog_new_aws_keypair"
#  key_name        = "yogender_new_aws_keypair"

  user_data = "${file("init.sh")}"
  tags = {
    Name = 'Yogesh'
  }
}

