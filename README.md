# deps
A smart dependencies assistant that will install dependencies for you to make you code work or inject a script into a folder to make a python script reay to use!

# WARNING
Deps is in development still, i cannot guarentee 100% functionability.


# Installation
```bash
git clone https://github.com/lucy407/deps.git
cd Deps

Install required packages (if any):
```

```bash
python3 -m pip install -r requirements.txt
```
Make deps.py executable:
```
chmod +x deps.py`
```

# Usage
```bash
python3 deps.py --dev /path/to/script.py
```
This will install all dependencies you need as the developer to get your code working, it uses its smart scanning feature to check for imports & instal them
```bash
python3 deps.py --packageit /path/to/scripts/folder
```
This command injects it's smart installing assistant into the folder so when ran it installs the dependencies the user needs so the main scripts ready to go!

