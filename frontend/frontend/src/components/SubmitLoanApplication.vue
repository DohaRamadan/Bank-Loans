<template>
<div>
    <ViewLoans></ViewLoans>
    <v-container class="submit-loan-container">
        <v-card class="submit-loan-card">
            <v-card-title class="submit-loan-title">Submit Loan Application</v-card-title>
            <v-card-text>
                <v-form @submit.prevent="submitLoanApplication">
                    <v-text-field v-model="loanId" label="Loan ID" required></v-text-field>
                    <v-text-field v-model="amount" label="Amount" required></v-text-field>
                    <v-btn type="submit" color="primary">Submit Loan Application</v-btn>
                </v-form>
            </v-card-text>
        </v-card>
    </v-container>
</div>
</template>

<script>
import axios from 'axios';
import ViewLoans from './ViewLoans.vue';
export default {
    data() {
        return {
            loanId: '',
            amount: ''
        };
    },
    components: {
        ViewLoans,
    },
    methods: {
        submitLoanApplication() {
            const loanApplication = {
                loan: this.loanId,
                amount: this.amount
            };

            axios
                .post('/loan-applications/submit/', loanApplication, {
                    headers: {
                        Authorization: `Token ${localStorage.getItem('token')}`
                    }
                })
                .then(() => {
                    this.$router.push('/loan-applications/view')
                })
                .catch(error => {
                    console.log(error)
                    let message = ""; 
                    if(error.response.data.error.customer){
                        message += "customer: "
                        message += error.response.data.error.customer[0] + "\n";
                    }
                    if (error.response.data.error.loan) {
                        message += "loan: "
                        message += error.response.data.error.loan[0] + "\n";
                    }
                    if (error.response.data.error.amount) {
                        message += "amount: "
                        message += error.response.data.error.amount[0] + "\n";
                    }
                    if(error.response.data.error.non_field_errors){
                        message += error.response.data.error.non_field_errors[0] + "\n";
                    }
                    this.$router.push({name:'ErrorPage',query: { errorMessage: message }})
                });

            // Clear the form fields
            this.loanId = '';
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
