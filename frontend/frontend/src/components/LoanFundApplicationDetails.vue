<template>
<div>
    <h1 class="display-1">Loan Fund Application Details</h1>

    <v-card>
        <v-card-text>
            <v-list>
                <v-list-item>
                    <v-list-item-content class="headline">ID: </v-list-item-content>
                    <v-list-item-content>{{ loanFundApplication.id }}</v-list-item-content>
                </v-list-item>
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
            <v-select v-model="selectedStatus" :items="statusOptions" label="Loan Status" outlined dense></v-select>
            <v-btn color="primary" @click="updateLoanFundApplication">Update</v-btn>
        </v-card-text>
    </v-card>
</div>
</template>

<script>
import axios from 'axios';

export default {
    data() {
        return {
            loanFundApplication: {},
            selectedStatus: '',
            statusOptions: ['Pending', 'Approved', 'Rejected'],
        };
    },
    methods: {
        fetchLoanApplication() {
            const loanFundApplicationId = this.$route.params.loanFundApplicationId;

            axios
                .get(`loan-fund-applications/get/${loanFundApplicationId}`, {
                    headers: {
                        Authorization: `Token ${localStorage.getItem('token')}`,
                    },
                })
                .then(response => {
                    this.loanFundApplication = response.data;
                    this.selectedStatus = response.data.status;
                })
                .catch(error => {
                    const statusCode = error.response ? error.response.status : 500;
                    this.$router.push({
                        name: 'ErrorPage',
                        params: {
                            code: statusCode
                        }
                    });
                });
        },
        updateLoanFundApplication() {
            const loanFundApplicationId = this.$route.params.loanFundApplicationId;

            axios
                .put(`/loan-fund-applications/update/${loanFundApplicationId}/`, {
                    status: this.selectedStatus,
                }, {
                    headers: {
                        Authorization: `Token ${localStorage.getItem('token')}`,
                    },
                })
                .then(() => {
                    this.$router.push('/loan-fund-applications/view')
                    this.loanFundApplication.status = this.selectedStatus;
                })
                .catch(error => {
                    const statusCode = error.response ? error.response.status : 500;
                    this.$router.push({
                        name: 'ErrorPage',
                        params: {
                            code: statusCode
                        }
                    });
                });
        },
    },
    mounted() {
        // Fetch the loan application when the component is mounted
        this.fetchLoanApplication();
    },
};
</script>
