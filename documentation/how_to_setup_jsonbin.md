# Setting up your JSONBIN.io account for using Meddiff

## Register an account

1. Go to the [create account page](https://jsonbin.io/create-account).
2. Fill all the required fields with your personal details.
3. Press **Create Account**.
4. Verify your email.
5. Done.


## Create two Bins

1. Go to the [login page](https://jsonbin.io/login).
2. Input your credentials and login.
3. Select **Bins** on the left side menu.
4. Press **Create a Bin**.
5. In the panel that has opened on the right side of your window input the following JSON format:
```
{
  "record": {}
}
```
10. Use `jsonbin` for the name and save it.
11. Copy the **Bin ID** of the two bins for later use.
12. Done.


## Get the Master key

1. Go to the [login page](https://jsonbin.io/login).
2. Input your credentials and login.
3. Select **API KEYS** on the left side menu.
4. Copy the **X-Master-Key** for later use.
5. If you need a new key, for possible security reasons, you can press the two circular arrows button to generate a new one. Make sure to update it everywhere afterwards.
6. Done.


## Setup the Streamlit .toml file

1. Make sure you have followed the [Installation](../README.md#Installation) instructions correctly.
2. Open the `Meddiff/source/.streamlit/secrets.toml` file with a text editor.
3. Copy the **X-Master-Key** mentioned above to the `api_key` occurences (within single quotes).
4. Copy the **Bin ID** of the `jsonbin` bin to the `bin_id` field under the `[jsonbin]` tag (within single quotes).
5. Save the file.
6. Done.

