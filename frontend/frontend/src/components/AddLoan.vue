<template>
<v-container>
    <h1 class="display-1">Add Loan</h1>

    <!-- Add Loan Form -->
    <v-form @submit.prevent="addLoan">
        <v-row>
            <v-col cols="12" md="6">
                <v-text-field v-model="minAmount" label="Minimum Amount" required></v-text-field>
            </v-col>
            <v-col cols="12" md="6">
                <v-text-field v-model="maxAmount" label="Maximum Amount" required></v-text-field>
            </v-col>
        </v-row>
        <v-row>
            <v-col cols="12" md="6">
                <v-text-field v-model="interestRate" label="Interest Rate" required></v-text-field>
            </v-col>
            <v-col cols="12" md="6">
                <v-text-field v-model="duration" label="Duration" required></v-text-field>
            </v-col>
        </v-row>
        <v-row>
            <v-col>
                <v-btn type="submit" color="primary">Add Loan</v-btn>
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
            minAmount: '',
            maxAmount: '',
            interestRate: '',
            duration: '',
        };
    },
    methods: {
        addLoan() {
            const loan = {
                min_amount: this.minAmount,
                max_amount: this.maxAmount,
                interest_rate: this.interestRate,
                duration: this.duration,
            };

            // Make an API call to submit the loan
            axios
                .post('/loans/submit/', loan, {
                    headers: {
                        Authorization: `Token ${localStorage.getItem('token')}`,
                    },
                })
                .then(response => {
                    // Handle success response and update the loans list
                    this.loans.push(response.data);
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
            this.minAmount = '';
            this.maxAmount = '';
            this.interestRate = '';
            this.duration = '';
        },
    },
};
</script>
