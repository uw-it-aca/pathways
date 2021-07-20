<template>
  <!-- layout.vue: this is where you override the layout -->
  <topbar
    :app-name="appName"
    :page-title="pageTitle"
    :user-name="userName"
    :sign-out-url="signOutUrl"
  >
    <template #header></template>
    <template #navigation>
      <!-- navigation menu override -->
      <ul class="nav flex-column">
        <li v-for="item in navItems" :key="item.title" class="nav-item mb-2">
          <a class="nav-link d-block px-2 py-1" :href="item.href">{{ item.title }}</a>
        </li>
      </ul>
    </template>
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
      <div class="text-white font-weight-light">
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
