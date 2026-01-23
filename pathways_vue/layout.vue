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
            class="router-link text-decoration-none me-3 text-white"
            ><i class="bi bi-question-circle me-2"></i>FAQ</a
          >
          <a :href="signOutUrl" class="text-decoration-none text-white"
            ><i class="bi bi-box-arrow-right me-2"></i>Sign out</a
          >
        </div>
      </div>
    </template>

    <template #system>
      <Banner />
    </template>

    <template #main>
      <div class="d-flex flex-column align-items-start h-100 w-100 gap-3">
        <slot name="content"></slot>
      </div>
      <Feedback />
    </template>

    <template #footer></template>
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
