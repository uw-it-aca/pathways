// major-details.vue 

<template>
  <div class="mb-5">
<<<<<<< HEAD
    <h2>Chemistry (BS)</h2>
    <p class="text-uppercase mb-1">College of Arts & Sciences - Seattle</p>
    <p><strong>Admission type:</strong> capacity-contrained <a href="#"><i class="bi bi-info-circle-fill"></i></a></p>
=======
    <h2> {{ major["Major"] }}</h2>
    <p class="text-uppercase mb-1">{{ major["college"] }} - {{ major["campus"] }}</p>
    <p><strong>Admission Policy:</strong> {{ major["Admission Policy"] }}</p>
>>>>>>> 66d1b22 (Implemented major search)
    <div class="major-info">
      <div class="major-description">
        <p v-html="major['Description']" />
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