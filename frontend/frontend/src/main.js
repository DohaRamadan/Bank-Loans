import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import vuetify from "./plugins/vuetify"; // Import the Vuetify instance
import axios from "axios";
import store from "./store";
import Toast from "vue-toastification";
import "vue-toastification/dist/index.css";

axios.defaults.baseURL = "http://localhost:8000";

const app = createApp(App);
app.use(store);
app.use(router, axios);
app.use(Toast);
app.use(vuetify); // Use the Vuetify instance


app.mount("#app");
