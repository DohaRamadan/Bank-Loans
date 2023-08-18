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
            const loanFundApplication = {
                amount: this.amount
            };

            axios
                .post('/loan-fund-applications/submit/', loanFundApplication, {
                    headers: {
                        Authorization: `Token ${localStorage.getItem('token')}`
                    }
                })
                .then(() => {
                    this.$router.push('/loan-fund-applications/view')
                })
                .catch(error => {
                    console.log(error)
                    let message = ""
                    if (error.response.data.error.amount) {
                        message += error.response.data.error.amount[0]
                    }
                    if(error.response.data.error.non_field_errors){
                        message += error.response.data.error.non_field_errors[0] + "\n";
                    }
                    this.$router.push({name:'ErrorPage',query: { errorMessage: message }})

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
