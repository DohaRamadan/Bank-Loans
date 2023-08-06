<template>
    <v-container class="submit-loan-container">
      <v-card class="submit-loan-card">
        <v-card-title class="submit-loan-title">Submit Loan Fund Application</v-card-title>
        <v-card-text>
          <v-form @submit.prevent="submitLoanApplication">
            <v-text-field v-model="amount" label="Amount" required></v-text-field>
            <v-btn type="submit" color="primary">Submit Loan Fund Application</v-btn>
          </v-form>
        </v-card-text>
      </v-card>
    </v-container>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        amount: ''
      };
    },
    methods: {
      submitLoanApplication() {
        const loanApplication = {
          amount: this.amount
        };
  
        axios
          .post('/loan-applications/submit/', loanApplication, {
            headers: {
              Authorization: `Token ${localStorage.getItem('token')}`
            }
          })
          .then(response => {
            // Handle success response and update the loan applications list
            this.loanApplications.push(response.data);
          })
          .catch(error => {
            // Handle error response
            // this.$toast.error(error.response.data.error);
            this.$router.push({ name: 'error', params: { code: error.response.detail } });
          });
  
        // Clear the form field
        this.amount = '';
      }
    }
  };
  </script>
  
  <style scoped>
  .submit-loan-container {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
  }
  
  .submit-loan-card {
    max-width: 400px;
    width: 100%;
    padding: 24px;
  }
  
  .submit-loan-title {
    font-size: 24px;
    font-weight: bold;
    margin-bottom: 16px;
  }
  </style>