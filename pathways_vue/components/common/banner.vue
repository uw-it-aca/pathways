// banner.vue

<template>

    <div class="alert alert-info alert-dismissible fade show text-center mb-0" v-if="show_outcomes">
        <strong>New Feature!</strong> DawgPath now shows which courses act as a gateway. Look for the gateway icon  <div class="round round-sm bg-success">
      <span class="material-symbols-outlined fw-bold">call_split</span>
    </div>  in course listings.  <a href="/faq#gateway" class="router-link">Learn more.</a>
        <button type="button" class="btn btn-link close" aria-label="Close" @click="dismissOutcomes">
            <span aria-hidden="true"><i class="bi bi-x-lg" title="Dismiss alert"></i></span>
        </button>
    </div>

</template>

<script>
export default {
    name: 'Banner',
    data() {
        return {show_outcomes: false};
    },
    methods: {
      dismissOutcomes: function (){
        this.saveModalPref();
        this.show_outcomes = false;
      },
      saveModalPref() {
        this.axios({
          method: 'post',
          url: '/api/v1/user_pref/',
          headers: { 'X-CSRFToken': window.csrf_token },
          data: {
            viewed_outcomes_banner: true,
          },
        });
      },
    },
    computed: {
    },
    mounted() {
      if (window.show_outcomes) {
        this.show_outcomes = true;
      }
    }
};
</script>

<style lang="scss" scoped>
.alert {
    border-radius: 0;
}
.alert {
  .round-sm {
    height: 18px;
    width: 18px;
    line-height: 18px;
    -moz-border-radius: 15px;
    border-radius: 15px;
    font-size: 0.7em;

    .material-symbols-outlined {
      font-size: 0.8rem;
    }
  }
}
</style>
