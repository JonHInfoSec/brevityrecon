import io, json
import brevitycore.core

def prepareInteract(programName,inputBucketName, interactType):
    if (interactType == 'server'):
        scriptStatus = generateScriptInteractServer(programName,inputBucketName)
        return scriptStatus
    if (interactType == 'client'):
        scriptStatus = generateScriptInteractClient(programName, inputBucketName)
        return scriptStatus
    else:
        scriptStatus = 'Incorrect options'
        return scriptStatus

def generateScriptInteractServer(programName, inputBucketName):
    secretName = 'brevity-interact-auth'
    regionName = 'us-east-1'
    secretRetrieved = brevitycore.core.get_secret(secretName,regionName)
    secretjson = json.loads(secretRetrieved)
    interactAuthToken = secretjson['interact-auth']
    fileBuffer = io.StringIO()
    fileContents = f"""#!/bin/bash

# Run custom interactsh script
export HOME=/root
export PATH=/root/go/bin:$PATH

mkdir $HOME/security/presentation
mkdir $HOME/security/presentation/interact

interactsh-server -domain brr.icicles.io -token {interactAuthToken} -smb &"""

#sh $HOME/security/run/{programName}/stepfunctions-{programName}.sh"""

    fileBuffer.write(fileContents)
    objectBuffer = io.BytesIO(fileBuffer.getvalue().encode())
    # Upload file to S3
    object_name = 'interact-' + programName + '.sh'
    object_path = 'run/' + programName + '/' + object_name
    status = brevitycore.core.upload_object(objectBuffer,inputBucketName,object_path)
    fileBuffer.close()
    objectBuffer.close()
    return status

def generateScriptInteractClient(programName, inputBucketName):
    secretName = 'brevity-interact-auth'
    regionName = 'us-east-1'
    secretRetrieved = brevitycore.core.get_secret(secretName,regionName)
    secretjson = json.loads(secretRetrieved)
    interactAuthToken = secretjson['interact-auth']
    fileBuffer = io.StringIO()
    fileContents = f"""#!/bin/bash

# Run custom interactsh script
export HOME=/root
export PATH=/root/go/bin:$PATH

mkdir $HOME/security/presentation
mkdir $HOME/security/presentation/interact
interactsh-client -server http://brr.icicles.io -token {interactAuthToken} -v -o interactsh-logs.txt -json &"""

#sh $HOME/security/run/{programName}/stepfunctions-{programName}.sh"""

    fileBuffer.write(fileContents)
    objectBuffer = io.BytesIO(fileBuffer.getvalue().encode())
    # Upload file to S3
    object_name = 'interact-' + programName + '.sh'
    object_path = 'run/' + programName + '/' + object_name
    status = brevitycore.core.upload_object(objectBuffer,inputBucketName,object_path)
    fileBuffer.close()
    objectBuffer.close()
    return status

def generateInstallScriptInteract(inputBucketName):
    # Load AWS access keys for s3 synchronization
    secretName = 'brevity-aws-recon'
    regionName = 'us-east-1'
    secretRetrieved = brevitycore.core.get_secret(secretName,regionName)
    secretjson = json.loads(secretRetrieved)
    awsAccessKeyId = secretjson['AWS_ACCESS_KEY_ID']
    awsSecretKey = secretjson['AWS_SECRET_ACCESS_KEY']
    
    fileBuffer = io.StringIO()
    fileContents = f"""#!/bin/bash

# Create directory structure
export HOME=/root
mkdir $HOME/security
mkdir $HOME/security/tools
mkdir $HOME/security/tools/amass
mkdir $HOME/security/tools/amass/db
mkdir $HOME/security/tools/hakrawler
mkdir $HOME/security/tools/interactsh
mkdir $HOME/security/raw
mkdir $HOME/security/refined
mkdir $HOME/security/presentation
mkdir $HOME/security/presentation/interactsh
mkdir $HOME/security/scope
mkdir $HOME/security/install
mkdir $HOME/security/config
mkdir $HOME/security/run
mkdir $HOME/security/inputs

# Update apt repositories to avoid software installation issues
apt-get update

# Ensure OS and packages are fully upgraded
#apt-get -y upgrade

# Install Git
apt-get install -y git # May already be installed

# Install Python and Pip
apt-get install -y python3 # Likely is already installed
apt-get install -y python3-pip

# Install Golang via cli
#apt-get install -y golang
cd $HOME/security/config/
wget https://go.dev/dl/go1.17.5.linux-amd64.tar.gz
sudo tar -xvf go1.17.5.linux-amd64.tar.gz
sudo rm -R /usr/lib/go
sudo mv go /usr/lib

echo 'export GOROOT=/usr/lib/go' >> ~/.bashrc
echo 'export GOPATH=$HOME/go' >> ~/.bashrc
echo 'export PATH=$GOPATH/bin:$GOROOT/bin:$PATH' >> ~/.bashrc
source ~/.bashrc
    
# Install aws cli
apt-get install -y awscli

# Install go tools
go install -v github.com/projectdiscovery/interactsh/cmd/interactsh-server@latest
go install -v github.com/projectdiscovery/interactsh/cmd/interactsh-client@latest"""
    fileBuffer.write(fileContents)
    objectBuffer = io.BytesIO(fileBuffer.getvalue().encode())

    # Upload file to S3
    object_name = 'bounty-startup-interact.sh'
    object_path = 'config/' + object_name
    bucket = inputBucketName
    installScriptStatus = brevitycore.core.upload_object(objectBuffer,bucket,object_path)
    fileBuffer.close()
    objectBuffer.close()
    return installScriptStatus