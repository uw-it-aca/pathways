<template>
  <!-- layout.vue: this is where you override the layout -->
  <STopbarNeo
    :app-name="appName"
    :app-root-url="appRootUrl"
    :page-title="pageTitle"
    :user-name="userName"
    :sign-out-url="signOutUrl"
  >
    <template #settings>
      <!-- profile section override -->
      <div class="d-flex">
        <div class="flex-fill text-white">
          <i class="bi bi-person-circle me-2"></i>{{ userName }}
        </div>
        <div class="flex-fill text-end">
          <a
            href="/faq"
            class="router-link text-white me-3 text-decoration-none"
            ><i class="bi bi-question-circle me-2"></i>FAQ</a
          >
          <a :href="signOutUrl" class="text-white text-decoration-none"
            ><i class="bi bi-box-arrow-right me-2"></i>Sign out</a
          >
        </div>
      </div>
    </template>

    <template #system>
      <Banner />
    </template>

    <template #main>
      <div class="" style="min-height: 400px">
        <!-- main section override -->
        <slot name="content"></slot>
      </div>
    </template>

    <template #footer>
      <!-- footer section override -->
      <!--<div class="bg-dark">
        <div class="container-xl">
          <div class="text-white font-weight-light py-3 small">
            <div class="d-flex justify-content-between">
              <ul class="list-inline mb-2">
                <li class="list-inline-item item-dot">
                  <a
                    href="mailto:help@uw.edu?subject=DawgPath Help, please route to Student and Instructor Success Analytics Service Offering"
                    title="Contact the DawgPath team"
                    class="text-white text-decoration-none me-2"
                    ><i class="bi bi-envelope-fill me-0"></i> Contact</a
                  >
                </li>
                <li class="list-inline-item item-dot">
                  <a
                    href="https://itconnect.uw.edu/tools-services-support/teaching-learning/research/success-analytics/apps/#dawg"
                    title="DawgPath Docs on IT Connect"
                    class="text-white text-decoration-none me-2"
                    >Documentation</a
                  >
                </li>
                <li class="list-inline-item item-dot">
                  <a
                    href="https://www.washington.edu/online/terms/"
                    title="UW Terms of Use"
                    class="text-white text-decoration-none me-2"
                    >Terms</a
                  >
                </li>
                <li class="list-inline-item">
                  <a
                    href="https://www.washington.edu/online/privacy/"
                    title="UW Privacy Policy"
                    class="router-link text-white text-decoration-none me-2"
                    >Privacy</a
                  >
                </li>
              </ul>
              <Feedback />
            </div>

            <div class="font-weight-light" style="color: #aaa">
              &copy; {{ new Date().getFullYear() }} University of Washington
            </div>
          </div>
        </div>
      </div>-->
    </template>
  </STopbarNeo>
</template>

<script>
import Feedback from "@/components/common/feedback.vue";
import Banner from "@/components/common/banner.vue";
import { STopbarNeo } from "solstice-vue";

export default {
  name: "DawgPath",
  components: {
    Feedback,
    Banner,
    STopbarNeo,
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
      appName: "DawgPath",
      appRootUrl: "/",
      userName: "",
      signOutUrl: "/saml/logout",
      tagLine: "Discover your path to a degree",
    };
  },
  mounted() {
    this.userName = window.user;
  },
  created: function () {
    // constructs page title in the following format "Page Title - AppName"
    document.title = this.pageTitle + " - " + this.appName;
  },
};
</script>

<style lang="scss">
.item-dot {
  &::after {
    content: "·";
    color: #fff;
  }
}

.tagline {
  font-size: 0.45em;
  right: 0;
  bottom: 0;
}

.logo {
  max-width: 200px;
  padding: 0.7rem;
}
</style>
