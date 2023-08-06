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
            items: [{
                    title: 'View Loans',
                    icon: 'mdi-view-list',
                    route: '/loans/view'
                },
                {
                    title: 'Add Loan',
                    icon: 'mdi-file-document',
                    route: '/loans/submit'
                },
                {
                    title: 'View Loan Application',
                    icon: 'mdi-view-list',
                    route: '/loan-applications/view'
                },
                {
                    title: 'View Loan Fund Applications',
                    icon: 'mdi-view-list',
                    route: '/loan-fund-applications/view'
                }
            ]
        };
    },
    methods: {
        logout() {
            // Send request to '/logout/' API endpoint
            // After the request is successful, redirect the user to the 'signin/' route
            // Example:
            axios.post('/logout/')
              .then(() => {
                localStorage.removeItem('token')
                localStorage.removeItem('role')
                // window.location.reload();
                this.$router.push('/')

              })
              .catch((error) => {
                console.error('Logout request failed', error);
              });
        }
    }
};
</script>

  
<style scoped>
.sidebar {
    background-color: #f0f0f0;
    box-shadow: 2px 0px 10px rgba(0, 0, 0, 0.1);
    width: 250px;
}

.sidebar .v-list-item {
    padding: 12px 24px;
}

.sidebar .v-list-item__content {
    margin-left: 20px;
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
