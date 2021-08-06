//prereq-course-list.vue

<template>
  <div class="card mb-3">
    <div class="card-body">
      <h4>Prerequesites <span class="badge rounded-pill bg-secondary">1</span></h4>
      <div class="mt-3">
        <ul class="list-unstyled">
          <li>
            <a href="#" class="router-link-active"
              ><span class="badge bg-link-color text-light">CSS 415</span></a
            >
            <span class="ms-3">Preparation for General Chemistry</span>
          </li>
          <li>
            <a href="#" class="router-link-active"
              ><span class="badge bg-link-color text-light">MATH 124</span></a
            >
            <span class="ms-3">Calculus with Analytic Geometry I</span>
          </li>
        </ul>
      </div>
    </div>
  </div>
  <div class="card mb-3">
    <div class="card-body">
      <h4>
        Courses Available Upon Completion <span class="badge rounded-pill bg-secondary">26</span>
      </h4>
      <p>list here</p>
    </div>
  </div>
</template>

<script>
export default {
  name: 'PrereqCourseList',
  data() {
    return {};
  },
  methods: {},
};
</script>

<style lang="scss" scoped>
li {
  list-style-type: none;
  padding-bottom: 0.5rem;
}
</style>