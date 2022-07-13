// banner.vue

<template>

    <div class="alert alert-info alert-dismissible fade show text-center" role="alert">
        <strong>New Feature!</strong> DawgPath now shows which courses act as a bottleneck or a gateway for easier
        registration planning. <a href="/faq#bottleneck" class="router-link">Learn more.</a>
        <button type="button" class="btn btn-link close" data-bs-dismiss="alert" aria-label="Close">
            <span aria-hidden="true"><i class="bi bi-x-lg" title="Dismiss alert"></i></span>
        </button>
    </div>

</template>

<script>
export default {
    name: 'Banner',
    data() {
        return {};
    },
    methods: {},
    computed: {
    }
};
</script>

<style lang="scss" scoped>
.alert {
    border-radius: 0;
}
</style>