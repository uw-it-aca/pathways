// home.vue
<template>
  <DefaultLayout :page-title="pageTitle">
    <!-- page content -->
    <template #content>
      <div class="row mt-5">
        <div class="col-md-8 col-12">
          <SearchMini class="d-md-none" />
          <SHeading level="1" class="fw-bold ff-encode-sans mb-3"
            >Welcome back,
            {{ contextStore.context.personData.preferred_first_name }}</SHeading
          >
        </div>
        <div class="col-md-4 col-12">
          <SearchMini class="d-none d-md-block" />
        </div>
      </div>
      <div class="row">
        <div class="col">
          <BCard class="bg-body-tertiary rounded-3 mb-5" border-variant="0">
            <pre>{{
              JSON.stringify(contextStore.context.personData, null, 2)
            }}</pre>
          </BCard>

          <SHeading level="2" class="mb-3">My Intended Majors</SHeading>
          <div class="row mb-5">
            <div
              v-for="(major, index) in contextStore.context.personData
                .intended_majors"
              :key="index"
              class="col-4"
            >
              <BCard class="rounded-3 mb-3">
                <pre>{{ JSON.stringify(major, null, 2) }}</pre>
              </BCard>
            </div>
          </div>

          <SHeading level="2" class="mb-3">My Majors</SHeading>
          <div class="row mb-5">
            <div
              v-for="(major, index) in contextStore.context.personData.majors"
              :key="index"
              class="col-4"
            >
              <BCard class="rounded-3 mb-3">
                <pre>{{ JSON.stringify(major, null, 2) }}</pre>
              </BCard>
              <BCard class="rounded-3 mb-3">
                <SHeading level="3" class="fw-bold h4"
                  >major.credential_title</SHeading
                >
                <div>major["major_school"] - major["major_campus"]</div>
                <div>
                  <strong class="me-2">Admission Type:</strong
                  ><MajorCapacityDisplay :admission-type="'capacity-constrained'" /> major.major_admission
                </div>
                <div>
                  <BLink :to="'/major?id=INFO-0-1-6'">INFO-0-1-6</BLink>
                </div>
              </BCard>
            </div>
          </div>
        </div>
      </div>
    </template>
  </DefaultLayout>
</template>

<script>
  import DefaultLayout from "@/layouts/default.vue";
  import SearchMini from "@/components/search/search-mini.vue";
  import MajorCapacityDisplay from "@/components/major/capacity-display.vue";
  import { useCustomFetch } from "@/composables/customFetch";
  import { BCard, BLink } from "bootstrap-vue-next";
  import { SHeading } from "solstice-vue";
  import { useContextStore } from "@/stores/context";

  export default {
    name: "HomeComp",
    components: {
      BCard,
      BLink,
      DefaultLayout,
      MajorCapacityDisplay,
      SearchMini,
      SHeading,
    },
    data() {
      return {
        welcomeModal: null,
      };
    },
    computed: {
      contextStore() {
        return useContextStore();
      },
      pageTitle() {
        return this.contextStore.context.personData.display_name;
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
