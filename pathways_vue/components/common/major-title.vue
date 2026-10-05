<template>
  <template v-if="!majorAbbrCode || !majorAbbrCode.trim()">
    <div>Pre-Major</div>
  </template>
  <template v-else-if="titles.length">
    <div v-for="(title, index) in titles" :key="index">{{ title }}</div>
  </template>
  <div v-else-if="loading" class="spinner-border spinner-border-sm" role="status">
    <span class="visually-hidden">Loading...</span>
  </div>
  <div v-else-if="showError">{{ majorAbbrCode }}</div>
</template>

<script>
  import { useCustomFetch } from "@/composables/customFetch";

  export default {
    name: "MajorTitle",
    props: {
      majorAbbrCode: {
        type: String,
        default: "",
      },
    },
    data() {
      return {
        titles: [],
        showError: false,
        loading: false,
      };
    },
    watch: {
      majorAbbrCode() {
        this.getMajorTitles();
      },
    },
    mounted() {
      this.getMajorTitles();
    },
    methods: {
      fetchMajor(code) {
        return useCustomFetch(
          "/api/v1/majors/details/" + encodeURIComponent(code),
        );
      },
      async getMajorTitles() {
        const code = this.majorAbbrCode?.trim();
        this.titles = [];
        this.showError = false;
        if (!code) {
          // no abbr code means the student is a pre-major
          return;
        }
        this.loading = true;
        try {
          const data = await this.fetchMajor(code);
          if (data.matches) {
            // bare abbr codes (e.g. "ACMS") can map to multiple degrees,
            // so fetch each one to get its credential_title
            const results = await Promise.allSettled(
              data.matches.map((m) => this.fetchMajor(m.credential_code)),
            );
            this.titles = results
              .filter((r) => r.status === "fulfilled" && r.value)
              .map((r) => r.value.credential_title)
              .filter(Boolean);
          } else if (data.credential_title) {
            this.titles = [data.credential_title];
          }
          if (!this.titles.length) this.showError = true;
        } catch {
          this.showError = true;
        } finally {
          this.loading = false;
        }
      },
    },
  };
</script>
