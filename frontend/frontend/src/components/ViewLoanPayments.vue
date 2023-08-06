<template>
    <div>    
        <!-- List All Loan Payments -->
        <h2>Loan Payments</h2>
        <v-card v-for="loanPayment in loanPayments" :key="loanPayment.id">
            <v-card-title>{{ loanPayment.id }}</v-card-title>
            <v-card-text>
                <p>Loan: {{ loanPayment.loan }}</p>
                <p>Amount: {{ loanPayment.amount }}</p>
            </v-card-text>
        </v-card>
    
    </div>
    </template>
    
      
    <script>
    import axios from 'axios';
    
    export default {
        data() {
            return {
                loanPayments: [],
            };
        },
        methods: {
            fetchLoanPayments() {
                // Make an API call to fetch all loan payments
                        axios.get('/loans/make-payment/', {
                  headers: {
                    'Authorization': `Token ${localStorage.getItem('token')}` 
                  }
                })
                          .then(response => {
                            // Handle success response and update the loan payments list
                            this.loanPayments = response.data;
                          })
                          .catch(error => {
                            // Handle error response
                            this.$toast.error(error.response.data.error);
                            this.$router.push({ name: 'error', params: { code: error.response.status } });
                          });
    
                // For demonstration purposes, let's simulate a successful response and update the loan payments list
                // this.loanPayments = [
                //   {
                //     id: 1,
                //     title: 'Loan Payment 1',
                //     loan: 'Loan 1',
                //     amount: 1000,
                //   },
                //   {
                //     id: 2,
                //     title: 'Loan Payment 2',
                //     loan: 'Loan 2',
                //     amount: 1500,
                //   },
                // ];
            },
        },
        mounted() {
            // Fetch loan payments when the component is mounted
            this.fetchLoanPayments();
        },
    };
    </script>
    