// home.vue
<template>
  <DefaultLayout :page-title="pageTitle">
    <!-- page content -->
    <template #content>
      <div class="row my-5">
        <div class="col-12 col-md-4"><SearchMini /></div>
        <div class="order-md-first col-12 col-md-8">
          <h1 class="my-3 my-md-0">{{ pageTitle }}</h1>
        </div>
      </div>
      <div class="row">
        <div class="col">jasdflkjlka sdflk jlkajsdflk;asjdf</div>
      </div>
    </template>
  </DefaultLayout>
</template>

<script>
  import DefaultLayout from "@/layouts/default.vue";
  import SearchMini from "@/components/search/search-mini.vue";
  import { useCustomFetch } from "@/composables/customFetch";

  export default {
    name: "HomeComp",
    components: {
      DefaultLayout,
      SearchMini,
    },
    data() {
      return {
        pageTitle: "Welcome back, Jack!",
        welcomeModal: null,
      };
    },
    mounted() {},
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
