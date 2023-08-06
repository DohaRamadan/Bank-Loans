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

            axios
                .post('/loans/submit/', loan, {
                    headers: {
                        Authorization: `Token ${localStorage.getItem('token')}`,
                    },
                })
                .then(() => {
                    this.$router.push('/loans/view')
                })
                .catch(error => {
                    const statusCode = error.response ? error.response.status : 500;
                    // Handle error response
                    this.$router.push({
                        name: 'ErrorPage',
                        params: {
                            code: statusCode
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
