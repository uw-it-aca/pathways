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
            <th scope="col" style="width: 10%">
              %
              <a
                tabindex="0"
                class="info-major-common"
                role="button"
                data-bs-toggle="popover"
                data-bs-trigger="focus"
                title="Percentage"
                data-bs-content="Description of common courses for majors."
              >
                <i class="bi bi-info-circle-fill"></i>
              </a>
            </th>
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
              <a href="/course/?code=CSS+415" class="router-link-active"
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
              <a href="/course/?code=MATH+124" class="router-link-active"
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
              <a href="/course/?code=CHEM+317" class="router-link-active"
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
import { Popover } from 'bootstrap';

export default {
  name: 'CommonCourses',
  data() {
    return {};
  },
  mounted() {
    var popover = new Popover(document.querySelector('.info-major-common'));
  },
  methods: {},
};
</script>

<style lang="scss" scoped></style>