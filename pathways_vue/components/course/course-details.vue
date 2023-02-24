// course-details.vue

<template>
  <div class="mb-3">
    <h1 class="h2 axdd-font-encode-sans fw-bold">
      {{ course.course_id }}: {{ course.course_title }}
    </h1>
    <icon-popover
      v-if="course.is_bottleneck"
      :variant="'bottleneck'"
    ></icon-popover>
    <icon-popover v-if="course.is_gateway" :variant="'gateway'"></icon-popover>
    <div>
      <strong>Credits:</strong>
      {{ course.course_credits }}
    </div>
    <div class="mb-2" v-if="offered_terms">
      <strong>Typically offered:</strong>
      <ul class="ms-2 d-inline list-inline">
        <li
          class="list-inline-item"
          v-for="(term, i) in offered_terms"
          :key="i"
        >
          <span class="badge text-dark" :class="term.class">{{
            term.quarter
          }}</span>
        </li>
      </ul>
    </div>

    <p>{{ course.course_description }}</p>
  </div>
</template>
r

<script>
import IconPopover from "../common/icon-popover.vue";

export default {
  name: "CourseDetails",
  components: {
    "icon-popover": IconPopover,
  },
  props: {
    course: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {};
  },
  mounted() {},
  computed: {
    offered_terms: function () {
      let matching_quarters = [];
      if (
        this.course.course_offered !== undefined &&
        this.course.course_offered !== null
      ) {
        let offered_string = this.course.course_offered;
        if (offered_string.length > 0) {
          offered_string = this.get_quarters_from_offered(offered_string);
          if (offered_string !== undefined) {
            offered_string = offered_string.trim();
            let quarters = offered_string.match(/([A-Z]?[^A-Z]*)/g);
            if (quarters.includes("A")) {
              matching_quarters.push({ quarter: "AUT", class: "creamcicle" });
            }
            if (quarters.includes("Sp")) {
              matching_quarters.push({ quarter: "SPR", class: "pw-green" });
            }
            if (quarters.includes("S")) {
              matching_quarters.push({ quarter: "SUM", class: "yellow" });
            }
            if (quarters.includes("W")) {
              matching_quarters.push({ quarter: "WIN", class: "bg-blue-200" });
            }
          }
        }
      }
      return matching_quarters;
    },
  },
  methods: {
    get_quarters_from_offered(offered) {
      offered = offered.replace(".", "");
      if (offered.includes(";")) {
        let parts = offered.split(";");
        offered = parts[1];
      }
      if (offered.includes("jointly")) {
        return undefined;
      }
      if (offered.includes(",")) {
        let parts = offered.split(",");
        return parts[0];
      } else {
        return offered;
      }
    },
  },
};
</script>
