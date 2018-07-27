# CustomizedPollingApp
A Python Django Web Application where group of people can anonymously agree on some top answers for a selected question/poll.

### About
This application is developed in Python Django, Where a user can create a poll, once user creates poll, user can send it to multiple participants
to get answers for the poll.
Atlast we will send link of results of voting poll to all participants.

### Running Application Locally

* First, clone the repository to your local machine
* Install the requirements:

```bash
pip install -r requirements.txt
```

* Create the database:

```bash
python manage.py migrate
```

* Run the development server:

```bash
python manage.py runserver
```

The project will be available at **127.0.0.1:8000**.
