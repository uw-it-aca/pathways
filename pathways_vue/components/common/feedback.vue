// feedback.vue

<template>
  <button
    class="btn btn-sm btn-primary position-absolute end-0"
    style="margin-top: -60px; margin-right: 10px; z-index: 1"
    type="button"
    data-bs-toggle="offcanvas"
    data-bs-target="#send_feedback"
    aria-controls="send_feedback"
  >
    <i class="bi bi-chat-right-text-fill me-0"></i> Send us feedback
  </button>

  <div
    class="offcanvas offcanvas-end"
    tabindex="-1"
    id="send_feedback"
    aria-labelledby="dawgpath_feedback"
  >
    <div class="offcanvas-header">
      <h2 id="dawgpath_feedback" class="visually-hidden">Feedback Form</h2>
      <button
        type="button"
        class="btn-close text-reset"
        data-bs-dismiss="offcanvas"
        aria-label="Close"
      ></button>
    </div>
    <div class="offcanvas-body">
      <div class="embed-responsive">
        <iframe class="embed-responsive-item" :src="form_url"></iframe>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "FeedbackComp",
  data() {
    return {};
  },
  methods: {},
  computed: {
    form_url: function () {
      var url = document.body.getAttribute("data-google-feedback-form");
      return url;
    },
  },
};
</script>

<style lang="scss">
iframe {
  position: absolute;
  top: 50px;
  bottom: 0;
  left: 0;
  right: 0;
  height: 100%;
  width: 100%;
}
</style>
