<template>
  <a
    tabindex="0"
    class="info-bottleneck"
    role="button"
    data-bs-toggle="popover"
    data-bs-trigger="focus"
    data-bs-placement="left"
    data-bs-content="This course acts as a bottleneck course. These high-demand courses are typically required for graduation and have prerequisites."
  >
    <div class="round round-sm bg-danger mb-2">
      <span class="material-symbols-outlined fw-bold">call_merge</span>
    </div>
  </a>
</template>

<script>
import { Popover } from 'bootstrap';
export default {
  name: 'IconBottleneck',
  data() {
    return {};
  },
  mounted() {
    // enable popovers everywhere
    // https://getbootstrap.com/docs/5.1/components/popovers/#example-enable-popovers-everywhere
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
      return new Popover(popoverTriggerEl);
    });
  },
};
</script>

<style lang="scss">
.material-symbols-outlined {
  vertical-align: middle;
  line-height: 0 !important;
  position: relative;
  top: -1px;
  font-size: 1rem;
}
.round {
  display: inline-block;
  height: 30px;
  width: 30px;
  line-height: 30px;
  -moz-border-radius: 15px;
  border-radius: 15px;
  background-color: #222;
  color: #fff;
  text-align: center;
}
.round.round-sm {
  height: 25px;
  width: 25px;
  line-height: 25px;
  -moz-border-radius: 15px;
  border-radius: 15px;
  font-size: 0.7em;
}
</style>
