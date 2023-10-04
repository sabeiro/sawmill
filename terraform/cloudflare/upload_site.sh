 aws s3 cp website/ s3://$(terraform output -raw website_bucket_name)/ --recursive
