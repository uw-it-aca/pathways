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
            <div class="flex-fill"><i class="bi bi-person-circle me-2"></i>{{ userName }}</div>
            <div class="flex-fill text-end">
              <a href="/faq" class="router-link text-white me-3 text-decoration-none"><i class="bi bi-question-circle me-2"></i>FAQ</a>
              <a :href="signOutUrl" class="text-white text-decoration-none"><i class="bi bi-box-arrow-right me-2"></i>Sign out</a>
            </div>
          </div>
        </div>
      </div>
      <div class="bg-purple axdd-topbar-brand">
        <div class="container-xl axdd-topbar-logo">
          <div
            class="d-inline align-middle text-white"
            :class="[$mq == 'desktop' ? 'h3' : 'h5']"
          >
            <a :href="appRootUrl" class="text-white text-decoration-none"><span class="visually-hidden">{{
              appName
            }}</span> <img src="/static/pathways/img/logo.png" class="logo" alt="Dawgpath logo with husky paw prints" /> <sub class="tagline text-white fst-italic" :class="[$mq == 'mobile' ? 'd-none' : 'display']">{{tagLine}}</sub></a>
          </div>
        </div>
      </div>
    </template>
    <template #main>
      <div class="bg-white mt-n3 mb-n5" style="min-height: 400px;">
        <!-- main section override -->
        <slot name="title">
          {{ pageTitle }}
        </slot>
        <slot name="content"></slot>
      </div>
    </template>
    <template #footer>
      <feedback />
      <!-- footer section override -->
       <div class="w-100 mt-auto pt-3 pb-3 small bg-gray-800">
        <div class="container-xl py-3">
          <ul class="list-inline mb-2">
            <li class="list-inline-item item-dot"><a href="mailto:help@uw.edu?subject=DawgPath Help, please route to Student and Instructor Success Analytics Service Offering" title="Contact the DawgPath team" class="text-white text-decoration-none me-2"><i class="bi bi-envelope-fill me-0"></i> Contact</a></li>
            <li class="list-inline-item item-dot"><a href="https://itconnect.uw.edu/learn/success-analytics/apps/#dawg" title="DawgPath Docs on IT Connect" class="text-white text-decoration-none me-2">Documentation</a></li>
            <li class="list-inline-item item-dot"><a href="https://www.washington.edu/online/terms/" title="UW Terms of Use" class="text-white text-decoration-none me-2">Terms</a></li>
            <li class="list-inline-item"><a href="https://www.washington.edu/online/privacy/" title="UW Privacy Policy" class="router-link text-white text-decoration-none me-2">Privacy</a></li>
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
import Feedback from "./components/common/feedback.vue";

export default {
  name: 'DawgPath',
  components: {
    'topbar': Topbar,
    'feedback': Feedback,
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
      userName: '',
      signOutUrl: '/saml/logout',
      tagLine: 'Discover your path to a degree',

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
  mounted() {
    this.userName = window.user;
  },
};
</script>

<style lang="scss">
.item-dot {
  &::after {
    content: '·';
    color: #fff;
  }
}
.axdd-topbar-brand {
  line-height: 65px;
}
.tagline {
    font-size: 0.45em;
    right: 0em;
    bottom: 0em;
}
.logo {
  max-width: 200px;
  padding:0.7rem;
}
</style>
