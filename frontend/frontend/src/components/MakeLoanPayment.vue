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
            Success! Your available amount is {{ availableAmount }}$
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
            availableAmount: null,
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
                        .get('/get-available-amount', {
                            headers: {
                                Authorization: `Token ${localStorage.getItem('token')}`,
                            },
                        })
                        .then(response => {
                            console.log(response)
                            this.availableAmount = response.data.available_amount;
                            this.showSuccessAlert = true;
                        })
                        .catch(error => {
                            console.log(error);
                            const statusCode = error.response ? error.response.status : 500;
                            // Handle error response
                            if (statusCode === 400) {
                                this.errorMessage = error.response.data.error;
                            } else {
                                this.$router.push({
                                    name: 'ErrorPage',
                                    params: {
                                        code: statusCode
                                    }
                                });
                            }
                        });
                })
                .catch(error => {
                    const statusCode = error.response ? error.response.status : 500;
                    console.error(error);
                    // Handle error response
                    this.$router.push({
                        name: 'ErrorPage',
                        params: {
                            code: statusCode
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
