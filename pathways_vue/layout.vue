<template>
  <!-- layout.vue: this is where you override the layout -->
  <topbar
    :app-name="appName"
    :app-root-url="appRootUrl"
    :page-title="pageTitle"
    :user-name="userName"
    :sign-out-url="signOutUrl"
  >
    <template #header></template>
    <template #main>
      <!-- main section override -->
      <h1>
        <slot name="title">
          {{ pageTitle }}
        </slot>
      </h1>
      <slot name="content"></slot>
    </template>
    <template #footer>
      <!-- footer section overrixe -->
      <div class="text-test font-weight-light">
        this is my custom footer<br />
        Copyright &copy; {{ new Date().getFullYear() }} University of Washington
      </div>
    </template>
  </topbar>
</template>

<script>
import { Topbar } from 'axdd-components';

export default {
  name: 'Pathways',
  components: {
    topbar: Topbar,
  },
  props: {
    pageTitle: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      // minimum application setup overrides
      appName: 'Pathways',
      appRootUrl: '/',
      userName: 'javerage',
      signOutUrl: '/signout',

      // automatically set year
      currentYear: new Date().getFullYear(),

      // example: dynamic navigation menu
      navItems: [
        {
          title: 'Home',
          href: '#',
        },
        {
          title: 'First',
          href: '#',
        },
        {
          title: 'Second',
          href: '#',
        },
        {
          title: 'Third',
          href: '#',
        },
      ],
    };
  },
};
</script>

<style lang="scss" scoped></style>
