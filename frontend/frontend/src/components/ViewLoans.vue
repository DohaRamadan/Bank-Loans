<template>
<div>
    <!-- List All Loans -->
    <h1 class="display-1">Loans</h1>
    <v-container>
        <v-row>
            <v-col cols="12" md="6" lg="4" v-for="loan in loans" :key="loan.id">
                <v-card outlined class="mb-4">
                    <v-card-title>{{ loan.title }}</v-card-title>
                    <v-card-text>
                        <v-list>
                            <v-list-item>
                                <v-list-item-content>ID: </v-list-item-content>
                                <v-list-item-content>{{ loan.id }}</v-list-item-content>
                            </v-list-item>
                            <v-list-item>
                                <v-list-item-content>Minimum Amount: </v-list-item-content>
                                <v-list-item-content>{{ loan.min_amount }}</v-list-item-content>
                            </v-list-item>
                            <v-list-item>
                                <v-list-item-content>Maximum Amount: </v-list-item-content>
                                <v-list-item-content>{{ loan.max_amount }}</v-list-item-content>
                            </v-list-item>
                            <v-list-item>
                                <v-list-item-content>Interest Rate: </v-list-item-content>
                                <v-list-item-content>{{ loan.interest_rate }}</v-list-item-content>
                            </v-list-item>
                            <v-list-item>
                                <v-list-item-content>Duration: </v-list-item-content>
                                <v-list-item-content>{{ loan.duration }}</v-list-item-content>
                            </v-list-item>
                        </v-list>
                    </v-card-text>
                </v-card>
            </v-col>
        </v-row>
    </v-container>
</div>
</template>

<script>
import axios from 'axios';
export default {
    data() {
        return {
            loans: [],
            drawer: true
        };
    },
    methods: {
        fetchLoans() {
            axios
                .get('/loans/view/', {
                    headers: {
                        Authorization: `Token ${localStorage.getItem('token')}`,
                    },
                })
                .then(response => {
                    this.loans = response.data;
                })
                .catch(error => {
                    let message = error.response.data.error
                    this.$router.push({name:'ErrorPage',query: { errorMessage: message }})
                });
        },
    },
    mounted() {
        // Fetch loans when the component is mounted
        this.fetchLoans();
    },
};
</script>
