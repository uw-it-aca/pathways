<template>
  <div>
    <h2 class="h5 mb-3">Recent Searches</h2>
    <div v-if="recent_searches">
      <ul class="list-unstyled mb-3">
        <li v-for="search in recent_searches" class="mb-2">
          <a
            href="#"
            @click.prevent="setSearch(search)"
            data-clarity-unmask="true"
            >{{ search }}</a
          >
        </li>
      </ul>
    </div>
    <div v-else>No recent searches</div>
  </div>
</template>
<script>
  export default {
    name: "RecentSearches",
    components: {},
    props: {},
    data() {
      return {};
    },
    computed: {
      recent_searches() {
        let recent_searches = JSON.parse(
          localStorage.getItem("recentSearches"),
        );
        return recent_searches;
      },
    },
    watch: {},
    methods: {
      setSearch(search_string) {
        this.$router.push({ path: "/search", query: { q: search_string } });
      },
    },
  };
</script>

<style scoped>
  li:last-child {
    margin-bottom: 0 !important;
  }
</style>
