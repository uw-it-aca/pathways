//common-courses.

<template>
  <div class="card mb-5">
    <div class="card-body explore-major">
      <h3>Most commonly taken courses among students who declared this major</h3>
      <p>
        Below are the 10 most popular courses at the time of declaration among students who declared
        this major in the last 5 years.
      </p>

      <table class="table table-borderless">
        <thead>
          <tr class="bg-light text-dark">
            <th scope="col" style="width: 10%">% info</th>
            <th scope="col" class="visually-hidden" style="width: 30%">Percentage Graph</th>
            <th scope="col" style="width: 30%">Common Course</th>
            <th scope="col" style="width: 30%">CDI</th>
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
              <a href="#" class="router-link-active"><span class="badge bg-light text-dark">CSS 415</span></a> 
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
              <a href="#" class="router-link-active"><span class="badge bg-light text-dark">MATH 124</span></a> Calculus
              with Analytic Geometry I
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
              <a href="#" class="router-link-active"><span class="badge bg-light text-dark">CHEM 317</span></a> Inorganic
              Chemistry Laboratory
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
  name: 'CommonCourses',
  data() {
    return {};
  },
  methods: {},
};
</script>

<style lang="scss" scoped></style>