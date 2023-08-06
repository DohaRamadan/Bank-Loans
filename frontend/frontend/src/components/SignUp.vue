<template>
<v-container class="signup-container">
    <v-card class="signup-card">
        <v-card-title class="signup-title">Sign Up</v-card-title>
        <v-card-text>
            <v-form @submit="signup">
                <v-text-field v-model="username" label="Username" required></v-text-field>
                <v-text-field v-model="email" label="Email" required></v-text-field>
                <v-text-field v-model="password" label="Password" type="password" required></v-text-field>
                <v-select v-model="role" :items="roleOptions" label="Role" required></v-select>
                <v-btn type="submit" color="primary">Sign Up</v-btn>
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
            role: '',
            email: '',
            roleOptions: ['Loan Customer', 'Loan Provider']
        };
    },
    methods: {
        signup(event) {
            event.preventDefault();

            const data = {
                username: this.username,
                password: this.password,
                role: this.role,
                email: this.email
            };

            axios.post('/signup/', data)
                .then(response => {
                    console.log(response.data);
                    // Handle success response
                    if (response.data.message) {
                        this.$router.push('/signin/').then(() => {
                            this.$router.go()
                        })
                    }
                })
                .catch(error => {
                    console.error(error.response.data);
                    const statusCode = error.response ? error.response.status : 500;
                    // Handle error response
                    this.$router.push({
                        name: 'ErrorPage',
                        params: {
                            code: statusCode
                        }
                    });
                });
        }
    }
};
</script>

<style scoped>
.signup-container {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
}

.signup-card {
    max-width: 400px;
    width: 100%;
    padding: 24px;
}

.signup-title {
    font-size: 24px;
    font-weight: bold;
    margin-bottom: 16px;
}
</style>
