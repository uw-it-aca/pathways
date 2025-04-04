<template>
  <div>
    <h2 class="h5 mb-3">Recent Searches</h2>
    <div v-if="recent_searches">
      <ul
        v-for="(search, index) in recent_searches"
        :key="index"
        class="list-unstyled"
      >
        <li>
          <a href="#" @click.prevent="setSearch(search)">{{ search }}</a>
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
  emits: ["setSearch"],
  data() {
    return {};
  },
  computed: {
    recent_searches() {
      let recent_searches = JSON.parse(localStorage.getItem("recentSearches"));
      return recent_searches;
    },
  },
  watch: {},
  methods: {
    setSearch(search_string) {
      this.$emit("setSearch", search_string);
    },
  },
};
</script>
