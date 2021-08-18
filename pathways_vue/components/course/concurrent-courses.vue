// concurrent-courses.vue

<template>
  <div class="card mb-5">
    <div class="card-body">
      <h3>Concurrent Courses</h3>
      <p>
        Students who took <strong>CHEM 162</strong> in the past 2 years also took the following
        courses at the same time.
      </p>
      <table class="table table-borderless">
        <thead>
          <tr class="bg-light text-dark">
            <th scope="col" style="width: 10%">% <a href="#"><i class="bi bi-info-circle-fill"></i></a></th>
            <th scope="col" class="visually-hidden" style="width: 30%">Percentage Graph</th>
            <th scope="col" style="width: 30%">Concurrent Course</th>
            <th scope="col" style="width: 30%">COI</th>
          </tr>
        </thead>
        <tbody>
          <tr class="align-middle">
            <th scope="row">73%</th>
            <td>
              <div class="progress">
                <div
                  class="progress-bar bg-secondary"
                  role="progressbar"
                  style="width: 73%"
                  aria-valuenow="73"
                  aria-valuemin="0"
                  aria-valuemax="100"
                ></div>
              </div>
            </td>
            <td>
              <a href="#" class="router-link-active"
                ><span class="badge bg-link-color text-light">CSS 415</span></a
              >
              Preparation for General Chemistry
            </td>
            <td>5.55</td>
          </tr>
          <tr class="align-middle">
            <th scope="row">55%</th>
            <td>
              <div class="progress">
                <div
                  class="progress-bar bg-secondary"
                  role="progressbar"
                  style="width: 55%"
                  aria-valuenow="55"
                  aria-valuemin="0"
                  aria-valuemax="100"
                ></div>
              </div>
            </td>
            <td>
              <a href="#" class="router-link-active"
                ><span class="badge bg-link-color text-light">MATH 124</span></a
              >
              Calculus with Analytic Geometry I
            </td>
            <td>3.51</td>
          </tr>
          <tr class="align-middle">
            <th scope="row">27%</th>
            <td>
              <div class="progress">
                <div
                  class="progress-bar bg-secondary"
                  role="progressbar"
                  style="width: 27%"
                  aria-valuenow="27"
                  aria-valuemin="0"
                  aria-valuemax="100"
                ></div>
              </div>
            </td>
            <td>
              <a href="#" class="router-link-active"
                ><span class="badge bg-link-color text-light">CHEM 317</span></a
              >
              Inorganic Chemistry Laboratory
            </td>
            <td>7.2</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ConcurrentCourses',
  data() {
    return {};
  },
  methods: {},
};
</script>

<style lang="scss"></style>