<template>
<div>
    <h1 class="display-1">Loan Applications</h1>

    <!-- List All Loan Applications -->
    <v-card v-for="loanApplication in loanApplications" :key="loanApplication.id" class="mb-4">
        <v-card-text>
            <v-list>
                <v-list-item>
                    <v-list-item-content class="headline">Loan ID: </v-list-item-content>
                    <v-list-item-content>{{ loanApplication.loan }}</v-list-item-content>
                </v-list-item>
                <v-list-item>
                    <v-list-item-content class="headline">Amount: </v-list-item-content>
                    <v-list-item-content>{{ loanApplication.amount }}</v-list-item-content>
                </v-list-item>
                <v-list-item>
                    <v-list-item-content class="headline">Status: </v-list-item-content>
                    <v-list-item-content>{{ loanApplication.status }}</v-list-item-content>
                </v-list-item>
                <v-list-item>
                    <v-list-item-content class="headline">Customer ID: </v-list-item-content>
                    <v-list-item-content>{{ loanApplication.customer }}</v-list-item-content>
                </v-list-item>
            </v-list>
            <v-btn v-if="isBankPersonnel" color="primary" @click="viewLoanApplication(loanApplication)">
                View Details
            </v-btn>
        </v-card-text>
    </v-card>
</div>
</template>

<script>
import axios from 'axios';

export default {
    data() {
        return {
            loanApplications: [],
            isBankPersonnel: false,
        };
    },
    methods: {
        fetchLoanApplications() {
            // Make an API call to fetch all loan applications
            axios
                .get('/loan-applications/view/', {
                    headers: {
                        Authorization: `Token ${localStorage.getItem('token')}`,
                    },
                })
                .then(response => {
                    // Handle success response and update the loan applications list
                    this.loanApplications = response.data;
                })
                .catch(error => {
                    // Handle error response
                    const statusCode = error.response ? error.response.status : 500;
                    // Handle error response
                    this.$router.push({
                        name: 'ErrorPage',
                        params: {
                            code: statusCode
                        }
                    });
                });
        },
        viewLoanApplication(loanApplication) {
            this.$router.push({
                name: 'LoanApplicationDetails',
                params: {
                    loanApplicationId: loanApplication.id
                }
            });
        },
    },
    mounted() {
        // Fetch loan applications when the component is mounted
        this.fetchLoanApplications();

        // Check if the user is a Bank Personnel
        const userType = localStorage.getItem('role');
        this.isBankPersonnel = userType === 'BankPersonnel';
    },
};
</script>
