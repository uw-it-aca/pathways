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
          <tr v-for="course in common_courses" class="align-middle">
            <th scope="row">{{course.percent}}%</th>
            <td>
              <div class="progress">
                <div
                  class="progress-bar bg-secondary"
                  role="progressbar"
                  :style="course.width"
                  :aria-valuenow="course.percent"
                  aria-valuemin="0"
                  aria-valuemax="100"
                ></div>
              </div>
            </td>
            <td>
              <a href="/course/?code=CSS+415" class="router-link-active"><span class="badge bg-link-color text-light">{{course.course}}</span></a>
              {{course.title}}
            </td>
            <td>5.55</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
export default {
  name: 'CommonCourses',
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
    common_courses: function (){
      let processed_courses = [];

      for (const [course, data] of Object.entries(this.major.common_course_decl)) {

        let style_string = `width: ${data['percent']}%`;
        processed_courses.push({'course': course,
          'percent': data['percent'],
          'title': data['title'],
          'width': style_string})
      }

      return processed_courses.sort((a, b) => (a.percent < b.percent)? 1 : -1);
    }
  }
};
</script>

<style lang="scss" scoped></style>
