// course-details.vue

<template>
  <div class="mb-5">
    <h2>{{ course.title }}</h2>
    <div><strong>Credits:</strong> {{ course.credits }}</div>
    <div class="mb-2">
      <strong>Offered</strong>
      <ul class="ms-2 d-inline list-inline">
        <li class="list-inline-item" v-for="(term, i) in course.offered" :key="i">
          <span class="badge text-dark" :class="term.class">{{ term.quarter }}</span>
        </li>
      </ul>
    </div>

    <p>
      {{ course.description }}
    </p>
  </div>
</template>

<script>
export default {
  name: 'CourseDetails',
  props: {
    course: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {};
  },
  methods: {},
};
</script>

<style lang="scss" scoped>
@import '../../css/custom.scss';

.creamcicle {
  background-color: $orange-200;
}
</style>
