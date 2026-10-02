<template>
  <template v-if="majors.length">
    <div
      v-for="majorData in majors"
      :key="majorData.credential_code"
      class="col"
    >
      <BCard class="rounded-3 h-100">
        <SHeading level="3" class="fw-bold h5">{{
          majorData.credential_title
        }}</SHeading>
        <div>{{ majorData.major_school }} - {{ majorData.major_campus }}</div>
        <div class="mb-3">
          <strong class="me-2">Admission Type:</strong>
          <MajorCapacityDisplay :admission-type="majorData.major_admission" />
        </div>
        <div class="text-end">
          <BLink
            :to="{ path: '/major', query: { id: majorData.credential_code } }"
            >Learn more about this major</BLink
          >
        </div>
      </BCard>
    </div>
  </template>
  <div v-else-if="showError" class="col">
    <BCard class="rounded-3 h-100">
      <p class="mb-0">
        Data is not available for major
        <strong>{{ majorAbbrCode }}</strong
        >.
      </p>
    </BCard>
  </div>
  <div v-else-if="loading" class="col">
    <BCard class="rounded-3 h-100">
      <div class="text-center">
        <div class="spinner-border" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
      </div>
    </BCard>
  </div>
</template>

<script>
  import { BCard, BLink } from "bootstrap-vue-next";
  import { SHeading } from "solstice-vue";
  import MajorCapacityDisplay from "@/components/major/capacity-display.vue";
  import { useCustomFetch } from "@/composables/customFetch";

  export default {
    name: "MajorMini",
    components: {
      BCard,
      SHeading,
      BLink,
      MajorCapacityDisplay,
    },
    props: {
      majorAbbrCode: {
        type: String,
        required: true,
      },
    },
    data() {
      return {
        majors: [],
        showError: false,
        loading: false,
      };
    },
    watch: {
      majorAbbrCode() {
        this.getMajorData();
      },
    },
    mounted() {
      this.getMajorData();
    },
    methods: {
      fetchMajor(code) {
        return useCustomFetch(
          "/api/v1/majors/details/" + encodeURIComponent(code),
        );
      },
      async getMajorData() {
        const code = this.majorAbbrCode?.trim();
        this.majors = [];
        this.showError = false;
        if (!code) {
          this.showError = true;
          return;
        }
        this.loading = true;
        try {
          const data = await this.fetchMajor(code);
          if (data.matches) {
            // Bare abbr codes (e.g. "ACMS") can map to multiple degrees;
            // fetch full details for each so every degree gets a card.
            const results = await Promise.allSettled(
              data.matches.map((m) => this.fetchMajor(m.credential_code)),
            );
            this.majors = results
              .filter((r) => r.status === "fulfilled" && r.value)
              .map((r) => r.value);
          } else {
            this.majors = [data];
          }
          if (!this.majors.length) this.showError = true;
        } catch {
          this.showError = true;
        } finally {
          this.loading = false;
        }
      },
    },
  };
</script>
