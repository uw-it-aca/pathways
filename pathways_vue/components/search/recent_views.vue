<template>
  <div>
    <h2 class="h5 mb-3">Recently Viewed</h2>
    <div v-if="recent_views">
      <ul
        v-for="(view, index) in recent_views"
        :key="index"
        class="list-unstyled"
      >
        <li>
          <a :href="view.url" class="recent-view-link"
            >{{ view.title }}
            <div
              class="badge text-bg-light rounded-pill text-uppercase float-end"
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
  methods: {},
};
</script>

<style lang="scss">
a.recent-view-link {
  text-transform: capitalize;
}
</style>
