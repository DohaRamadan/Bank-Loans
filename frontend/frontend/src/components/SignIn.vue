<template>
<v-container class="signin-container">
    <v-card class="signin-card">
        <v-card-title class="signin-title">Sign In</v-card-title>
        <v-card-text>
            <v-form @submit="signin">
                <v-text-field v-model="username" label="Username" required></v-text-field>
                <v-text-field v-model="password" label="Password" type="password" required></v-text-field>
                <v-btn type="submit" color="primary">Sign In</v-btn>
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
            username: '',
            password: '',
        };
    },
    methods: {
        signin(event) {
            event.preventDefault();

            const data = {
                username: this.username,
                password: this.password
            };

            axios.post('/signin/', data)
                .then(response => {
                    console.log(response.data);
                    // Handle success response
                    if (response.data.key) {
                        // Save the token in the local storage
                        const token = response.data.key
                        this.$store.commit('setToken', token)
                        axios.defaults.headers.common['Authorization'] = "Token " + token
                        localStorage.setItem('token', token);
                        // Redirect the user to the main page
                        // this.$router.push('/dashboard');

                        axios.get('/get-user-role/')
                            .then(roleResponse => {
                                const role = roleResponse.data.role;
                                this.role = role;
                                localStorage.setItem('role', role.split(" ").join(""));
                                console.log(localStorage.getItem('role'));

                                // Redirect the user to the main page
                                if (role === "Loan Customer") {
                                    this.$router.push('loan-applications/view')
                                } else if (role === 'Loan Provider') {
                                    this.$router.push('loan-fund-applications/view')
                                } else if (role === 'Bank Personnel') {
                                    this.$router.push('loans/view')
                                }
                            })
                            .catch(error => {
                                console.error(error);
                                // Handle error response
                                this.$toast.error("Failed to retrieve user role.");
                            });
                    }
                })
                .catch(error => {
                    console.error(error.response.data);
                    // Handle error response
                    this.$toast.error(error.response.data.error);
                    this.$router.push({
                        name: 'error',
                        params: {
                            code: error.response.status
                        }
                    });
                });
        }
    }
};
</script>

<style scoped>
.signin-container {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
}

.signin-card {
    max-width: 400px;
    width: 100%;
    padding: 24px;
}

.signin-title {
    font-size: 24px;
    font-weight: bold;
    margin-bottom: 16px;
}
</style>
