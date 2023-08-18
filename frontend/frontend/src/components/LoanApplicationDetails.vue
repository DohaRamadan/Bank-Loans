<template>
<div>
    <h1 class="display-1">Loan Application Details</h1>

    <v-card>
        <v-card-text>
            <v-list>
                <v-list-item>
                    <v-list-item-content class="headline">Loan ID: </v-list-item-content>
                    <v-list-item-content>{{ loanApplication.id }}</v-list-item-content>
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
            <v-select v-model="selectedStatus" :items="statusOptions" label="Loan Status" outlined dense></v-select>
            <v-btn color="primary" @click="updateLoanApplication">Update</v-btn>
        </v-card-text>
    </v-card>
</div>
</template>

<script>
import axios from 'axios';

export default {
    data() {
        return {
            loanApplication: {},
            selectedStatus: '',
            statusOptions: ['Pending', 'Approved', 'Rejected'],
        };
    },
    methods: {
        fetchLoanApplication() {
            const loanApplicationId = this.$route.params.loanApplicationId;

            // Make an API call to fetch the loan application by ID
            axios
                .get(`loan-applications/get/${loanApplicationId}`, {
                    headers: {
                        Authorization: `Token ${localStorage.getItem('token')}`,
                    },
                })
                .then(response => {
                    // Handle success response and update the loan application data
                    this.loanApplication = response.data;
                    this.selectedStatus = response.data.status;
                })
                .catch(error => {
                    let message = error.response.data.error
                    this.$router.push({name:'ErrorPage',query: { errorMessage: message }})
                });
        },
        updateLoanApplication() {
            const loanApplicationId = this.$route.params.loanApplicationId;

            axios
                .put(`/loan-applications/update/${loanApplicationId}/`, {
                    status: this.selectedStatus,
                }, {
                    headers: {
                        Authorization: `Token ${localStorage.getItem('token')}`,
                    },
                })
                .then(() => {
                    this.loanApplication.status = this.selectedStatus;
                    this.$router.push('/loan-applications/view')
                })
                .catch(error => {
                    let message = error.response.data.error
                    this.$router.push({name:'ErrorPage',query: { errorMessage: message }})
                });
        },
    },
    mounted() {
        // Fetch the loan application when the component is mounted
        this.fetchLoanApplication();
    },
};
</script>
