// home.vue
<template>
  <DefaultLayout :page-title="pageTitle">
    <!-- page content -->
    <template #content>
      <div class="row mt-5">
        <div class="col-md-8 col-12">
          <SearchMini class="d-md-none" />
          <SHeading level="1" class="fw-bold ff-encode-sans mb-5"
            >Welcome back,
            <template
              v-if="contextStore.context.personData.preferred_first_name"
            >
              {{ contextStore.context.personData.preferred_first_name }}
            </template>
            <template v-else>
              {{ contextStore.context.personData.uwnetid }}
            </template>
          </SHeading>
        </div>
        <div class="col-md-4 col-12">
          <SearchMini class="d-none d-md-block" />
        </div>
      </div>
      <div class="row">
        <div class="col">
          <BCard class="bg-body-tertiary rounded-3 mb-5" border-variant="0">
            <div class="row">
              <div class="col border-end px-4">
                <p class="fw-bold text-secondary">Major</p>
                <ul class="list-unstyled p-0">
                  <li class="d-flex justify-content-between">
                    <div>Major</div>
                    <div class="fs-5 fw-bold text-end">
                      <template
                        v-if="
                          !contextStore.context.personData.majors ||
                          contextStore.context.personData.majors.length === 0
                        "
                      >
                        <div>Pre-Major</div>
                      </template>
                      <template
                        v-for="(major, index) in contextStore.context.personData
                          .majors"
                        :key="index"
                      >
                        <div>{{ major.major_name }}</div>
                      </template>
                    </div>
                  </li>
                </ul>
              </div>
              <div class="col border-end px-4">
                <p class="fw-bold text-secondary">Satisfactory Progress</p>
                <ul class="list-unstyled p-0">
                  <li class="d-flex justify-content-between mb-2">
                    <div>Class Standing</div>
                    <div class="fs-5 fw-bold text-end">
                      {{ contextStore.context.personData.class_desc }}
                    </div>
                  </li>
                  <li class="d-flex justify-content-between">
                    <div>Credits</div>
                    <div>
                      {{ contextStore.context.personData.total_credits }} / 225
                    </div>
                  </li>
                  <li class="mb-2">
                    <div
                      class="progress"
                      role="progressbar"
                      aria-label="Basic example"
                      aria-valuenow="25"
                      aria-valuemin="0"
                      aria-valuemax="100"
                    >
                      <div class="progress-bar" style="width: 25%"></div>
                    </div>
                  </li>
                  <li class="d-flex justify-content-between">
                    <div>Quarters Completed</div>
                    <div>
                      {{ contextStore.context.personData.quarters_completed }} /
                      16 (4yr)
                    </div>
                  </li>
                  <li class="mb-2">
                    <div
                      class="progress"
                      role="progressbar"
                      aria-label="Basic example"
                      aria-valuenow="25"
                      aria-valuemin="0"
                      aria-valuemax="100"
                    >
                      <div class="progress-bar" style="width: 25%"></div>
                    </div>
                  </li>
                </ul>
              </div>
              <div class="col px-4">
                <p class="fw-bold text-secondary">Academics</p>
                <ul class="list-unstyled p-0">
                  <li class="d-flex justify-content-between">
                    <div>Cummulative GPA</div>
                    <div class="fs-5 fw-bold text-end">
                      {{ contextStore.context.personData.cumulative_gpa }}
                    </div>
                  </li>
                </ul>
              </div>
            </div>
          </BCard>
          <div>
            <pre>{{
              JSON.stringify(contextStore.context.personData, null, 2)
            }}</pre>
          </div>

          <!-- TODO: hide intended majors when majors exist -->
          <SHeading level="2" class="mb-3">My Intended Majors</SHeading>
          <div class="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-3 mb-5">
            <template
              v-if="
                (contextStore.context.personData.intended_majors || []).length
              "
            >
              <div
                v-for="(major, index) in contextStore.context.personData
                  .intended_majors || []"
                :key="index"
                class="col-4"
              >
                <div>
                  <pre>{{ JSON.stringify(major, null, 2) }}</pre>
                </div>

                <BCard class="rounded-3 mb-3"> asldkfjasdklfjasdfklj </BCard>
              </div>
            </template>
            <template v-else>
              <p>No intended majors found.</p>
            </template>
          </div>

          <SHeading level="2" class="mb-3">My Majors</SHeading>
          <div
            v-if="(contextStore.context.personData.majors || []).length"
            class="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-3 mb-5"
          >
            <template
              v-for="(major, index) in contextStore.context.personData.majors ||
              []"
              :key="index"
            >
              <MajorMini :major-abbr-code="major.major_abbr_code" />
            </template>
          </div>
          <p v-else class="mb-5">No majors found.</p>

          <SHeading level="2" class="mb-3">Test Display Majors</SHeading>
          <div class="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-3 mb-5">

            <MajorMini :major-abbr-code="'CSSE'" />
            <MajorMini :major-abbr-code="'COMP E'" />
            <MajorMini :major-abbr-code="'CMP E'" />
            <MajorMini :major-abbr-code="'ACMS'" />
            <MajorMini :major-abbr-code="'C SCI'" />
            <MajorMini :major-abbr-code="'AMATH'" />
            <MajorMini :major-abbr-code="'B CRS'" />

          </div>

        </div>
      </div>
    </template>
  </DefaultLayout>
</template>

<script>
  import DefaultLayout from "@/layouts/default.vue";
  import SearchMini from "@/components/search/search-mini.vue";
  import MajorMini from "@/components/common/major-mini.vue";
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
      MajorMini,
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
