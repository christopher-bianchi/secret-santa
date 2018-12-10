# secret-santa
A simple script that automates matching and emailing for the Secret Santa holiday event.
It takes a list of participants and for each santa participant will pair them with a giftee, notifying all participants of their match.

- `santas.txt`: list of participants by email and name.
- `email_template.txt`: the message that is sent to each participant.
    - The email signoff name can be set inside the `docker-compose.yml`.
- Credentials for the mailing account will need to be set.

## Prerequisites
- Install Docker: https://docs.docker.com/docker-for-mac/install/
- A gmail account with permissions to send messages remotely.

## Setup
1. Clone the repo.
2. Set local environment secrets for the email account that will be sending the event emails.
    1. Open `~/.profile` for edit.
    2. Add `SANTA_MAILER_ACCOUNT_EMAIL` to `~/.profile`:
        - `export SANTA_MAILER_ACCOUNT_EMAIL=<mailer_email_address>`
    3. Replace `<mailer_email_address>` with the email address that will be sending the event emails.
    4. Add `SANTA_MAILER_ACCOUNT_TOKEN` to `~/.profile`:
        - `export SANTA_MAILER_ACCOUNT_TOKEN=<mailer_app_token>`
    5. Replace `<mailer_app_token>` with the password token for the email account.
3. Reload profile to apply new env variables: `source ~/.profile`
4. Open `docker-compose.yml`.
5. Find `SANTA_EMAIL_SIGNOFF_NAME` under the `environment` section.
6. Set the signoff name that will be used in the event emails by replacing `<signoff_name>`.
    - e.g. `SANTA_EMAIL_SIGNOFF_NAME=Christopher`
7. Save `docker-compose.yml`.
8. Open `santas.txt`.
9. Add the email addresses and names of all participants starting at line 2 (under the file header).
    1. Remove the placeholder email examples at line 2 and line 3.
    2. Add an email address, a space, then a name for the participant on one line.
    3. Repeat on a new line for every participant until all event participants have been added to the `santas.txt` file.
10. Save `santas.txt`.

## Run it!
1. `docker-compose run --rm secret-santa`
