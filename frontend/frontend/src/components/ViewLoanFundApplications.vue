<template>
<div>
    <!-- List All Loan Fund Applications -->
    <h2 class="display-2">Loan Fund Applications</h2>
    <v-card v-for="loanFundApplication in loanFundApplications" :key="loanFundApplication.id" class="mb-4">
        <v-card-text>
            <v-list>
                <v-list-item>
                    <v-list-item-content class="headline">Amount: </v-list-item-content>
                    <v-list-item-content>{{ loanFundApplication.amount }}</v-list-item-content>
                </v-list-item>
                <v-list-item>
                    <v-list-item-content class="headline">Status: </v-list-item-content>
                    <v-list-item-content>{{ loanFundApplication.status }}</v-list-item-content>
                </v-list-item>
                <v-list-item>
                    <v-list-item-content class="headline">Customer ID: </v-list-item-content>
                    <v-list-item-content>{{ loanFundApplication.customer }}</v-list-item-content>
                </v-list-item>
            </v-list>
            <v-btn v-if="isBankPersonnel" color="primary" @click="viewLoanFundApplication(loanFundApplication)">
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
            loanFundApplications: [],
            isBankPersonnel: false,
        };
    },
    methods: {
        fetchLoanFundApplications() {
            // Make an API call to fetch all loan fund applications
            axios
                .get('/loan-fund-applications/view/', {
                    headers: {
                        Authorization: `Token ${localStorage.getItem('token')}`,
                    },
                })
                .then(response => {
                    // Handle success response and update the loan fund applications list
                    this.loanFundApplications = response.data;
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
        },
        viewLoanFundApplication(loanFundApplication) {
            // Redirect to the LoanApplicationDetails component with the selected loan application
            this.$router.push({
                name: 'LoanFundApplicationDetails',
                params: {
                    loanFundApplicationId: loanFundApplication.id
                }
            });
        },
    },

    mounted() {
        // Fetch loan fund applications when the component is mounted
        this.fetchLoanFundApplications();

        // Check if the user is a Bank Personnel
        const userType = localStorage.getItem('role');
        this.isBankPersonnel = userType === 'BankPersonnel';
    },
};
</script>
