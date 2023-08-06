<template>
<v-container>
    <h1 class="display-1">Make Loan Payment</h1>

    <!-- Loan Payment Form -->
    <v-form @submit.prevent="submitLoanPayment">
        <v-row>
            <v-col cols="12" md="6">
                <v-text-field v-model="amount" label="Amount" outlined required></v-text-field>
            </v-col>
        </v-row>
        <v-row>
            <v-col>
                <v-btn type="submit" color="primary" class="mr-4">Submit Loan Payment</v-btn>
                <v-btn @click="clearForm">Clear</v-btn>
            </v-col>
        </v-row>
    </v-form>
</v-container>
</template>

  
<script>
import axios from 'axios';

export default {
    data() {
        return {
            loan: '',
            amount: '',
        };
    },
    methods: {
        submitLoanPayment() {
            const loanPayment = {
                loan: this.loan,
                amount: this.amount,
            };

            // Make an API call to submit the loan payment
            axios
                .post('/loans/make-payment/', loanPayment, {
                    headers: {
                        Authorization: `Token ${localStorage.getItem('token')}`,
                    },
                })
                .then(response => {
                    // Handle success response and update the loan payments list
                    this.loanPayments.push(response.data);
                })
                .catch(error => {
                    // Handle error response
                    this.$toast.error(error.response.data.error);
                    this.$router.push({
                        name: 'error',
                        params: {
                            code: error.response.status
                        }
                    });
                });

            // Clear the form fields
            this.clearForm();
        },
        clearForm() {
            this.loan = '';
            this.amount = '';
        },
    },
};
</script>
