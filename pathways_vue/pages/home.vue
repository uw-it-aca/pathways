// home.vue
<template>
  <DefaultLayout :page-title="pageTitle">
    <!-- page content -->
    <template #content>
      <div class="row justify-content-center">
        <div class="col col-md-9">
          <h1 class="visually-hidden">{{ pageTitle }}</h1>
          <Search />
        </div>
      </div>
      <div class="row justify-content-center">
        <div class="col col-md-9">
          <p class="lead mb-5" style="max-width: 75ch">
            DawgPath helps you explore courses and majors and make strategic
            decisions about your schedule. It also provides useful data when
            you're planning for applying to capacity‑constrained majors.
          </p>

          <p>A few things to keep in mind before getting started:</p>

          <ul style="max-width: 80ch">
            <li class="mb-3">
              Grades are just one of the factors considered for
              capacity-constrained major. Reach out to your adviser to learn
              more.
            </li>
            <li class="mb-3">
              The median course grade and GPA data are only included for those
              who had declared for the major.
            </li>
            <li class="mb-3">
              Discovering and applying for a major can be a challenging
              experience. Look for the "Find your adviser” links to connect with
              your adviser.
            </li>
            <li>
              Check out the <a href="/faq">DawgPath FAQ</a> for more info.
            </li>
          </ul>
        </div>
      </div>
    </template>
  </DefaultLayout>
</template>

<script>
  import DefaultLayout from "@/layouts/default.vue";
  import Search from "@/components/search/search.vue";
  import { Modal } from "bootstrap";
  import { useCustomFetch } from "@/composables/customFetch";

  export default {
    name: "HomeComp",
    components: {
      DefaultLayout,
      Search,
    },
    data() {
      return {
        pageTitle: "Home",
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
