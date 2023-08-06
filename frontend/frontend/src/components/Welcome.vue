<template>
<v-container fluid>
    <v-row justify="center" align="center">
        <v-col cols="12" md="8" lg="6">
            <v-card elevation="3">
                <v-card-title class="text-center">
                    <h2 class="display-1">Welcome to Bank Loans!</h2>
                </v-card-title>
                <v-card-text>
                    <p class="text-center">Thank you for using our application. We're excited to have you on board!</p>
                    <p class="text-center">Please complete the setup process to get started.</p>
                </v-card-text>
                <v-card-actions class="justify-center">
                    <v-btn color="primary" @click="signUp">Sign Up</v-btn>
                </v-card-actions>
                <v-card-text>
                    <p class="text-center">Already Signed Up? Sign In!</p>
                    <v-card-actions class="justify-center">
                        <v-btn color="primary" @click="signIn">Sign In</v-btn>
                    </v-card-actions>
                </v-card-text>
            </v-card>
        </v-col>
    </v-row>
</v-container>
</template>

  
<script>
export default {
    methods: {
        signUp() {
            this.$router.push('signup/')
        },
        signIn() {
            this.$router.push('signin/')
        }
    }
};
</script>

  
<style scoped>
.text-center {
    text-align: center;
}
</style>
