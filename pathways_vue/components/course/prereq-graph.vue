// prereq-graph.vue

<template>
  <div>
    <div :id="'graph_container_' + id"/>
  </div>
</template>

<script>
export default {
  name: 'PrereqGraph',
  data() {
    return {
      id: undefined
    };
  },
  props: {
    graph_data: {
      type: Object,
      required: true,
    },
    graph_type: {
      type: String,
      required: true,
    },
    active_course: {
      type: String,
      required: false,
    },
  },
  watch: {
    graph_data(){
      this.show_graph()
    },
  },
  created() {
    this.id = this.uuid()
    var vue = this;
    // Ensures div has ID set when graph is being appended
    setTimeout(() => {vue.show_graph()}, 100);
  },
  methods: {
    uuid() {
      return ([1e7]+-1e3+-4e3+-8e3+-1e11).replace(/[018]/g, c =>
        (c ^ crypto.getRandomValues(new Uint8Array(1))[0] & 15 >> c / 4).toString(16)
      );
    },
    show_graph(){
      if(this.graph_data  && Object.keys(this.graph_data).length > 0){
        // draw the graph
        let graph_div = document.getElementById('graph_container_' + this.id);
        this.new_graph(graph_div, this.graph_data.x, this.active_course);
      }
    },
    new_graph(graph_div, data, course_param) {
      var node_list = [];
      for (var i = 0; i < Object.keys(data.nodes.course_number).length; i++) {
        var course_id =
          data.nodes.department_abbrev[i] + " " + data.nodes.course_number[i];
        node_list.push({id: course_id, label: course_id});
      }

      var edge_list = [];
      Object.keys(data.edges.from).forEach(function (key) {
        var from = data.edges.from[key];
        var to = data.edges.to[key];
        edge_list.push({from: from, to: to});
      });
      var nodes = new vis.DataSet(node_list);
      var edges = new vis.DataSet(edge_list);

      var options = data.options; // [TODO] not resuse `data`?
      var data = { nodes: nodes, edges: edges };
      var network = new vis.Network(graph_div, data, options);

      // manipulation of network map based on location
      if (this.graph_type == "curric") {

        // Removing this unless we need to handle clicking on courses

        // actual selectNode click event
        // network.on("selectNode", function(properties) {
        //   console.log("node selected");
        //   var ids = properties.nodes;
        //   var clickedNode = nodes.get(ids);
        //   // show course infobox for a given node (course id)
        //   $(document).trigger("showCourseInfo", [clickedNode[0].id]);
        //   // animate to the course node and animate
        //   network.focus(clickedNode[0].id, { scale: 1.25, animation: true });
        // });
        //
        // network.on("deselectNode", function(properties) {
        //   // close infobox when deselected
        //   $(document).trigger("closeCourseInfo");
        // });

        // if course param was passed
        if (course_param) {
          // select and focus on that course node
          try {
            network.selectNodes([course_param]);
            network.focus(course_param, {
              scale: 1.0,
              offset: {x:50, y:50},
              animation: true
            });
          } catch(error){
          }
        } else {
          // default zoom for ONLY curric search (initial)
          network.moveTo({
            position: { x: 200, y: 200 },
            scale: 0.50
          });
        }
      } else if (this.graph_type == "course") {
        if (course_param) {
          // auto select course node and zoom to it
          network.selectNodes([course_param]);
          network.focus(course_param, { scale: 1.25 });

          // disable de-select by keeping course node selected
          network.on("deselectNode", function(properties) {
            network.selectNodes([course_param]);
          });
        }
      }
    }

  },
};
</script>

<style lang="scss"></style>
