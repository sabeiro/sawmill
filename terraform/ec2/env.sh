#!/bin/sh
cat <<EOF
{
  "aws_region": "$aws_region"
  ,"aws_access_key": "$aws_access_key_id"
  ,"aws_secret_key": "$aws_secret_access_key"
}
EOF
