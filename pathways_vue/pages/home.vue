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
            <p>
              Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aenean eu
              auctor nunc, ut malesuada risus. Proin hendrerit ac dolor eleifend
              fermentum. Vivamus commodo sed nisi vitae vestibulum. Praesent
              facilisis ac est sit amet vulputate. Cras sollicitudin ornare
              sapien a molestie. Donec nunc mauris, interdum quis scelerisque
              et, lobortis quis odio. Curabitur ultricies quis augue at posuere.
              Proin pretium sed nulla sit amet feugiat. Nunc justo dolor,
              blandit ac lorem ac, tempus consectetur magna. Praesent eu tempus
              massa, eu commodo nisi. Pellentesque a nisi non metus finibus
              cursus. Vestibulum consectetur, lacus a ultrices mattis, libero
              lacus ornare nibh, et mollis dui massa non nulla. Cras rhoncus
              nibh id feugiat tristique. Duis quis maximus augue. Cras quis
              tincidunt libero.
            </p>
            <p>
              Maecenas placerat varius nulla at porta. Pellentesque leo mauris,
              egestas nec fringilla in, maximus eget lorem. Maecenas ultricies
              vitae libero porta iaculis. Nullam convallis est vel quam gravida
              suscipit. Integer mattis odio est, ut rhoncus neque malesuada vel.
              Nullam mollis posuere turpis. Pellentesque eu lacinia eros. Sed
              faucibus justo id libero iaculis, accumsan interdum turpis
              feugiat. Proin eu orci bibendum, mollis sapien at, laoreet risus.
              Ut id sapien vel enim commodo accumsan. Donec eget massa ut nibh
              dapibus vulputate. Ut non massa mollis erat sodales dapibus quis
              quis quam. In rutrum eu augue id semper. Donec sem augue, eleifend
              ac mi at, porttitor congue ipsum.
            </p>
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
