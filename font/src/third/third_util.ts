import { graphlib, render } from "dagre-d3"
import { div } from "../base/components/dom/div"
import * as d3 from "d3"
import constant from "src/base/web/constant";
import { Svg } from "../base/components/svg/svg";
class ThirdUtil {
    dagre_d3(el: any) {
        let g = new graphlib.Graph().setGraph({})
        g.setNode("root", {
            label: function () {
                var table = document.createElement("table"),
                    tr = d3.select(table).append("tr");
                tr.append("td").text("A");
                tr.append("td").text("B");
                return table;
            },
            padding: 0,
            rx: 5,
            ry: 5
        });
        g.setNode("A", { label: "A", fill: "#afa" });
        g.setNode("B", { label: "B", fill: "#faa" });
        g.setEdge("root", "A", {});
        g.setEdge("root", "B", {});

        // Create the renderer

        // Set up an SVG group so that we can translate the final graph.
        var svg = d3.select(el)
        var svgGroup = svg.append('g')

        // Run the renderer. This is what draws the final graph.
        new render()(svgGroup, g as any);
        // Center the graph
        // var xCenterOffset = (svg.attr('width') - g.graph().width) / 2;
        // svgGroup.attr('transform', 'translate(' + xCenterOffset + ', 20)');
        // svg.attr('height', g.graph().height + 40);
    }
}
let third_util = new ThirdUtil()
export function dagre_d3_dev() {
    return new Svg().mount_html((el: any) => {
        third_util.dagre_d3(el)
    })
}
export default third_util
