Highcharts.chart("container", {
          chart: {
            spacingBottom: 30,
            marginRight: 120,
            height: 1200
          },
          title: {
            text: " Sri Aditya Developers"
          },
          series: [
            {
              type: "treegraph",
              keys: ["parent", "id", "level"],
              clip: false,
              data: [

                // Sri Aditya Developers tree
                [undefined, "Sri Aditya Developers"],
                ["Sri Aditya Developers", "Branch 1"],
                ["Sri Aditya Developers", "Branch 2"],
                ["Sri Aditya Developers", "Branch 3"],
                ["Sri Aditya Developers", "Branch 4"],
                ["Sri Aditya Developers", "Branch 5"],
                ["Branch 1", "Leaf 1-1", 3],
                ["Branch 1", "Leaf 1-2", 3],
                ["Branch 1", "Leaf 1-3", 3],
                ["Branch 1", "Leaf 1-4", 3],
                ["Branch 1", "Leaf 1-5", 3],
                ["Branch 2", "Leaf 2-1", 3],
                ["Branch 2", "Leaf 2-2", 3],
                ["Branch 2", "Leaf 2-3", 3],
                ["Branch 2", "Leaf 2-4", 3],
                ["Branch 2", "Leaf 2-5", 3],
                ["Branch 3", "Leaf 3-1", 3],
                ["Branch 3", "Leaf 3-2", 3],
                ["Branch 3", "Leaf 3-3", 3],
                ["Branch 3", "Leaf 3-4", 3],
                ["Branch 3", "Leaf 3-5", 3],
                ["Branch 4", "Leaf 4-1", 3],
                ["Branch 4", "Leaf 4-2", 3],
                ["Branch 4", "Leaf 4-3", 3],
                ["Branch 4", "Leaf 4-4", 3],
                ["Branch 4", "Leaf 4-5", 3],
                ["Branch 5", "Leaf 5-1", 3],
                ["Branch 5", "Leaf 5-2", 3],
                ["Branch 5", "Leaf 5-3", 3],
                ["Branch 5", "Leaf 5-4", 3],
                ["Branch 5", "Leaf 5-5", 3]
              ],
              marker: {
                symbol: "circle",
                radius: 6,
                fillColor: "#ffffff",
                lineWidth: 3
              },
              dataLabels: {
                align: "left",
                pointFormat: "{point.id}",
                style: {
                  color: "#000000",
                  textOutline: "3px #ffffff",
                  whiteSpace: "nowrap"
                },
                x: 24,
                crop: false,
                overflow: "none"
              },
              levels: [
                {
                  level: 1,
                  levelIsConstant: false
                },
                {
                  level: 2,
                  colorByPoint: true
                },
                {
                  level: 3,
                  colorVariation: {
                    key: "brightness",
                    to: -0.5
                  }
                },
                {
                  level: 4,
                  colorVariation: {
                    key: "brightness",
                    to: 0.5
                  }
                },
                {
                  level: 6,
                  dataLabels: {
                    x: 10
                  },
                  marker: {
                    radius: 4
                  }
                }
              ]
            }
          ]
        });