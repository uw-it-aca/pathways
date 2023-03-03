// banner.vue

<template>
  <div
    v-if="show_coi"
    class="alert alert-warning alert-dismissible fade show text-center mb-0 pe-3"
  >
    <div class="container-xl text-start">
      <strong>New Feature!</strong> DawgPath has new data to help you plan a
      balanced schedule. Search for a Seattle course to get a walk through of
      the <strong>Course Outcome Index</strong>. Coming soon for Bothell and
      Tacoma.
      <a href="/faq#coi" class="router-link">Learn more.</a>
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
  methods: {
    dismiss: function () {
      this.saveModalPref();
      this.show_coi = false;
    },
    saveModalPref() {
      this.axios({
        method: "post",
        url: "/api/v1/user_pref/",
        headers: { "X-CSRFToken": window.csrf_token },
        data: {
          viewed_coi_banner: true,
        },
      });
    },
  },
  computed: {},
  mounted() {
    if (window.show_coi) {
      this.show_coi = true;
    }
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
