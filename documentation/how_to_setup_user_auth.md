# Setting up user Authentication

The **Meddiff** application has been setup using the `Streamlit-Authenticator` library, for easy deployment in new environments.
Without too many changes the application can be updated to accomondate other methods of authentication, like OIDC, but for the current offline setup do the following:

1. Open the `Meddiff/source/config.yaml` file with a text editor.
2. Update the `cookie.key` value with a secret key of your choice (string).
3. Update the `credentials.usernames.your_username` tag with your username.
4. Update the `credentials.usernames.your_username.name` value with your name.
5. Update the `credentials.usernames.your_username.password` value with your plaintext password. Upon the first run of the application, the password will be encrypted.
6. Save the file.
7. Done.
