<template>
  <!-- layout.vue: this is where you override the layout -->
  <STopbarNeo
    :app-name="appName"
    :app-root-url="appRootUrl"
    :page-title="pageTitle"
    :user-name="contextStore.context.login_user"
    :sign-out-url="contextStore.context.signout_url"
  >
    <template #settings>
      <!-- user comp here -->
      <SUser
        :user-netid="contextStore.context.login_user"
        :user-override="contextStore.context.override_user"
        :signout-url="contextStore.context.signout_url"
        :clear-override-url="'/'"
        data-clarity-mask="true"
      >
        Welcome back,
        <template v-if="contextStore.context.personData?.preferred_first_name">
          {{ contextStore.context.personData.preferred_first_name }}
        </template>
        <template v-else>
          {{ contextStore.context.personData?.uwnetid }}
        </template>
        <template #action>
          <a v-if="isOverriding" href="/support/" class="link-quiet-danger"
            ><i class="bi bi-x-circle me-2"></i>Clear override</a
          >
          <a
            v-else
            :href="contextStore.context.signout_url"
            class="link-quiet-danger"
            ><i class="bi bi-box-arrow-left me-2"></i>Sign out</a
          >
        </template>
      </SUser>
      <SColorMode color-class="text-white" class="ms-2" />
    </template>

    <template v-if="systemMessages.length" #system>
      <div class="row">
        <div class="col">
          <ul
            class="list-unstyled text-info-emphasis small m-0 py-2 text-center"
          >
            <li
              v-for="(message, index) in systemMessages"
              :key="index"
              class="mb-2"
              v-html="message"
            ></li>
          </ul>
        </div>
      </div>
    </template>

    <template #main>
      <div class="d-flex flex-column h-100 w-100">
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
        tagLine: "Discover your path to a degree",
      };
    },
    computed: {
      // true only when an override is set AND differs from the login user
      isOverriding() {
        const { override_user: overrideUser, login_user: loginUser } =
          this.contextStore.context;
        return !!overrideUser && overrideUser !== loginUser;
      },
      // get system messages from window.pathways.messages (django persistent messages)
      systemMessages() {
        return window.pathways?.messages || [];
      },
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
