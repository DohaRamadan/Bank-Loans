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
    <div>
        <v-alert v-if="showSuccessAlert" elevation="4" prominent type="success">
            Success! Your loan amount is {{ laonAmount }}$
        </v-alert>
    </div>

</v-container>
</template>

<script>
import axios from 'axios';

export default {
    data() {
        return {
            loan: '',
            amount: '',
            showSuccessAlert: false,
            laonAmount: null,
            errorMessage: ''
        };
    },
    methods: {
        submitLoanPayment() {
            const loanPayment = {
                loan: this.loan,
                amount: this.amount,
            };

            axios
                .post('/loans/make-payment/', loanPayment, {
                    headers: {
                        Authorization: `Token ${localStorage.getItem('token')}`,
                    },
                })
                .then(() => {

                    // Make API call to get available amount
                    axios
                        .get('/get-loan-amount', {
                            headers: {
                                Authorization: `Token ${localStorage.getItem('token')}`,
                            },
                        })
                        .then(response => {
                            console.log(response)
                            this.laonAmount = response.data.loan_amount;
                            this.showSuccessAlert = true;
                        })
                        .catch(error => {
                            let message = error.response.data.error
                            this.$router.push({
                                name: 'ErrorPage',
                                query: {
                                    errorMessage: message
                                }
                            });
                        });
                })
                .catch(error => {
                    console.log(error.response.data.error)
                    let message = error.response.data.error
                    this.$router.push({
                        name: 'ErrorPage',
                        query: {
                            errorMessage: message
                        }
                    });
                });

            // Clear the form fields
            this.clearForm();
        },
        clearForm() {
            this.loan = '';
            this.amount = '';
            this.errorMessage = '';
        },
    },
};
</script>
