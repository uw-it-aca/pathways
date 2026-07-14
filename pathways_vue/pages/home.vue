// home.vue
<template>
  <DefaultLayout :page-title="pageTitle">
    <!-- page content -->
    <template #content>
      <div class="row mt-5">
        <div class="col-md-8 col-12">
          <SearchMini class="d-md-none" />
          <h1 class="my-md-0 my-3">{{ pageTitle }}</h1>
        </div>
        <div class="col-md-4 col-12">
          <SearchMini class="d-none d-md-block" />
        </div>
      </div>
      <div class="row">
        <div class="col">
          <BCard class="bg-body-tertiary rounded-3" border-variant="0">
            <pre>{{ JSON.stringify(contextStore.context.personData, null, 2) }}</pre>
          </BCard>
        </div>
      </div>
    </template>
  </DefaultLayout>
</template>

<script>
  import DefaultLayout from "@/layouts/default.vue";
  import SearchMini from "@/components/search/search-mini.vue";
  import { useCustomFetch } from "@/composables/customFetch";
  import { BCard } from "bootstrap-vue-next";
  import { useContextStore } from "@/stores/context";

  export default {
    name: "HomeComp",
    components: {
      BCard,
      DefaultLayout,
      SearchMini,
    },
    data() {
      return {
        pageTitle: "Welcome back, Jack!",
        welcomeModal: null,
      };
    },
    computed: {
      contextStore() {
        return useContextStore();
      },
    },
    mounted() {
      const contextStore = useContextStore();
      console.log("Context store data:", contextStore.context);
    },
    methods: {
      showWelcomeModal() {
        this.welcomeModal = new Modal(
          document.getElementById("exampleModal"),
          {},
        );
        this.welcomeModal.show();
      },
      async saveModalPref() {
        try {
          await useCustomFetch("/api/v1/user_pref/", {
            method: "POST",
            body: JSON.stringify({
              viewed_welcome_display: true,
            }),
            headers: {
              "Content-Type": "application/json",
            },
          });
        } catch (error) {
          console.error("Failed to save welcome display preference:", error);
        }
      },
    },
  };
</script>

<style lang="scss">
  .modal-body li {
    margin-bottom: 1em;
  }
</style>
