<template>
  <div>
    <h2>Recent Views</h2>
    <ul v-for="view in recent_views">
      <li><a v-bind:href="view.url" class="recent_view_link">{{ view.title }} ({{view.campus}})</a></li>
    </ul>
  </div>
</template>
<script>

export default {
  name: 'RecentViews',
  components: {
  },
  props: {
  },
  data() {
    return {
    };
  },
  computed: {
    recent_views() {
      let recent_views = JSON.parse(localStorage.getItem('recentViews'));
      return recent_views;
    }
  },
  watch: {
  },
  methods: {
  },
};
</script>

<style lang="scss">
a.recent_view_link {
  text-transform: capitalize;
}
</style>
