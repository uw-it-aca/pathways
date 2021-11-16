<template>
  <!-- layout.vue: this is where you override the layout -->
  <topbar
    :app-name="appName"
    :app-root-url="appRootUrl"
    :page-title="pageTitle"
    :user-name="userName"
    :sign-out-url="signOutUrl"
  >
    <template #header>
      <div class="bg-dark-purple text-white py-2 small">
        <div class="container-xl">
          <div class="d-flex">
            <div class="flex-fill">{{ userName }}</div>
            <div class="flex-fill text-end">
              <a :href="signOutUrl" class="text-white">Sign out</a>
            </div>
          </div>
        </div>
      </div>
      <div class="bg-purple axdd-topbar-brand">
        <div class="container-xl axdd-topbar-logo">
          <a
            v-if="$slots['navigation']"
            class="btn btn-link btn-sm d-lg-none p-0 border-0 text-white"
            data-bs-toggle="collapse"
            data-bs-target="#nav-collapse"
            role="button"
            aria-expanded="false"
            aria-controls="collapseExample"
            aria-label="Toggle Navigation Menu"
          >
            <font-awesome-layers class="fa-2x">
              <font-awesome-icon
                :icon="faSquare"
                transform="right-1"
                class="m-0"
              />
              <font-awesome-icon
                :icon="faBars"
                transform="shrink-8 right-1 "
                class="m-0"
              />
            </font-awesome-layers>
          </a>

          <div
            class="d-inline align-middle text-white"
            :class="[$mq == 'desktop' ? 'h3' : 'h5']"
          >
            <a :href="appRootUrl" class="text-white text-decoration-none">{{
              appName
            }}</a>
          </div>
        </div>
      </div>
    </template>
    <template #main>
      <!-- main section override -->
      <slot name="title">
        {{ pageTitle }}
      </slot>
      <slot name="content"></slot>
    </template>
    <template #footer>
      <!-- footer section override -->
       <div class="w-100 mt-auto pt-3 pb-3 small bg-gray-800">
        <div class="container-xl py-3">
          <ul class="list-inline mb-2">
            <li class="list-inline-item item-dot"><a href="mailto:help@uw.edu?subject=DawgPath Comment, Request, Suggestion" class="text-white text-decoration-none me-2"><i class="bi bi-envelope-fill me-0"></i> Contact</a></li>
            <li class="list-inline-item item-dot"><a href="#" title="See DawgPath on IT Connect" class="text-white text-decoration-none me-2">DawgPath Help</a></li>
            <li class="list-inline-item item-dot"><a href="https://www.washington.edu/online/terms/" class="text-white text-decoration-none me-2">Terms</a></li>
            <li class="list-inline-item"><a href="https://www.washington.edu/online/privacy/" class="router-link text-white text-decoration-none me-2">Privacy</a></li>
          </ul>
          <div class="font-weight-light" style="color:#aaa">
            &copy; {{ new Date().getFullYear() }} University of
          Washington
          </div>
        </div>
      </div>
    </template>
  </topbar>
</template>

<script>
import { Topbar } from 'axdd-components';

export default {
  name: 'DawgPath',
  components: {
    'topbar': Topbar,
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
      appName: 'DawgPath',
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

<style lang="scss">
@import './css/custom.scss';

.item-dot {
  &::after {
    content: '·';
    color: #fff;
  }
}

</style>
