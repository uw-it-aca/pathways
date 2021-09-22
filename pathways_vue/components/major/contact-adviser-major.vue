// contact-adviser-major.vue

<template>
  <div class="card mb-5">
    <div class="card-body">
      <h3>Are you considering this major?</h3>
      <p>
        We understand this can be a challenging process with many sources of information to
        consider. This webpage is designed to be a useful tool but not a replacement for meeting
        with an academic adviser. As you begin to consider what you want to major in, we recommend
        scheduling a meeting with your adviser to discuss your interests, goals, degree requirements
        and academic planning.
      </p>
      <form action="https://www.washington.edu/uaa/advising/">
        <button type="submit" class="btn btn-purple" aria-label="Contact your adviser">
          Contact your adviser
        </button>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ContactAdviserMajor',
  data() {
    return {};
  },
  methods: {},
};
</script>

<style lang="scss" scoped></style>
