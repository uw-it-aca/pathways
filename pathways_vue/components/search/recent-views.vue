<template>
  <div>
    <h2 class="h5 mb-3">Recently Viewed</h2>
    <div v-if="recent_views">
      <ul class="list-unstyled m-0">
        <li v-for="view in recent_views" class="mb-2">
          <a
            :href="view.url"
            class="recent_view_link text-wrap d-flex align-items-start"
            data-clarity-unmask="true"
            ><span class="flex-grow-1">{{ preventWidow(view.title) }}</span>
            <div
              class="badge text-bg-light rounded-pill text-uppercase ms-2 flex-shrink-0"
            >
              {{ view.campus }}
            </div></a
          >
        </li>
      </ul>
    </div>
    <div v-else>No courses or majors recently viewed</div>
  </div>
</template>
<script>
  import { preventWidow } from "@/utils";

  export default {
    name: "RecentViews",
    components: {},
    props: {},
    data() {
      return {};
    },
    computed: {
      recent_views() {
        let recent_views = JSON.parse(localStorage.getItem("recentViews"));
        return recent_views;
      },
    },
    watch: {},
    methods: {
      preventWidow,
    },
  };
</script>

<style scoped>
  li:last-child {
    margin-bottom: 0 !important;
  }
</style>
