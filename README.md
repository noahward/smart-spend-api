# SmartSpend

Spend smarter, not harder. Track and categorize your spending, set budgeting goals, and receive insights into how to better manage your money.

This ```README.md``` serves as the documentation for both the SmartSpend API and the [SmartSpend UI](https://github.com/noahward/smart-spend-ui).



## Features

- Create an account secured by token authentication
- Add your spending/saving accounts and upload transactions to them
- Categorize your transactions by utilizing the default categories or creating your own
- Develop a budget to fit your needs and allocate funds to areas of spending
- Receive insights into your spending habits through an intuitive dashboard


## Run Locally

Both the API and UI need to be cloned and set up using seperate terminal instances. 

You may choose to run the API and not the UI depending on your development needs, and vise versa.

#### API Setup

```bash
  git clone https://github.com/noahward/smart-spend-api.git
  
  cd budget-buddy-api           # Navigate to the project 
  pip install tox               # Install tox globally
  tox -e dev                    # Create a development environment using tox
  .\venv\Scripts\activate       # Activate the virtual environment
  python manage.py runserver    # Run the server
```

Environment variable template: ```.env.dist``` serves as a template for the required API environment variables.

Create either a ```.env.dev``` or a ```.env.prod``` file and populate it.

#### UI Setup

```bash
  git clone https://github.com/noahward/smart-spend-ui.git

  cd budget-buddy-ui            # Navigate to the project
  npm install                   # Install dependencies
  quasar dev                    # Run the development server
```

Environment variable template: ```.env.development```

Create either a ```.env.development.local``` or a ```.env.production.local``` file and populate it.
