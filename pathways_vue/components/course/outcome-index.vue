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
      <div
        class="modal fade"
        role="dialog"
        id="coi_modal"
        tabindex="-1"
        aria-modal="true"
        aria-labelledby="coi_onboard"
        aria-hidden="true"
      >
        <div class="modal-dialog modal-dialog-centered modal-lg">
          <div class="modal-content">
            <div class="modal-body">
              <h2 class="modal-title mb-2" id="coi_onboard">COI</h2>
              <div>
                <p>Content for COI here</p>
              </div>
              <div class="text-end">
                <button
                  type="button"
                  class="btn btn-purple"
                  data-bs-dismiss="modal"
                  aria-label="Next"
                >
                  Next
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
      <button
        type="button"
        class="btn btn-link mt-2 btn-sm text-decoration-none"
        aria-label="Open modal"
        @click="showCOIModal"
      >
        open modal
      </button>
      <div v-if="course_coi == null">
        <div class="alert alert-purple" role="alert">
          <p>
            The COI is not available for
            <strong>{{ course.course_id }}</strong> because there isn't enough
            data for this course.
          </p>
        </div>
      </div>
      <div v-else>
        <div id="sr-text" class="screen-reader-only"></div>
        <div id="upper">
          <div id="layer-select"></div>
          <a id="score"></a>
        </div>
        <div aria-hidden="true" id="coiGraph" />
      </div>
    </div>
  </div>
</template>

<script>
import * as d3 from "d3";
import { Modal, Popover } from "bootstrap";
import { select } from "d3";

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
    // range_text: function () {
    //   if (this.course_coi <= 1) {
    //     return "0 - 1";
    //   } else if (this.course_coi <= 2) {
    //     return "1 - 2";
    //   } else if (this.course_coi <= 3) {
    //     return "2 - 3";
    //   } else if (this.course_coi <= 4) {
    //     return "3 - 4";
    //   } else if (this.course_coi <= 5) {
    //     return "4 - 5";
    //   }
    // },
  },
  methods: {
    showCOIModal() {
      this.coiModal = new Modal(document.getElementById("coi_modal"), {});
      this.coiModal.show();
    },
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
      // Store chosen course
      var chosenCourse;
      // Store chosen major
      var chosenMajor;

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

      // Tooltip for hover
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
      const majorPicked = coursePicked.match(/\D+/)[0].trim();

      // Specific course color (purple)
      const courseColor = "#452a78";
      // Major course color (gold)
      const majorColor = "#ab9765";
      // Major averages (grey)
      const avgColor = "#6E757C";

      // Different layer options
      const layerOptions = {
        single: {
          name: coursePicked,
          color: courseColor,
        },
        chosen: {
          name: majorPicked + " Courses",
          color: majorColor,
        },
        other: {
          name: "Other Major Averages",
          color: avgColor,
        },
      };

      // Set radius here
      const RADIUS = 4.2;
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

      // Clear legend so new data can be added
      layerSelect.html("");

      // Add some text to the container
      layerSelect
        .append("a")
        .text("View " + coursePicked + " in context")
        .style("font-weight", "bold")
        .append("br");

      var selectID;

      // Add the two options as radio buttons
      for (var option in layerOptions) {
        selectID = layerOptions[option].name.replace(" ", "-");

        layerSelect
          .append("input")
          .attr("type", "radio")
          .attr("value", option)
          .attr("id", selectID + "-button")
          .attr("name", "toggle");

        // Add the text label
        // layerSelect.append("a").text(layerOptions[option]);
        layerSelect
          .append("label")
          .text(layerOptions[option].name)
          .attr("for", selectID + "-button");

        // console.log(layerSelect.select("label").getBoundingClientRect())

        layerSelect
          .append("circle")
          .attr("r", RADIUS)
          .style("fill", layerOptions[option].color);

        // Line break
        layerSelect.append("br");
      }

      // Default selection
      layerSelect.select("input[value='single']").property("checked", true);

      // Make legend visible
      layerSelect.style("visibility", "visible");

      // Add the different annotations
      addScaleAnnotation();

      // Create and add circles for chosen major
      createPoints(this.course_coi_data, "chosen");
      // Create and add circles for other majors
      createPoints(this.curric_coi_data, "avg");

      // Populate the title with course title and score
      d3.select("#score").text("COI: " + chosenCourse.score);

      // Add an event listener to the radio buttons
      d3.selectAll("input[name='toggle']").on("change", function () {
        // Get the layer the user selected
        var selectedLayer = d3.select(this).property("value");

        var courseId = "#" + coursePicked.replace(/\s/g, "_");

        var prev = d3.selectAll(".shown, " + courseId);
        var selected;

        if (selectedLayer == "single") {
          if (d3.select(".shown").attr("class").includes("chosen")) {
            selected = d3.select(courseId + ".chosen");
          } else {
            selected = d3.select(courseId + ".avg");
          }

          // Screen reader text for the specific course
          d3.select("#sr-text").text(
            `${chosenCourse.name} has a score of ${chosenCourse.score}.`
          );

        } else if (selectedLayer == "chosen") {
          // Screen reader text for the chosen major
          d3.select("#sr-text").text(
            `${chosenCourse.name} has a score of ${chosenCourse.score} compared to the major average of ${chosenCourse.score}.`
          );

          // If the user selected the major courses layer
          selected = d3.selectAll(".chosen");
        } else {
          // Screen reader text for layer with average scores
          d3.select("#sr-text").text(
            `${chosenMajor.name} has a score of ${chosenMajor.score} compared to the average of around 0.`
          );

          // If the user selected the major averages layer
          selected = d3.selectAll(".avg");
        }

        switchLayers(prev, selected);
      });

      // Allow for the hiding and showing of different layers
      function switchLayers(hide, show) {
        // Hiding the previous layer
        // First transition: move circle(s) to the center of y axis
        hide
          .transition("moveout-vcenter")
          .duration(1000)
          .delay(function (d, i) {
            return i / 3;
          })
          .attr("cy", yCenter)
          .end()
          .then(() => {
            // Second transition: move circle(s) to the center of x axis
            hide
              .transition("moveout-hcenter")
              .duration(500)
              .delay(function (d, i) {
                return i / 3;
              })
              .attr("cx", x(0))
              .style("opacity", 0)
              .end()
              .then(() => {
                hide.classed("shown", false);
                show.classed("shown", true);

                // Layer to show
                // Third transition: move circle(s) to their respective x positions
                show
                  .transition("movein-vpoints")
                  .duration(1000)
                  .delay(function (d, i) {
                    return i / 3;
                  })
                  .style("opacity", 1)

                  .attr("cx", function (d) {
                    return d.x;
                  })
                  .end()
                  .then(() => {
                    // Fourth transition: move circle(s) to their respective y positions
                    show
                      .transition("movein-hpoints")
                      .duration(500)
                      .delay(function (d, i) {
                        return i / 3;
                      })
                      .attr("cy", function (d) {
                        if (show._groups[0].length == 1) {
                          return yCenter;
                        } else {
                          return d.y;
                        }
                      })
                      .end();
                  });
              });
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

        // Filter out data and create a new array to feed into force simulation
        var nodes = data
          .filter(function (node) {
            // Filter out UWB and UWT courses/majors
            if (
              node[labelName].includes("BOTHELL") ||
              node[labelName].includes("TACOMA") ||
              node[labelName].includes("BOTHL") ||
              node[labelName].includes("UWT") ||
              node[labelName].includes("UWB")
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
              x: x(score), // Scale the score from -5 to 5
              y: yCenter, // Set the default height of the point
              score: Math.round(score * 100) / 100, // Round the score to two decimal places
              name: node[labelName], // Give the course/major its name
              major: "curric" in node ? node.curric : majorPicked, // Major codes to each point
            };
          });

        // Add chosen course to the major averages layer
        if (layer != "chosen") {
          nodes.push({
            x: chosenCourse.x,
            y: chosenCourse.y,
            score: chosenCourse.score,
            name: chosenCourse.name,
            major: chosenCourse.major,
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
          .selectAll("." + layer + " circle")
          .data(nodes)
          .enter()
          .append("circle")
          .classed("shown", function (d) {
            console.log(d.name)
            console.log(layer)
            return d.name == vue.course_id && layer == "chosen";
          })
          .style("fill", function (d) {
            if (d.major == majorPicked && layer == "avg") {
              chosenMajor = d;
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
            if (d.name == vue.course_id && layer == "chosen") {
              return 1;
            } else {
              return 0;
            }
          })
          .attr("cx", function (d) {
            if (d.name == vue.course_id && layer == "chosen") {
              return d.x;
            } else {
              return x(0);
            }
          })
          .attr("cy", function () {
            return yCenter;
          })
          .attr("r", RADIUS)
          .attr("class", function () {
            if (layer == "chosen") {
              return "chosen";
            } else {
              return "avg";
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
                  .style("visibility", "visible")
                  .html(d.name + "<br>" + "COI: " + d.score);
              })
              .on("mousemove", function (event) {
                tooltip
                  .style("left", event.pageX + 5 + "px")
                  .style("top", event.pageY - 50 + "px");
              })
              .on("mouseout", function () {
                d3.select(this)
                  .transition()
                  .duration(200)
                  .style("stroke", "none")
                  .attr("r", RADIUS);

                tooltip.style("opacity", 0).style("visibility", "visible");
              });
          });
      }

      // Add text annotation
      function addScaleAnnotation() {
        var labelPosY = height / 1.3;
        var fontSize = "14px";

        svg
          .append("text")
          .style("font-size", fontSize)
          .attr("x", x(3.25))
          .attr("y", labelPosY)
          .attr("text-anchor", "middle")
          .html("More manageable &#128694;");
        // .html("&#10145;&#65039; More manageable &#128694;");

        svg
          .append("text")
          .style("font-size", fontSize)
          .attr("x", x(-3.25))
          .attr("y", labelPosY)
          .attr("text-anchor", "middle")
          .html("&#127939; Less manageable");
        // .html("&#127939; Less manageable &#11013;&#65039;");
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

.tooltip {
  width: auto;
}

.axis text {
  fill: black;
}

.axis line,
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
  font-size: 100%;
  visibility: hidden;
  border-radius: 15px;
  width: auto;
  padding: 1% 2%;
  background-color: #eaeaea;
}

#layer-select label {
  padding: 3%;
}

#score {
  font-size: 100%;
  font-weight: bold;
}

#upper {
  margin-top: 5%;
  display: flex;
  justify-content: start;
  align-items: center;
  gap: 20%;
}

#coiGraph path.domain,
#coiGraph g.tick {
  stroke-width: 1px;
}

#coiGraph g.tick line {
  stroke-width: 1px;
}

.screen-reader-only {
  position: absolute;
  height: 1px;
  width: 1px;
  clip: rect(1px 1px 1px 1px); // IE 6 and 7
  clip: rect(1px, 1px, 1px, 1px);
  clip-path: polygon(0px 0px, 0px 0px, 0px 0px);
  -webkit-clip-path: polygon(0px 0px, 0px 0px, 0px 0px);
  overflow: hidden !important;
}

#coi-tooltip {
  width: auto;
}

.shown {
  visibility: visible;
}
</style>
