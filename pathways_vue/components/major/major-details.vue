// major-details.vue

<template>
  <div class="mb-5">
    <h1 class="h2 axdd-font-encode-sans fw-bold"> {{ major["credential_title"] }}</h1>
    <p class="text-uppercase mb-1">{{ major["major_school"] }} - {{ major["major_campus"] }}</p>
    <p><strong>Admission Policy:</strong> <a href="/faq#admission_types" class="router-link-active text-capitalize" title="Admission to majors">{{ AdminReqs }}</a></p>
    <div class="major-info">
      <div class="major-description">
        <p v-html="major['credential_description']" />
      </div>
    </div>
  </div>
</template>


<script>
export default {
  name: 'MajorDetails',
  props: {
    major: {
      type: Object,
      required: true,
    }
  },
  data() {
    return {};
  },
  methods: {},
  computed: {
    AdminReqs() {
      if(this.major["major_admission"] === "minimumRequirements"){
        return "Minimum Requirements"
      } else {
        return this.major["major_admission"]
      }
    },
  },
};
</script>

<style lang="scss"></style>
