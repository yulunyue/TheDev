import { Div, web_dom, Util, Data, Svg } from "../base/components/export";
import * as dagreD3 from "dagre-d3";
import * as d3 from "d3"
export class D3DagreUtil extends Svg {
    svg: any
    inner: any
    init_node(): void {
        this.svg = d3.select(this.el)
        this.inner = this.svg.append("g")
    }
    draw() {
        const g = new dagreD3.graphlib.Graph()
            // 设置图的布局方向和节点间距等选项
            .setGraph({
                rankdir: "LR",    // "TB" 表示从上到下布局
                nodesep: 50,      // 同层节点间水平间距
                ranksep: 80       // 不同层级间垂直间距
            })
            // 设置边的默认标签对象（这里设置为空对象）
            .setDefaultEdgeLabel(() => ({}));

        // 3. 添加节点 (setNode)
        // 参数1: 节点ID
        // 参数2: 节点配置对象，label 是节点显示的文本
        g.setNode("start", { label: "开始" });
        g.setNode("apply", { label: "填写申请" });
        g.setNode("approve", { label: "审核" });
        g.setNode("reject", { label: "驳回修改" });
        g.setNode("end", { label: "结束" });

        // 4. 添加边 (setEdge)
        // 参数1: 起始节点ID
        // 参数2: 目标节点ID
        // 参数3: 边的配置对象，例如可以添加 label 显示在连线上
        g.setEdge("start", "apply", { label: "开始申请" });
        g.setEdge("apply", "approve", { label: "提交审核" });
        g.setEdge("approve", "reject", { label: "不通过" });
        g.setEdge("approve", "end", { label: "通过" });
        g.setEdge("reject", "apply", { label: "重新修改" });

        // 5. 创建渲染器并渲染图形
        // 调用 dagreD3.render() 函数，将 inner 组和 graph 对象传入，即可完成所有绘制工作。
        const render = new dagreD3.render();
        render(this.inner, g as any);

        // // 6. (可选) 添加缩放和平移功能，提升用户体验
        const zoom = d3.zoom().on("zoom", (event) => {
            // this.inner.attr("transform", event.transform);
        });
        this.svg.call(zoom);
    }
    render_option(): void {
        this.draw()
    }
}