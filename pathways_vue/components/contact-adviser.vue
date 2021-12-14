<template>
  <div class="card mb-5">
    <div class="card-body">
      <h3>Are you considering this {{type}}?</h3>
      <p>
        We understand this can be a challenging process with many sources of information to
        consider. This webpage is designed to be a useful tool but not a replacement for meeting
        with an academic adviser. As you begin to consider what you want to major in, we recommend
        scheduling a meeting with your adviser to discuss your interests, goals, degree requirements
        and academic planning.
      </p>
      <ul>
        <li v-for="info in advisingInfo" :key="info.url">
          <a :href="info.url">{{info.label}}</a>
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
          {"label": "UW, Tacoma advising",
           "url": "https://www.washington.edu/uaa/advising/"}]
      } else if (this.campus == "seattle") {
        return [
          {"label": "UW, Seattle premajor",
           "url": "https://www.washington.edu/uaa/advising/appointments/"},
          {"label": "UW, Seattle premajor OMAD",
           "url": "http://depts.washington.edu/omadcs/location/"},
          {"label": "UW, Seattle declared",
           "url": "http://www.washington.edu/uaa/advising/degree-overview/" +
                  "majors/advising-offices-by-program"}]
      } else if (this.campus == "bothell") {
        return [
          {"label": "UW, Bothell advising",
           "url": "https://uwb.campus.eab.com/"}]
      }
    }
  },
  methods: {},
};
</script>

<style lang="scss" scoped></style>