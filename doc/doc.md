# 安装本地aws
    docker run --name dynamodb -p 8000:8000 amazon/dynamodb-local

# 安装aws-cli 

# 并配置key  secret
# aws configure
    AWS Access Key ID [None]: AKIAIOSFODNN7EXAMPLE
    AWS Secret Access Key [None]: wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
    Default region name [None]: us-west-2
    Default output format [None]: ENTER
# 要更新任何设置，只需再次运行 aws configure 并根据需要输入新值。