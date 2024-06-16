# End to end RAG using Amazon Bedrock

## How to run?

### 1. Create a new environment
```bash
conda create -n ragabedrock python=3.8 -y
```

### 2. Activate the environment.
```bash
conda activate ragabedrock
```

### 3. Intsall required dependencies
```bash
pip install -r requirements.txt
```

# AWS Cloud deployment
### 1. Install vim editor
```bash
sudo apt install git curl unzip tar make sudo vim wget -y
```
### 2. Clone the github
```bash
git clone "use_own_url"
```
### 3. After clone, go the directoy
```bash
cd rag_using_amazon_bedrock/
```
### 4. Create .env file
```bash
touch .env
```
### 5. Edit .env file and the secrets as mentioned below
```bash
vim .env
```
```bash
aws_access_key_id = ""
aws_secret_access_key = ""
region_name  = ""
```
### 6. Install python requiremets
```bash
sudo apt install python3-pip && sudo apt install python3-venv
```
### 7. Create virtual environment
```bash
python3 -m venv .venv
```
### 8. Activate virtual environment
```bash
source .venv/bin/activate
```
### 9. Install requirements
```bash
pip3 install -r requirements.txt
```

### Set inbound rule to acces the application
- Select the instance
- Go to security and select Security groups
- Click on inbund rulesand add port `8501` and source `0..0.0.0/0`
- Save the rule

### Temporary running of application
```bash
python3 -m streamlit run main.py
```

### Perminant running of application
```bash
nohub python3 -m streamlit run main.py
```