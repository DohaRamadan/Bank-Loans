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
    setup() {},
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
                        const token = response.data.key;
                        this.$store.commit('setToken', token);
                        axios.defaults.headers.common['Authorization'] = "Token " + token;
                        localStorage.setItem('token', token);

                        axios.get('/get-user-role/')
                            .then(roleResponse => {
                                const role = roleResponse.data.role;
                                this.role = role;
                                localStorage.setItem('role', role.split(" ").join(""));
                                console.log(localStorage.getItem('role'));

                                // Redirect the user
                                if (role === "Loan Customer") {
                                    this.$router.push('/loan-applications/view').then(() => {
                                        this.$router.go()
                                    })
                                } else if (role === 'Loan Provider') {
                                    this.$router.push('/loan-fund-applications/view').then(() => {
                                        this.$router.go()
                                    })
                                } else if (role === 'Bank Personnel') {
                                    this.$router.push('/loans/view').then(() => {
                                        this.$router.go()
                                    })
                                }
                            })
                            .catch(error => {
                                this.handleRequestError(error)
                            });
                    }
                })
                .catch(error => {
                    this.handleRequestError(error)
                });
        },
        handleRequestError(error) {
            let message = error.response && error.response.data.non_field_errors ? error.response.data.non_field_errors[0] : '';
            console.log(message);
            this.$router.push({name:'ErrorPage',query: { errorMessage: message }})
        },
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
