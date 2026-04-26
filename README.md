<a id="readme-top"></a>

<div align="center">

# Meddiff **TODO**

Helps with white blood cells counting in school.
**TODO**


</div>

## Table of Contents

- [Meddiff](#optimisation-and-bio-inspired-algorithms)
	- [Table of Contents](#table-of-contents)
	- [About](#about)
	- [Project Structure](#project-structure)
	- [Getting Started](#getting-started)
		- [Prerequisites](#prerequisites)
		- [Installation](#installation)
	- [Usage](#usage)
	- [Roadmap](#roadmap)
		- [Authors](#authors)
	- [License](#license)

## About

TODO

[Back to top](#readme-top)

## Goals

**TODO**

[Back to top](#readme-top)

## Project Structure


```text
Meddiff/
	LICENSE
	README.md
	documentation
	pages/
	source/
	templates/
```

[Back to top](#readme-top)

## Getting Started

### Prerequisites

- git
- python 3.10+
- streamlit
- pandas
- streamlit_authenticator
- plotly

### Installation

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
Distributed under The Unlicense license.
For more information see `LICENSE`.

[Back to top](#readme-top)
