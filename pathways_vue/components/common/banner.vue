// banner.vue

<template>
  <div
    v-if="show_coi"
    class="alert alert-warning alert-dismissible fade show text-center mb-0 pe-3"
  >
    <div class="container-xl text-start">
      <strong>Join us as research participants!</strong> Get $20 Husky Card
      credit by participating in a feedback session for our new DawgPath
      feature. Be the first to sign up and share your valuable insights with us!
      <a
        target="_blank"
        href="https://docs.google.com/forms/d/e/1FAIpQLSetsq9KtmiTV8JMj1QM9R62pdrTUwiPlTAHK8bt9sq59FzlDw/viewform"
      >
        Sign up for a feedback session.</a
      >
      <button
        type="button"
        class="btn btn-link btn-close"
        aria-label="Close"
        title="Dismiss alert"
        @click="dismiss"
      ></button>
    </div>
  </div>
</template>

<script>
export default {
  name: "BannerComp",
  data() {
    return { show_coi: false };
  },
  computed: {},
  mounted() {
    if (window.show_coi) {
      this.show_coi = false;
    }
  },
  methods: {
    dismiss: function () {
      this.saveModalPref();
      this.show_coi = false;
    },
    async saveModalPref() {
      try {
        await useCustomFetch("/api/v1/user_pref/", {
          method: "POST",
          body: JSON.stringify({
            viewed_coi_banner: true,
          }),
          headers: {
            "Content-Type": "application/json",
          },
        });
      } catch (error) {
        console.error("Failed to save modal preference:", error);
      }
    },
  },
};
</script>

<style lang="scss" scoped>
.alert {
  border-radius: 0;

  .round-sm {
    height: 18px;
    width: 18px;
    line-height: 18px;
    border-radius: 15px;
    font-size: 0.7em;

    .material-symbols-outlined {
      font-size: 0.8rem;
    }
  }
}
</style>
