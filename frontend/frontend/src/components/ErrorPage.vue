<template>
<v-container class="error-page" fluid>
    <v-row align="center" justify="center">
        <v-col cols="12" sm="8" md="6">
            <v-card outlined class="error-card">
                <v-card-title class="error-title">Error {{ code }}</v-card-title>
                <v-card-text class="error-message">An error occurred. Please try again later.</v-card-text>
                <v-card-actions>
                    <v-btn color="primary" outlined @click="$router.go(-1)">Go Back</v-btn>
                </v-card-actions>
            </v-card>
        </v-col>
    </v-row>
</v-container>
</template>

  
<script>
export default {
    props: ['code']
};
</script>

  
<style scoped>
.error-page {
    height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
}

.error-card {
    max-width: 400px;
    text-align: center;
    padding: 24px;
}

.error-title {
    font-size: 24px;
    font-weight: bold;
    margin-bottom: 16px;
}

.error-message {
    margin-bottom: 16px;
}
</style>
