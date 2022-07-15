// banner.vue

<template>

    <div class="alert alert-info alert-dismissible fade show text-center mb-0" v-if="show_bottleneck">
        <strong>New Feature!</strong> DawgPath now shows which courses act as a bottleneck or a gateway for easier
        registration planning. <a href="/faq#bottleneck" class="router-link">Learn more.</a>
        <button type="button" class="btn btn-link close" aria-label="Close" @click="dismissBottleneck">
            <span aria-hidden="true"><i class="bi bi-x-lg" title="Dismiss alert"></i></span>
        </button>
    </div>

</template>

<script>
export default {
    name: 'Banner',
    data() {
        return {show_bottleneck: false};
    },
    methods: {
      dismissBottleneck: function (){
        this.saveModalPref();
        this.show_bottleneck = false;
      },
      saveModalPref() {
        this.axios({
          method: 'post',
          url: '/api/v1/user_pref/',
          headers: { 'X-CSRFToken': window.csrf_token },
          data: {
            viewed_bottleneck_banner: true,
          },
        });
      },
    },
    computed: {
    },
    mounted() {
      if (window.show_bottleneck) {
        this.show_bottleneck = true;
      }
    }
};
</script>

<style lang="scss" scoped>
.alert {
    border-radius: 0;
}
</style>
