// outcome-index.vue

<template>
  <div class="card mb-5">
    <div class="card-body">
      <h2 class="h4 axdd-font-encode-sans fw-bold">
        Course Outcome Index (COI)
      </h2>
      <p>
        Using prior course data, this index compares estimated pass/completion
        rates against actual pass/completion rates.
        <a
          tabindex="0"
          class="info-popper"
          role="button"
          data-bs-toggle="popover"
          data-bs-trigger="focus"
          title="Course Outcome Indicator"
          data-bs-content="A negative COI indicates that fewer people completed the course than expected. COI around 0 indicates the course is on target with expectations. A positive COI indicates that more people completed the course than anticipated."
        >
          <i class="bi bi-info-circle-fill"></i>
        </a>
      </p>
      <div id="sr-text"></div>
      <div id="upper">
        <div id="layer-select"></div>
        <a id="score"></a>
      </div>
      <div aria-hidden="true" id="coiGraph" />
    </div>
  </div>
</template>

<script>
import * as d3 from "d3";
import { Popover } from "bootstrap";

export default {
  name: "OutcomeScore",
  data() {
    return {
      percent_in_range: null,
      course_coi: null,
      course_level_coi: null,
      curric_coi: null,
      curric_id: null,
      curric_abbr: null,
      course_num: null,
      course_level: null,
      course_coi_data: null,
      curric_coi_data: null,
    };
  },
  props: {
    course: {
      type: Object,
      required: true,
    },
  },
  watch: {
    course: function (course) {
      this.init();
    },
  },
  mounted() {
    var popover = new Popover(document.querySelector(".info-popper"));
    this.init();
  },
  computed: {
    range_text: function () {
      if (this.course_coi <= 1) {
        return "0 - 1";
      } else if (this.course_coi <= 2) {
        return "1 - 2";
      } else if (this.course_coi <= 3) {
        return "2 - 3";
      } else if (this.course_coi <= 4) {
        return "3 - 4";
      } else if (this.course_coi <= 5) {
        return "4 - 5";
      }
    },
  },
  methods: {
    init() {
      this.percent_in_range = this.course.coi_data.percent_in_range;
      this.course_coi = this.course.coi_data.course_coi;
      this.course_level_coi = this.course.coi_data.course_level_coi;
      this.curric_coi = this.course.coi_data.curric_coi;
      this.course_id = this.course.course_id;

      var split_pos = this.course_id.lastIndexOf(" ");
      this.curric_abbr = this.course_id.substring(0, split_pos);
      this.course_num = parseInt(
        this.course_id.substring(split_pos + 1, this.course_id.length)
      );
      this.course_level = Math.floor(this.course_num / 100) * 100;
      this.getCourseCOI();
    },
    getData() {
      this.getCurricCOI();
    },

    generateRect() {
      let vue = this;
      var chosenCourse;
      var chosenCurric;
      // Clear any previous graphs
      document.getElementById("coiGraph").innerHTML = "";
      const margin = { top: 20, right: 10, bottom: 20, left: 10 };
      const width = 600 - margin.left - margin.right,
        height = 200 - margin.top - margin.bottom,
        rwidth = width + margin.left + margin.right,
        rheight = height + margin.top + margin.bottom;

      // Append SVG to container
      const svg = d3
        .select("#coiGraph")
        .append("svg")
        .attr("viewBox", `0 0 ${rwidth} ${rheight}`)
        .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

      const tooltip = d3
        .select("body")
        .append("div")
        .attr("class", "tooltip")
        .attr("id", "coi-tooltip")
        .style("opacity", 0)
        .style("left", "-9999px")
        .style("visibility", "hidden");

      // Pull in data to plot on line
      const coursePicked = vue.course_id;
      // Get the major of the chosen course
      const curricPicked = coursePicked.match(/\D+/)[0].trim();

      const courseColor = "#452a78";
      const majorColor = "#ab9765";
      const avgColor = "#6E757C";

      // Different layer options
      const layerOptions = {
        single: coursePicked,
        chosen: curricPicked + " Courses",
        other: "Other Major Averages",
      };

      // Set radius here
      const RADIUS = 4;
      const yCenter = 65;

      // Create the 5.0 COI scale
      const x = d3.scaleLinear().domain([-5, 5]).range([0, width]);

      // Scale score from -5 to 5
      var scaleScore = d3.scaleLinear().domain([0, 5]).range([5, -5]);

      // Draw the axis
      var xAxis = d3.axisBottom(x).ticks(11);

      // Add axis to the svg
      svg
        .append("g")
        .attr("class", "x axis")
        .attr(
          "transform",
          "translate(0," + (height - margin.bottom * 0.3) + ")"
        )
        .call(
          xAxis
            .tickValues([-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5])
            .tickFormat(function (d) {
              return d3.format(".0f")(d);
            })
        );

      // Where the layer select buttons will be
      var layerSelect = d3.select("#layer-select");

      // Add some text to the container
      layerSelect
        .append("a")
        .text("View " + coursePicked + " in context")
        .style("font-weight", "bold")
        .append("br");

      // Add the two options as radio buttons
      for (var option in layerOptions) {
        layerSelect
          .append("input")
          .attr("type", "radio")
          .attr("value", option)
          .attr("id", layerOptions[option] + "-button")
          .attr("name", "toggle");

        // Add the text label
        // layerSelect.append("a").text(layerOptions[option]);
        layerSelect
          .append("label")
          .text(layerOptions[option])
          .attr("for", layerOptions[option] + "-button");

        // Line break
        layerSelect.append("br");
      }

      // Default selection
      layerSelect.select("input[value='single']").property("checked", true);

      // Add the different annotations
      addScaleAnnotation();

      // Create and add circles for chosen major
      createPoints(this.course_coi_data, "chosen");
      // Create and add circles for other majors
      createPoints(this.curric_coi_data, "avg");

      // Add an event listener to the radio buttons
      d3.selectAll("input[name='toggle']").on("change", function () {
        // Get the layer the user selected
        var selectedLayer = d3.select(this).property("value");

        // Chosen course point
        var course = d3.select("#" + coursePicked.replace(/\s/g, "_"));

        // Select the different layers
        var chosen = d3.selectAll(".chosen");
        var curric = d3.selectAll(".curric");

        d3.select("#sr-text").text(
          chosenCourse.name + " has a score of " + chosenCourse.score + " compared to the major average of " + curricPicked.score
        );

        if (selectedLayer == "single") {
          var prevLayer;

          if (d3.select(".chosen").style("visibility") == "visible") {
            prevLayer = chosen;
          } else {
            prevLayer = curric;
          }

          switchLayers(prevLayer, course);
        } else if (selectedLayer == "chosen") {
          // If the user selected the major courses layer
          switchLayers(curric, chosen);
        } else {
          // If the user selected the major averages layer
          switchLayers(chosen, curric);
        }
      });

      // Allow for the hiding and showing of different layers
      function switchLayers(hide, show) {
        hide
          .transition("moveOut")
          .duration(1000)
          .delay(function (d, i) {
            return i / 3;
          })
          .style("opacity", 0)
          .attr("cy", yCenter)
          .attr("cx", x(0))
          .each(function () {
            d3.select(this).moveToBack();
          })
          .end()
          .then(() => {
            hide.style("visibility", "hidden");
            show.style("visibility", "visible");

            show
              .transition("moveIn")
              .duration(1000)
              .delay(function (d, i) {
                return i / 3;
              })
              .style("opacity", 1)
              .attr("cy", function (d) {
                return d.y;
              })
              .attr("cx", function (d) {
                return d.x;
              })
              .each(function () {
                d3.select(this).moveToFront();
              })
              .end();
          });
      }

      // Function to generate and hide all the points onto the svg
      function createPoints(data, layer) {
        var labelName;
        if (layer == "chosen") {
          labelName = "course_id";
        } else {
          labelName = "curric_name";
        }

        //
        var nodes = data
          .filter(function (node) {
            if (
              node[labelName].includes("BOTHELL") ||
              node[labelName].includes("TACOMA")
            ) {
              return false;
            } else if (node.score == null) {
              return false;
            } else {
              return true;
            }
          })
          .map(function (node) {
            var score = scaleScore(node.score);
            return {
              x: x(score),
              y: yCenter + Math.abs(Math.random()),
              score: Math.round(score * 100) / 100,
              name: node[labelName],
            };
          });

        // Add chosen course to the major averages layer
        if (layer != "chosen") {
          nodes.push({
            x: chosenCourse.x,
            y: chosenCourse.y,
            score: chosenCourse.score,
            name: chosenCourse.name,
          });
        }

        // Specify force specifications for the circles
        var force = d3
          .forceSimulation(nodes)
          .force("forceX", d3.forceX((d) => d.x).strength(1))
          .force("forceY", d3.forceY(yCenter).strength(0.1))
          .force(
            "charge",
            d3.forceManyBody().distanceMax(2).distanceMin(1).strength(1)
          )
          .force("collide", d3.forceCollide().radius(RADIUS).strength(1))
          .on("tick", tick)
          .stop();

        function tick() {
          for (var i = 0; i < nodes.length; i++) {
            var node = nodes[i];
            node.cx = node.x;
            node.cy = node.y;
          }
        }

        const NUM_ITERATIONS = 500;
        force.tick(NUM_ITERATIONS);
        force.stop();

        // Add the points to the plot
        // Depending on whether the course is chosen, the fill color and opacity will be different
        svg
          .selectAll("circle ." + layer)
          .data(nodes)
          .enter()
          .append("circle")
          .style("visibility", function (d) {
            if (d.name == coursePicked && layer == "chosen") {
              return "visible";
            } else {
              return "hidden";
            }
          })
          .style("fill", function (d) {
            if (d.name == vue.curric_abbr) {
              chosenCurric = d;
            }
            if (d.name == vue.course_id) {
              chosenCourse = d;
              return courseColor;
            } else if (layer == "chosen") {
              return majorColor;
            } else {
              return avgColor;
            }
          })
          .style("opacity", function (d) {
            if (d.name == coursePicked && layer == "chosen") {
              return 1;
            } else {
              return 0;
            }
          })
          .attr("cx", function (d) {
            if (d.name == coursePicked && layer == "chosen") {
              return d.x;
            } else {
              return x(0);
            }
          })
          .attr("cy", function (d) {
            if (d.name == coursePicked && layer == "chosen") {
              return d.y;
            } else {
              return yCenter;
            }
          })
          .attr("r", RADIUS)
          .attr("class", function () {
            if (layer == "chosen") {
              return "chosen";
            } else {
              return "curric";
            }
          })
          .attr("id", function (d) {
            return d.name.replace(/\s/g, "_");
          })
          .attr("score", function (d) {
            return d.score;
          })
          .each(function () {
            d3.select(this)
              .on("mouseover", function (event, d) {
                d3.select(this)
                  .moveToFront()
                  .transition()
                  .duration(100)
                  .style("stroke", "black")
                  .attr("r", RADIUS * 1.2);

                tooltip
                  .style("opacity", 1)
                  .html(d.name + "<br>" + "COI: " + d.score)
                  .style("left", event.pageX + 5 + "px")
                  .style("top", event.pageY - 50 + "px");
              })
              .on("mouseout", function () {
                d3.select(this)
                  .transition()
                  .duration(200)
                  .style("stroke", "none")
                  .attr("r", RADIUS);

                tooltip.style("opacity", 0);
              });
          });
      }

      function addScaleAnnotation() {
        // Add text annotation
        var labelPosY = height / 1.3;
        var fontSize = "12px";

        svg
          .append("text")
          .style("font-size", fontSize)
          .attr("x", x(3.25))
          .attr("y", labelPosY)
          .attr("text-anchor", "middle")
          .html("More manageable &#128694;");

        svg
          .append("text")
          .style("font-size", fontSize)
          .attr("x", x(-3.25))
          .attr("y", labelPosY)
          .attr("text-anchor", "middle")
          .html("&#127939; Less manageable");
      }

      d3.selection.prototype.moveToFront = function () {
        return this.each(function () {
          this.parentNode.appendChild(this);
        });
      };

      d3.selection.prototype.moveToBack = function () {
        return this.each(function () {
          var firstChild = this.parentNode.firstChild;
          if (firstChild) {
            this.parentNode.insertBefore(this, firstChild);
          }
        });
      };
    },
    getCourseCOI() {
      let url = "/api/v1/coi/course/" + this.course.department_abbrev,
        vue = this;
      this.axios
        .get(url)
        .then((response) => {
          vue.course_coi_data = response.data;
          this.getData();
        })
        .catch(function (error) {
          vue.course_coi_data = {};
        });
    },
    getCurricCOI() {
      let vue = this;
      this.axios
        .get("/api/v1/coi/curric/")
        .then((response) => {
          vue.curric_coi_data = response.data;
          this.generateRect();
        })
        .catch(function (error) {
          vue.curric_coi_data = {};
        });
    },
  },
};
</script>

<style lang="scss">
@import url("https://fonts.googleapis.com/css2?family=Open+Sans&display=swap");

text {
  font-family: "Open Sans", sans-serif;
}

#scatter svg {
  margin-right: auto;
  margin-left: auto;
}

#coi-tooltip {
  width: auto;
}

.axis text {
  fill: black;
}

.axis line {
  stroke: gray;
  stroke-width: 2px;
}

.axis path {
  stroke: gray;
  stroke-width: 2px;
}

.grid {
  stroke: grey;
}

#more {
  font-style: italic;
  fill: green;
}

#less {
  font-style: italic;
  fill: red;
}

#layer-select {
  border-radius: 15px;
  width: 26%;
  padding: 10px;
  background-color: rgb(234, 234, 234);
}

#layer-select label {
  padding: 5px;
}

#score {
  font-size: 20px;
  font-weight: bold;
}

#upper {
  margin-top: 5%;
  display: flex;
  justify-content: start;
  align-items: center;
  gap: 15%;
}

#coiGraph path.domain,
#coiGraph g.tick {
  stroke-width: 1px;
}

#coiGraph g.tick line {
  stroke-width: 1px;
}
</style>
