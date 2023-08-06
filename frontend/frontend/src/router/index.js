import { createRouter, createWebHistory } from 'vue-router';

// Import your components
import ViewLoanApplications from '@/components/ViewLoanApplications.vue'
import ViewLoanFundApplications from '@/components/ViewLoanFundApplications.vue'
// import ViewLoanPayments from '@/components/ViewLoanPayments.vue'
import ViewLoans from '@/components/ViewLoans.vue'
import SubmitLoanApplication from '@/components/SubmitLoanApplication.vue'
import SubmitLoanFundApplication from '@/components/SubmitLoanFundApplication.vue'
import MakeLoanPayment from '@/components/MakeLoanPayment.vue'
import SignIn from '@/components/SignIn.vue'
import SignUp from '@/components/SignUp.vue'
import AddLoan from '@/components/AddLoan.vue'
import Welcome from '@/components/Welcome.vue'
import LoanApplicationDetails from '@/components/LoanApplicationDetails.vue'
import LoanFundApplicationDetails from '@/components/LoanFundApplicationDetails.vue'
const routes = [
  {
    path: '/',
    component: () => import('@/layouts/default/Default.vue'),
    children: [
      {
        path: '/',
        name: 'Welcome',
        component: Welcome,
      },
      {
        path: '/loan-applications/:loanApplicationId',
        name: 'LoanApplicationDetails',
        component: LoanApplicationDetails,
      },
      {
        path: '/loan-fund-applications/:loanFundApplicationId',
        name: 'LoanFundApplicationDetails',
        component: LoanFundApplicationDetails,
      },
      {
        path: '/loans/view',
        name: 'ViewLoans',
        component: ViewLoans,
      },
      {
        path: '/loan-fund-applications/view',
        name: 'ViewLoanFundApplications',
        component: ViewLoanFundApplications,
      },
      {
        path: '/loan-applications/view',
        name: 'ViewLoanApplications',
        component: ViewLoanApplications,
      },
      {
        path: '/loans/submit',
        name: 'AddLoan',
        component: AddLoan,
      },
      {
        path: '/loan-fund-applications/submit',
        name: 'SubmitLoanFundApplication',
        component: SubmitLoanFundApplication,
      },
      {
        path: '/loan-applications/submit',
        name: 'SubmitLoanApplication',
        component: SubmitLoanApplication,
      },
      {
        path: '/loans/make-payment',
        name: 'MakeLoanPayment',
        component: MakeLoanPayment,
      },
      {
        path: '/signin',
        name: 'Signin',
        component: SignIn,
      },
      {
        path: '/signup',
        name: 'Signup',
        component: SignUp,
      },
    ],
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;