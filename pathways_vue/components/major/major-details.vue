// major-details.vue

<template>
  <div class="mb-5">
    <h2> {{ major["major_title"] }}</h2>
    <p class="text-uppercase mb-1">{{ major["major_school"] }} - {{ major["major_campus"] }}</p>
    <p><strong>Admission Policy:</strong> {{ major["major_admission"] }}</p>
    <div class="major-info">
      <div class="major-description">
        <p v-html="major['major_description']" />
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
