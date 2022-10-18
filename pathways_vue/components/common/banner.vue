// banner.vue

<template>
  <div
    v-if="show_outcomes"
    class="alert alert-primary alert-dismissible fade show text-center mb-0"
  >
    <strong>New Feature!</strong> What have recent UW graduates done with their
    degree? Check out the "<strong>Career Outcomes</strong>" link, available for
    most majors.
    <button
      type="button"
      class="btn btn-link close"
      aria-label="Close"
      @click="dismissOutcomes"
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
    return { show_outcomes: false };
  },
  methods: {
    dismissOutcomes: function () {
      this.saveModalPref();
      this.show_outcomes = false;
    },
    saveModalPref() {
      this.axios({
        method: "post",
        url: "/api/v1/user_pref/",
        headers: { "X-CSRFToken": window.csrf_token },
        data: {
          viewed_outcomes_banner: true,
        },
      });
    },
  },
  computed: {},
  mounted() {
    if (window.show_outcomes) {
      this.show_outcomes = true;
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
