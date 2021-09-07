<template>
  <layout :page-title="pageTitle">
    <template #title>
      <h1>{{ pageTitle }}</h1>
    </template>
    <template #content>
      <ul>
        <li><a href="#faq">Frequently Asked Questions</a></li>
        <li><a href="#terms">Term Definitions</a></li>
        <li><a href="#gpa">Declared major cumulative GPA distribution</a></li>
        <li><a href="#coi">Course outcome index</a></li>
      </ul>

      <h2 id="faq">Frequently Asked Questions</h2>
      <p>Lorem ipsum dolor sit amet consectetur adipisicing elit. Sunt id eligendi nihil consequuntur, 
        repellendus accusamus quod facere dicta error voluptates quibusdam reprehenderit dolores, 
        cumque pariatur beatae aperiam quisquam, porro quas.</p>
      <p>Lorem ipsum dolor sit amet consectetur adipisicing elit. Sunt id eligendi nihil consequuntur, 
        repellendus accusamus quod facere dicta error voluptates quibusdam reprehenderit dolores, 
        cumque pariatur beatae aperiam quisquam, porro quas.</p>
      <p>Lorem ipsum dolor sit amet consectetur adipisicing elit. Sunt id eligendi nihil consequuntur, 
        repellendus accusamus quod facere dicta error voluptates quibusdam reprehenderit dolores, 
        cumque pariatur beatae aperiam quisquam, porro quas.</p>
      <p>Lorem ipsum dolor sit amet consectetur adipisicing elit. Sunt id eligendi nihil consequuntur, 
        repellendus accusamus quod facere dicta error voluptates quibusdam reprehenderit dolores, 
        cumque pariatur beatae aperiam quisquam, porro quas.</p>
      <p>Lorem ipsum dolor sit amet consectetur adipisicing elit. Sunt id eligendi nihil consequuntur, 
        repellendus accusamus quod facere dicta error voluptates quibusdam reprehenderit dolores, 
        cumque pariatur beatae aperiam quisquam, porro quas.</p>
      
      <h2 id="terms">Term Definitions</h2>
      <p>Lorem ipsum dolor sit amet consectetur adipisicing elit. Sunt id eligendi nihil consequuntur, 
        repellendus accusamus quod facere dicta error voluptates quibusdam reprehenderit dolores, 
        cumque pariatur beatae aperiam quisquam, porro quas.</p>
      <p>Lorem ipsum dolor sit amet consectetur adipisicing elit. Sunt id eligendi nihil consequuntur, 
        repellendus accusamus quod facere dicta error voluptates quibusdam reprehenderit dolores, 
        cumque pariatur beatae aperiam quisquam, porro quas.</p>
      <p>Lorem ipsum dolor sit amet consectetur adipisicing elit. Sunt id eligendi nihil consequuntur, 
        repellendus accusamus quod facere dicta error voluptates quibusdam reprehenderit dolores, 
        cumque pariatur beatae aperiam quisquam, porro quas.</p>
      <p>Lorem ipsum dolor sit amet consectetur adipisicing elit. Sunt id eligendi nihil consequuntur, 
        repellendus accusamus quod facere dicta error voluptates quibusdam reprehenderit dolores, 
        cumque pariatur beatae aperiam quisquam, porro quas.</p>
      
      <h2 id="gpa">Declared major cumulative GPA distribution</h2>
      <p>Lorem ipsum dolor sit amet consectetur adipisicing elit. Sunt id eligendi nihil consequuntur, 
        repellendus accusamus quod facere dicta error voluptates quibusdam reprehenderit dolores, 
        cumque pariatur beatae aperiam quisquam, porro quas.</p>
      <p>Lorem ipsum dolor sit amet consectetur adipisicing elit. Sunt id eligendi nihil consequuntur, 
        repellendus accusamus quod facere dicta error voluptates quibusdam reprehenderit dolores, 
        cumque pariatur beatae aperiam quisquam, porro quas.</p>
      <p>Lorem ipsum dolor sit amet consectetur adipisicing elit. Sunt id eligendi nihil consequuntur, 
        repellendus accusamus quod facere dicta error voluptates quibusdam reprehenderit dolores, 
        cumque pariatur beatae aperiam quisquam, porro quas.</p>
      <p>Lorem ipsum dolor sit amet consectetur adipisicing elit. Sunt id eligendi nihil consequuntur, 
        repellendus accusamus quod facere dicta error voluptates quibusdam reprehenderit dolores, 
        cumque pariatur beatae aperiam quisquam, porro quas.</p>
      
      <h2 id="coi">Course outcome index</h2>
      <p>Lorem ipsum dolor sit amet consectetur adipisicing elit. Sunt id eligendi nihil consequuntur, 
        repellendus accusamus quod facere dicta error voluptates quibusdam reprehenderit dolores, 
        cumque pariatur beatae aperiam quisquam, porro quas.</p>
      <p>Lorem ipsum dolor sit amet consectetur adipisicing elit. Sunt id eligendi nihil consequuntur, 
        repellendus accusamus quod facere dicta error voluptates quibusdam reprehenderit dolores, 
        cumque pariatur beatae aperiam quisquam, porro quas.</p>
      <p>Lorem ipsum dolor sit amet consectetur adipisicing elit. Sunt id eligendi nihil consequuntur, 
        repellendus accusamus quod facere dicta error voluptates quibusdam reprehenderit dolores, 
        cumque pariatur beatae aperiam quisquam, porro quas.</p>
      <p>Lorem ipsum dolor sit amet consectetur adipisicing elit. Sunt id eligendi nihil consequuntur, 
        repellendus accusamus quod facere dicta error voluptates quibusdam reprehenderit dolores, 
        cumque pariatur beatae aperiam quisquam, porro quas.</p>
      <p>Lorem ipsum dolor sit amet consectetur adipisicing elit. Sunt id eligendi nihil consequuntur, 
        repellendus accusamus quod facere dicta error voluptates quibusdam reprehenderit dolores, 
        cumque pariatur beatae aperiam quisquam, porro quas.</p>
    </template>
  </layout>
</template>

<script>
import Layout from '../layout.vue';

export default {
  name: "App",
  components: {
    'layout': Layout,
  },
  data() {
    return {
      pageTitle: 'About DawgPath',
    };
  },
  methods: {},
};
</script>
