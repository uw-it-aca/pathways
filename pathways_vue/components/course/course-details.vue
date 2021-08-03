// course-details.

<template>
  <div class="mb-5">
    <h2>CHEM 162: General Chemistry</h2>
    <div><strong>Credits:</strong> 5</div>
    <div>
      <strong>Offered</strong>
      <ul class="ms-2 d-inline list-inline">
        <li class="list-inline-item"><span class="badge pw-green text-dark">SPR</span></li>
        <li class="list-inline-item"><span class="badge creamcicle text-dark">AUT</span></li>
        <li class="list-inline-item"><span class="badge bg-blue-200 text-dark">WIN</span></li>
      </ul>
    </div>

    <p>
      Lorem ipsum dolor, sit amet consectetur adipisicing elit. Itaque numquam a maxime delectus
      tempora, ad molestiae rerum voluptate commodi cupiditate at quo fuga praesentium dicta
      repellendus quia et accusantium ab
    </p>
  </div>
</template>

<script>
export default {
  name: 'CourseDetails',
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