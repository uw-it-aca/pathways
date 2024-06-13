<template>
  <div>
    <h2 class="h5 mb-3">Recently Viewed</h2>
    <div v-if="recent_views">
      <ul v-for="view in recent_views" class="list-unstyled">
        <li>
          <a v-bind:href="view.url" class="recent_view_link"
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
a.recent_view_link {
  text-transform: capitalize;
}
</style>
