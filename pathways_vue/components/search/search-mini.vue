<template>
  <div class="dropdown mb-3" @focusout="onFocusOut">
    <BInputGroup size="md">
      <BFormInput
        v-model="query"
        type="text"
        autocomplete="off"
        @focus="open = true"
        @keyup.enter="navigate"
        :aria-expanded="open.toString()"
      />
      <BButton variant="outline-primary" @click="navigate">Search</BButton>
    </BInputGroup>
    <div
      v-show="open"
      class="dropdown-menu show mt-1 w-100 p-3"
      style=""
      @mousedown.prevent
    >
      <RecentSearches />
      <RecentViews />
    </div>
  </div>
</template>

<script>
  import RecentSearches from "@/components/search/recent-searches.vue";
  import RecentViews from "@/components/search/recent-views.vue";

  import {
    BInputGroup,
    BInputGroupText,
    BFormInput,
    BButton,
  } from "bootstrap-vue-next";

  export default {
    components: {
      RecentSearches,
      RecentViews,
      BInputGroup,
      BInputGroupText,
      BFormInput,
      BButton,
    },
    data() {
      return {
        open: false,
        query: "",
      };
    },
    methods: {
      navigate() {
        if (this.query.trim()) {
          this.$router.push({
            path: "/search",
            query: { q: this.query.trim() },
          });
          this.open = false;
        }
      },
      onFocusOut(e) {
        if (!this.$el.contains(e.relatedTarget)) {
          this.open = false;
        }
      },
    },
  };
</script>
