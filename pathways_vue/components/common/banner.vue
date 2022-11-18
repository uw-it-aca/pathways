// banner.vue

<template>
  <div
    class="alert alert-info alert-dismissible fade show text-center mb-0"
    v-if="show_bottleneck"
  >
    <strong>New Feature!</strong> DawgPath now shows which courses act as a
    bottleneck. Look for the bottleneck icon
    <div class="round round-sm bg-danger">
      <span class="material-symbols-outlined fw-bold">call_merge</span>
    </div>
    in course listings.
    <a href="/faq#bottleneck" class="router-link">Learn more.</a>
    <button
      type="button"
      class="btn btn-link close"
      aria-label="Close"
      @click="dismiss"
    >
      <span aria-hidden="true"
        ><i class="bi bi-x-lg" title="Dismiss alert"></i
      ></span>
    </button>
  </div>
</template>

<script>
export default {
  name: "BannerComp",
  data() {
    return { show_bottleneck: false };
  },
  methods: {
    dismiss: function () {
      this.saveModalPref();
      this.show_bottleneck = false;
    },
    saveModalPref() {
      this.axios({
        method: "post",
        url: "/api/v1/user_pref/",
        headers: { "X-CSRFToken": window.csrf_token },
        data: {
          viewed_bottleneck_banner: true,
        },
      });
    },
  },
  computed: {},
  mounted() {
    if (window.show_bottleneck) {
      this.show_bottleneck = true;
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
