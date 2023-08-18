# Bank-Loans

## Problem Statment 
The bank should receive funds from loan providers and be able to lend its customers within the limit of total funds. A user should be able to login to the system through a username and password. You have 3 user roles that you need to account for:
### Description:
    - Loan Provider: Should represent the total budget of the loans
    - Loan Customer: Should represent the loan, loan’s term and the loan’s amount
    - The Bank Personnel: Should define max and min amounts, interest rate, duration for each loan
### Endpoints:
    - Loan Providers:
        View status of loan fund applications.
    - Loan Customers:
        View status of loan applications.
        Make payments for his loans
    - The Bank Personnel:
        View applications from loan providers and customers and be able to above.
        The system should always make sure that the total loans should not exceed the total funds.

## Tools Used
- Django REST framework
- Vue.js
- Vuetify

## How to run it
1- Make sure you have the necessary packages installed, you can find the necessary packages to run the backend project in backend\requirements.txt and you can find the necessary packages to run the frontend project in frontend\frontend\package.json    
2- After cloning the project to your GitHub directory, open your command prompt in the project directory     
3- run the following commands    

    cd backend
    env\Scripts\activate    
    python manage.py runserver  
4- After running the previous commands go back to the project root directory using the following command    

    cd ..
5- To run the frontend project, run the following commands    

    cd frontend\frontend
    yarn dev
    
  

