<template>
  <div>
    <h2 class="h5 mb-3">Recent Searches</h2>
    <div v-if="recent_searches">
      <ul class="list-unstyled mb-3">
        <li v-for="search in recent_searches" class="mb-2">
          <a
            :href="`/search?q=${encodeURIComponent(search)}`"
            data-clarity-unmask="true"
            class="text-wrap"
            >{{ preventWidow(search) }}</a
          >
        </li>
      </ul>
    </div>
    <div v-else>No recent searches</div>
  </div>
</template>
<script>
  import { preventWidow } from "@/utils";

  export default {
    name: "RecentSearches",
    computed: {
      recent_searches() {
        return JSON.parse(localStorage.getItem("recentSearches"));
      },
    },
    methods: {
      preventWidow,
    },
  };
</script>

<style scoped>
  li:last-child {
    margin-bottom: 0 !important;
  }

  a {
    word-break: break-word;
  }
</style>
