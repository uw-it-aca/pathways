<template>
  <div class="card mb-5 bg-light-beige border-0 p-3">
    <div class="card-body">
      <h2 class="h4">Are you considering this {{type}}?</h2>
      <p>
        We understand this can be a challenging process with many sources of information to
        consider. DawgPath is designed to be a useful tool but not a replacement for meeting
        with an academic adviser. As you begin to consider what you want to major in, we recommend
        scheduling a meeting with your adviser to discuss your interests, goals, degree requirements
        and academic planning.
      </p>
      <ul>
        <li class="list-unstyled" v-for="info in advisingInfo" :key="info.url">
          <a :href="info.url"><i class="bi bi-dot me-1"></i>{{info.label}}</a>
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ContactAdviserCourse',
  props: ['campus', 'type'],
  data() {
    return {};
  },
  computed: {
    advisingInfo: function () {
      if (this.campus == "tacoma") {
        return [
          {"label": "Find your Tacoma adviser",
           "url": "https://www.tacoma.uw.edu/gaa#permalink-37917"}]
      } else if (this.campus == "seattle") {
        return [
          {"label": "Find your premajor adviser",
           "url": "https://www.washington.edu/uaa/advising/appointments/"},
          {"label": "Find your Office of Minority Affairs & Diversity (OMA&D) adviser",
           "url": "https://depts.washington.edu/omadcs/location/"},
          {"label": "Find your departmental or major adviser",
           "url": "https://www.washington.edu/uaa/advising/degree-overview/" +
                  "majors/advising-offices-by-program"}]
      } else if (this.campus == "bothell") {
        return [
          {"label": "Find your Bothell adviser",
           "url": "https://uwb.navigate.eab.com/"}]
      }
    }
  },
  methods: {},
};
</script>

<style lang="scss" scoped></style>
