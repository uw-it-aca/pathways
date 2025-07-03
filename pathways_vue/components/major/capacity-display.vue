<template>
  <div>
  <i :class="capacityIcon" style = "color:#4E2F7F; margin-right: 8px; font-size: 14px;">
  </i>{{capacityText}}</div>
  </template>

  <script>

  export default {
    name: "MajorCapacityDisplay",
    props: {
      admissionType: {
        type: String,
        required: true,
      },
    },
    data() {
      return {
      };
    },
    methods: {
    },
    computed: {
      capacityText(){
        if(this.admissionType === "open"){
          return "Open";
        } else if(this.admissionType === "minimumRequirements"){
          return "Minimum Requirements";
        } else if(this.admissionType === "capacity-constrained"){
          return "Capacity Constrained";
        } else {
          return "Unknown Requirements";
        }
      },
      capacityIcon(){
        if(this.admissionType === "open"){
          return "bi-circle";
        } else if(this.admissionType === "minimumRequirements"){
          return "bi-record-circle";
        } else if(this.admissionType === "capacity-constrained"){
          return "bi-circle-fill";
        } else {
          return "bi-question-circle";
        }
      },
    },
  };
  </script>
