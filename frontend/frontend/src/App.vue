<template>
<v-app>
    <v-main>
        <div v-if="userType === 'LoanCustomer'">
            <CustomerSideBar></CustomerSideBar>
        </div>
        <div v-if="userType === 'LoanProvider'">
            <ProviderSideBar></ProviderSideBar>
        </div>
        <div v-if="userType === 'BankPersonnel'">
            <BankPersonnelSideBar></BankPersonnelSideBar>
        </div>
        <v-container>
            <router-view></router-view>
        </v-container>
    </v-main>
</v-app>
</template>

<script>
import BankPersonnelSideBar from './components/Sidebar/BankPersonnelSideBar.vue';
import CustomerSideBar from './components/Sidebar/CustomerSideBar.vue';
import ProviderSideBar from './components/Sidebar/ProviderSideBar.vue';
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
export default {
    name: 'App',
    data() {
        return {
            userType: localStorage.getItem('role')
        };
    },
    components: {
        BankPersonnelSideBar,
        CustomerSideBar,
        ProviderSideBar, 
        components,
        directives
    },

};
</script>
