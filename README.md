<a id="readme-top"></a>

<div align="center">

# Meddiff 

![GitHub Repo Badge](https://img.shields.io/badge/github-repo-blue?logo=github)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Pandas](https://img.shields.io/badge/pandas-150458?logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![Plotly](https://img.shields.io/badge/Plotly-3F4F75?logo=plotly&logoColor=white)](https://plotly.com/python/)
[![Code style: PEP 8](https://img.shields.io/badge/code%20style-PEP%208-2ea44f.svg)](https://peps.python.org/pep-0008/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/chkameho/Meddiff/pulls)
[![GitHub issues](https://img.shields.io/github/issues/chkameho/Meddiff)](https://github.com/chkameho/Meddiff/issues)
[![GitHub last commit](https://img.shields.io/github/last-commit/chkameho/Meddiff)](https://github.com/chkameho/Meddiff/commits/main)
[![Status: WIP](https://img.shields.io/badge/status-active%20development-orange.svg)](#roadmap)

**Digital Hematology Cell Counter Application**

</div>

## Table of Contents

- [Meddiff]
	- [Table of Contents](#table-of-contents)
	- [About](#about)
	- [Goals](#goals)
	- [Project Structure](#project-structure)
	- [Getting Started](#getting-started)
		- [Prerequisites](#prerequisites)
		- [Installation](#installation)
	- [Usage](#usage)
	- [Roadmap](#roadmap)
	- [Authors](#authors)
	- [License](#license)

## About

A Web app that digitalizes blood cell counting in schools, replacing pen & paper hematology lab work.
**Meddiff** is a web application powered by [Streamlit](https://streamlit.io/) that digitalizes the manual pen and paper blood cell counting for students in school hematology labs.


[Back to top](#readme-top)

## Goals

The main goal of this project is to digitalize the blood cell counting process in schools, instead of counting cells with pen & paper. Students use the application to record their counts directly and produce a clean digital results that are easy to submit, review and compare.

[Back to top](#readme-top)

## Project Structure


```text
Meddiff/
	LICENSE
	README.md
	documentation/
	pages/
	source/
		utils/
		pages/
	templates/
```

[Back to top](#readme-top)

## Getting Started
These instructions will get you a copy of Meddiff running on your local machine.
### Prerequisites

- git
- python 3.10+
- streamlit 1.54
- pandas 2.3.3
- streamlit_authenticator 0.4.2
- plotly 6.7.0

### Installation

**Linux**
```sh
git clone git@github.com:chkameho/Meddiff.git
cd Meddiff
python -m venv meddiff
source meddiff/bin/activate
pip install -r requirements.txt
cd source
mkdir .streamlit
cp ../templates/secrets.toml .streamlit/
cp ../templates/config.yaml .
```

**Windows (PowerShell)**
```sh
git https://github.com/chkameho/Meddiff.git
cd Meddiff
python -m venv meddiff
conda activate meddiff
pip install -r requirements.txt
cd source
mkdir .streamlit
copy ..\templates\secrets.toml .streamlit\
copy ..\templates\config.yaml .
```


[Back to top](#readme-top)

## Usage

- Follow the Installation instructions.
- Set up the environment:
	- [create a JSONBIN.io account](documentation/how_to_setup_jsonbin.md#register-an-account), if you do not have one.
	- [create two Bins](documentation/how_to_setup_jsonbin.md#create-two-bins) and copy their **Bin ID**.
	- [get the Master Key](documentation/how_to_setup_jsonbin.md#get-the-master-key).
	- [setup Streamlit's .toml file](documentation/how_to_setup_jsonbin.md#setup-the-streamlit-.toml-file).
- [Set up the user authentication](documentation/how_to_setup_user_auth.md).
- Run the program: `streamlit run Meddiff.py`

[Back to top](#readme-top)

### Authors

- **Ka Men Ho**
	- GitHub: [@chkameho](https://github.com/chkameho)
- **Sara Kasraian Fard**
	- Github: [@sarakasraian](https://github.com/sarakasraian)
- **Spyridon Margomenos**
	- Github: [@the-nerd-sloth](https://github.com/the-nerd-sloth)

[Back to top](#readme-top)

## License
Distributed under the MIT License.  
See `LICENSE` for more information.

[Back to top](#readme-top)
