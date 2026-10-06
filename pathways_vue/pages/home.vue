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
                <p class="fw-bold text-body-secondary">Degree Information</p>
                <ul class="list-unstyled p-0">
                  <li class="d-flex justify-content-between">
                    <div>{{ majorCount > 1 ? "Majors" : "Major" }}</div>
                    <div class="fs-5 fw-bold text-end">
                      <div v-if="!hasMajors">Pre-Major</div>
                      <MajorTitle
                        v-for="(major, index) in majors"
                        :key="index"
                        :major-abbr-code="major.major_abbr_code"
                      />
                    </div>
                  </li>
                </ul>
              </div>
              <div class="col border-end px-4">
                <p class="fw-bold text-body-secondary">Progress</p>
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
                      {{ contextStore.context.personData.total_credits }} /
                      {{ creditsRequired }}
                    </div>
                  </li>
                  <li class="mb-2">
                    <BProgress
                      :value="creditsPercent"
                      aria-label="Credits completed"
                    />
                  </li>
                  <li class="d-flex justify-content-between">
                    <div>Quarters Completed</div>
                    <div>
                      {{ contextStore.context.personData.quarters_completed }} /
                      {{ quartersRequired }} (4yr)
                    </div>
                  </li>
                  <li class="mb-2">
                    <BProgress
                      :value="quartersPercent"
                      aria-label="Quarters completed"
                    />
                  </li>
                </ul>
              </div>
              <div class="col px-4">
                <p class="fw-bold text-body-secondary">Academics</p>
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
          <template v-if="contextStore.context.debugMode">
            <div>
              <pre>{{
                JSON.stringify(contextStore.context.personData, null, 2)
              }}</pre>
            </div>
          </template>

          <!-- show declared majors and intended majors as separate
               sections; a student may have both at the same time -->
          <SHeading level="2" class="mb-3">{{ majorsHeading }}</SHeading>
          <div
            v-if="hasMajors"
            class="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-3 mb-5"
          >
            <MajorMini
              v-for="(major, index) in majors"
              :key="index"
              :major-abbr-code="major.major_abbr_code"
            />
          </div>
          <p v-else class="mb-5">No majors found.</p>

          <SHeading level="2" class="mb-3">{{
            intendedMajorsHeading
          }}</SHeading>
          <div
            v-if="hasIntendedMajors"
            class="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-3 mb-5"
          >
            <MajorMini
              v-for="(major, index) in intendedMajors"
              :key="index"
              :major-abbr-code="major.major_abbr_code"
            />
          </div>
          <p v-else class="mb-5">No intended majors found.</p>

          <template v-if="contextStore.context.debugMode">
            <SHeading level="2" class="mb-3">Test Display Majors</SHeading>
            <div class="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-3 mb-5">
              <MajorMini :major-abbr-code="'CSSE'" />
              <MajorMini :major-abbr-code="'COMP E'" />
              <MajorMini :major-abbr-code="'CMP E'" />
              <MajorMini :major-abbr-code="'ACMS'" />
              <MajorMini :major-abbr-code="'C SCI'" />
              <MajorMini :major-abbr-code="'AMATH'" />
              <MajorMini :major-abbr-code="'B CRS'" />
              <MajorMini :major-abbr-code="'PSOCS'" />
              <MajorMini :major-abbr-code="'PREARC'" />
              <MajorMini :major-abbr-code="'PRESCI'" />
            </div>
          </template>
        </div>
      </div>
    </template>
  </DefaultLayout>
</template>

<script>
  import DefaultLayout from "@/layouts/default.vue";
  import SearchMini from "@/components/search/search-mini.vue";
  import MajorMini from "@/components/common/major-mini.vue";
  import MajorTitle from "@/components/common/major-title.vue";
  import { useCustomFetch } from "@/composables/customFetch";
  import { BCard, BProgress } from "bootstrap-vue-next";
  import { SHeading } from "solstice-vue";
  import { useContextStore } from "@/stores/context";

  export default {
    name: "HomeComp",
    components: {
      BCard,
      BProgress,
      DefaultLayout,
      MajorMini,
      MajorTitle,
      SearchMini,
      SHeading,
    },
    data() {
      return {
        welcomeModal: null,
        // degree requirements used as the progress bar maximums
        creditsRequired: 225,
        quartersRequired: 16,
      };
    },
    computed: {
      contextStore() {
        return useContextStore();
      },
      majors() {
        return this.contextStore.context.personData.majors || [];
      },
      intendedMajors() {
        return this.contextStore.context.personData.intended_majors || [];
      },
      hasMajors() {
        return this.majors.length > 0;
      },
      hasIntendedMajors() {
        return this.intendedMajors.length > 0;
      },
      majorCount() {
        return this.majors.length;
      },
      majorsHeading() {
        return this.majorCount > 1 ? "My Majors" : "My Major";
      },
      intendedMajorsHeading() {
        return this.intendedMajors.length > 1
          ? "My Intended Majors"
          : "My Intended Major";
      },
      creditsPercent() {
        return this.toPercent(
          this.contextStore.context.personData.total_credits,
          this.creditsRequired,
        );
      },
      quartersPercent() {
        return this.toPercent(
          this.contextStore.context.personData.quarters_completed,
          this.quartersRequired,
        );
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
      // percentage of a maximum, clamped to 0-100 and safe for missing data
      toPercent(value, max) {
        const current = Number(value);
        if (!max || !Number.isFinite(current)) return 0;
        return Math.min(100, Math.max(0, (current / max) * 100));
      },
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
