// major-details.vue

<template>
  <div class="mb-5">
    <h2> {{ major["credential_title"] }}</h2>
    <p class="text-uppercase mb-1">{{ major["major_school"] }} - {{ major["major_campus"] }}</p>
    <p><strong>Admission Policy:</strong> <a href="https://admit.washington.edu/apply/admission-to-majors/" title="Admission to majors" target="_blank">{{ major["major_admission"] }}</a></p>
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
};
</script>

<style lang="scss"></style>
