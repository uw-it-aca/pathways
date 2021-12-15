// feedback.vue

<template>
    <div class="position-relative mt-5">
        <div class="position-absolute bottom-0 end-0 p-3" style="z-index: 11;">
            <button
                class="btn btn-outline-primary"
                type="button"
                data-bs-toggle="offcanvas"
                data-bs-target="#offcanvasRight"
                aria-controls="offcanvasRight"
            ><i class="bi bi-chat-right-text-fill me-0"></i> Send us feedback</button>
        </div>
    </div>
    <div
        class="offcanvas offcanvas-end"
        tabindex="-1"
        id="offcanvasRight"
        aria-labelledby="offcanvasRightLabel"
    >
        <div class="offcanvas-header">
            <h5 id="offcanvasRightLabel">Feedback Form</h5>
            <button
                type="button"
                class="btn-close text-reset"
                data-bs-dismiss="offcanvas"
                aria-label="Close"
            ></button>
        </div>
        <div class="offcanvas-body">
            <div class="embed-responsive">
                <iframe class="embed-responsive-item" src="https://docs.google.com/forms/d/e/1FAIpQLScepHr_b5xnbFkPSsdWJb7QZ-raw27aKrY48tcx60NSF8TbVA/viewform?embedded=true"></iframe>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'Feedback',
    data() {
        return {};
    },
    methods: {},
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
  };
</style>