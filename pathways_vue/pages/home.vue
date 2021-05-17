// home.vue

<template>
  <layout :page-title="pageTitle">
    <!-- page content -->
    <template #title>
      {{ pageTitle }}
    </template>

    <template #description>
      <p class="p-0 col-md-8 lead">
        Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas eget pulvinar est. Sed
        gravida neque justo, pellentesque finibus velit scelerisque eu. Curabitur et dolor luctus,
        convallis magna at, mollis purus. Nunc tincidunt risus quis nisl bibendum volutpat. Praesent
        ut tincidunt ex.
      </p>
    </template>

    <template #content>
      <div class="row">
        <div class="col-md-6">
          <h2>Development Stack</h2>
          <p>
            What's included? This template repository is intended to start you off with AXDD's
            supported development stack.
          </p>
          <ul>
            <li>Django (2.1 - 2.3)
            <li>Vue (2.x)</li>
            <li>Webpack (5.x)</li>
            <li>Bootstrap (4.6.x)</li>
          </ul>
        </div>
        <div class="col-md-6">
          <h2>AXDD Libraries</h2>
          <p>
           The following is a list of specific AXDD libraries used in building applications.
          </p>
          <ul>
            <li><a href="https://github.com/uw-it-aca/django-container" target="_blank">Django Container</a></li>
            <li><a href="https://github.com/uw-it-aca/django-webpack-bridge" target="_blank">Django Webpack Bridge</a></li>
            <li><a href="https://github.com/uw-it-aca/axdd-components" target="_blank">AXDD Components</a></li>
          </ul>
        </div>
        <div class="col-md-6">
          <h2>Vue Libraries</h2>
          <p>
           The following is a list of common Vue libraries included in this repository.
          </p>
          <ul>
            <li><a href="https://bootstrap-vue.org/" target="_blank">BootstraVue</a></li>
            <li><a href="https://github.com/FortAwesome/vue-fontawesome" target="_blank">Vue FontAwesome</a></li>
            <li><a href="https://matteo-gabriele.gitbook.io/vue-gtag/" target="_blank">Vue Gtag</a></li>
          </ul>
        </div>
        <div class="col-md-6">
          <h2>Customization</h2>
          <p>
            Ready to go beyond the starter template and start buidling your application? Read about
            how to <a href="/customize/">customize</a> your application.
          </p>
        </div>
      </div>
    </template>
  </layout>
</template>

<script>
import Layout from '../layout.vue';

export default {
  components: {
    layout: Layout,
  },
  data() {
    return {
      pageTitle: 'Getting started',
    };
  },
  methods: {},
};
</script>

<style lang="scss"></style>
