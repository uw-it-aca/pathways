<template>
  <!-- layout.vue: this is where you override the layout -->
  <STopbarNeo
    :app-name="appName"
    :app-root-url="appRootUrl"
    :page-title="pageTitle"
    :user-name="contextStore.context.loginUser"
    :sign-out-url="signOutUrl"
  >
    <template #settings>
      <!-- user comp here -->
      <SUser :user-netid="contextStore.context.user" data-clarity-mask="true">
        Welcome back, {{ contextStore.context.user }}
        <template #action>
          <a :href="signOutUrl" class="link-quiet-danger"
            ><i class="bi bi-box-arrow-left me-2"></i>Sign out</a
          >
        </template>
      </SUser>
      <SColorMode color-class="text-white" class="ms-2" />
    </template>

    <template #system>
      <Banner />
    </template>

    <template #main>
      <div class="d-flex flex-column h-100 w-100 gap-3">
        <slot name="content"></slot>
        <div class="fixed-bottom m-2 text-end">
          <BButton
            href="https://forms.office.com/r/BwFCpA0RYZ"
            size="sm"
            role="link"
            target="_blank"
            ><i class="bi bi-chat-right-text-fill me-2"></i>Send us
            feedback</BButton
          >
        </div>
      </div>
    </template>

    <template #footer></template>
  </STopbarNeo>
</template>

<script>
  import Banner from "@/components/common/banner.vue";
  import { BButton } from "bootstrap-vue-next";
  import { STopbarNeo, SUser, SColorMode } from "solstice-vue";
  import { useContextStore } from "@/stores/context";

  export default {
    name: "DawgPath",
    components: {
      Banner,
      BButton,
      STopbarNeo,
      SUser,
      SColorMode,
    },
    props: {
      pageTitle: {
        type: String,
        required: true,
      },
    },
    setup() {
      const contextStore = useContextStore();
      return {
        contextStore,
      };
    },
    data() {
      return {
        // minimum application setup overrides
        appName: "DawgPath",
        appRootUrl: "/",
        signOutUrl: "/saml/logout",
        tagLine: "Discover your path to a degree",
      };
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
