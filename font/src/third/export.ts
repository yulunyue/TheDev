import { MeraGraph } from "./mermaid_util"
import { Ct, DivFactory } from "../base/components/export"
import { D3Chart } from "./d3_util/chart"
DivFactory.register(Ct.DOM_TYPE_MERA_GRAPH, () => new MeraGraph())
DivFactory.register(Ct.DOM_TYPE_D3_CHART, () => new D3Chart())
export { D3Chart, MeraGraph }