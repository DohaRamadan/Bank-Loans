<template>
<v-navigation-drawer app fixed permanent class="sidebar">
    <v-list dense>
        <v-list-item v-for="item in items" :key="item.title" :to="item.route" link>
            <v-list-item-icon>
                <v-icon>{{ item.icon }}</v-icon>
            </v-list-item-icon>
            <v-list-item-content>
                <v-list-item-title>{{ item.title }}</v-list-item-title>
            </v-list-item-content>
        </v-list-item>
        <v-list-item @click="logout">
            <v-list-item-icon>
                <v-icon>mdi-logout</v-icon>
            </v-list-item-icon>
            <v-list-item-content>
                <v-list-item-title>Logout</v-list-item-title>
            </v-list-item-content>
        </v-list-item>
    </v-list>
</v-navigation-drawer>
</template>

  
<script>
import axios from 'axios';
export default {
    data() {
        return {
            drawer: true,
            items: [{
                    title: 'Submit Loan Fund Application',
                    icon: 'mdi-file-document',
                    route: '/loan-fund-applications/submit'
                },
                {
                    title: 'View Loan Fund Applications',
                    icon: 'mdi-view-list',
                    route: '/loan-fund-applications/view'
                },
                //   { title: 'Logout', icon: 'mdi-logout', route: '/logout' },
            ],
        };
    },
    methods: {
        logout() {
            // Send request to '/logout/' API endpoint
            // After the request is successful, redirect the user to the 'signin/' route
            // Example:
            axios
                .post('/logout/')
                .then(() => {
                    localStorage.removeItem('token');
                    localStorage.removeItem('role');
                    this.$router.push('/').then(() => {
                        this.$router.go();
                    });
                })
                .catch((error) => {
                    console.error('Logout request failed', error);
                    const statusCode = error.response ? error.response.status : 500;
                    // Handle error response
                    this.$router.push({
                        name: 'ErrorPage',
                        params: {
                            code: statusCode,
                        },
                    });
                });
        },
    },
};
</script>

  
<style scoped>
.sidebar {
    background-color: #f0f0f0;
    box-shadow: 2px 0px 10px rgba(0, 0, 0, 0.1);
    width: 900px;

}

.sidebar .v-list-item {
    padding: 12px 24px;
}

.sidebar .v-list-item__content {
    margin-left: 20px;
    margin-top: 20px;
    margin-bottom: 20px;
}

.sidebar .v-list-item__title {
    font-size: 14px;
    font-weight: 500;
}

.sidebar .v-icon {
    font-size: 18px;
    margin-right: 12px;
}
</style>
