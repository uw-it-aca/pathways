<template>
  <BCard class="bg-body-tertiary rounded-3" border-variant="0">
    <h2 class="h4 ff-encode-sans fw-bold">
      Are you considering this {{ type }}?
    </h2>
    <p>
      We understand this can be a challenging process with many sources of
      information to consider. DawgPath is designed to be a useful tool but not
      a replacement for meeting with an academic adviser. As you begin to
      consider what you want to major in, we recommend scheduling a meeting with
      your adviser to discuss your interests, goals, degree requirements and
      academic planning.
    </p>
    <ul>
      <li v-for="info in advisingInfo" :key="info.url">
        <a :href="info.url">{{ info.label }}</a>
      </li>
    </ul>
  </BCard>
</template>

<script>
  import { BCard } from "bootstrap-vue-next";

  export default {
    name: "ContactAdviserCourse",
    props: ["campus", "type"],
    components: {
      BCard,
    },
    data() {
      return {};
    },
    computed: {
      advisingInfo: function () {
        let infoArray = [];
        if (this.campus.toLowerCase() == "tacoma") {
          infoArray = [
            {
              label: "Find your Tacoma adviser",
              url: "https://www.tacoma.uw.edu/gaa#permalink-37917",
            },
          ];
        } else if (this.campus.toLowerCase() == "seattle") {
          infoArray = [
            {
              label: "Find your premajor adviser",
              url: "https://www.washington.edu/uaa/advising/appointments/",
            },
            {
              label:
                "Find your Office of Minority Affairs & Diversity (OMA&D) adviser",
              url: "https://depts.washington.edu/omadcs/location/",
            },
            {
              label: "Find your departmental or major adviser",
              url:
                "https://advising.uw.edu/academic-support" +
                "/advising-offices-by-program/",
            },
          ];
        } else if (this.campus.toLowerCase() == "bothell") {
          infoArray = [
            {
              label: "Find your Bothell adviser",
              url: "https://uwb.navigate.eab.com/",
            },
          ];
        }
        return infoArray;
      },
    },
    methods: {},
  };
</script>
