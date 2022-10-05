// banner.vue

<template>

    <div v-for="message in banner_messages" class="alert alert-info alert-dismissible fade show text-center mb-0">
      <p>{{message.content}}</p>
    </div>

</template>

<script>
export default {
    name: 'Banner',
    data() {
        return {
          banner_messages: undefined
        };
    },
    methods: {
      getBannerMessages(){
        let vue = this;
        this.axios
          .get('/api/v1/persistent_messages/')
          .then((response) => {
            vue.banner_messages = response.data;
          })
          .catch(function (error) {

          });
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
      this.getBannerMessages();
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
