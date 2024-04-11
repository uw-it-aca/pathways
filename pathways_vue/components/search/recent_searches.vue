<template>
  <div>
    <h2>Recent Searches</h2>
    <ul v-for="search in recent_searches">
      <li><a href="#" @click.prevent="setSearch(search)">{{search}}</a></li>
    </ul>
  </div>
</template>
<script>

export default {
  name: 'RecentSearches',
  components: {
  },
  props: {
  },
  data() {
    return {
    };
  },
  computed: {
    recent_searches() {
      let recent_searches = JSON.parse(localStorage.getItem('recentSearches'));
      return recent_searches;
    }
  },
  watch: {
  },
  methods: {
    setSearch(search_string) {
      this.$emit('setSearch', search_string);
    },
  }
};
</script>

<style lang="scss">

</style>
