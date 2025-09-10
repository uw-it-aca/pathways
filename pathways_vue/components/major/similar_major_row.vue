<template>
  <div v-if="is_program">
    <div class="row my-2 py-2">
      <div class="col-11">
        <h6 class="fw-bold ff-open-sans mb-1">
          {{ majorData.program_title }}
        </h6>
        <p class="text-uppercase small text-black-50 mb-0">
          {{ majorData.program_school }} - {{ majorData.program_campus }}
        </p>
      </div>
      <div class="col-1 text-center" style="font-size: 18px">
        <a href="#" v-on:click.prevent="expandChildren" style="color: #2f68cb">
          <i :class="expand_icon"></i>
        </a>
      </div>
    </div>

    <div v-if="expanded">
      <div
        class="border-bottom border-light-subtle"
        style="margin-left: -1rem; margin-right: -1rem"
      ></div>
      <div v-for="(major, index) in majorData.program_majors" :key="index">
        <similar-major-display :majorData="major" style="margin-left: 40px" />
        <div
          v-if="index !== majorData.program_majors.length - 1"
          class="border-bottom border-light-subtle"
          style="margin-left: -1rem; margin-right: -1rem"
        ></div>
      </div>
    </div>
  </div>
  <div v-else>
    <similar-major-display :major-data="majorData" />
  </div>
  <!--  <h3><a :href="major_url">{{majorData.credential_title}}</a></h3>-->
  <!--  <p>{{majorData.major_school}} - {{majorData.campus}}</p>-->
  <!--  <major-capacity-display :admissionType="majorData.major_admission" />-->
</template>

<script>
import SimilarMajorDisplay from "./similar_major_display.vue";

export default {
  name: "SimilarMajorRow",
  components: {
    SimilarMajorDisplay,
  },
  props: {
    majorData: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      expanded: false,
    };
  },
  methods: {
    expandChildren() {
      this.expanded = !this.expanded;
    },
  },
  computed: {
    major_url() {
      return "/major?id=" + encodeURIComponent(this.majorData.id);
    },
    is_program() {
      return this.majorData.program_majors !== undefined;
    },
    expand_icon() {
      return this.expanded ? "bi-chevron-down" : "bi-chevron-right";
    },
  },
};
</script>
