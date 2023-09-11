import { app } from "../../../scripts/app.js";
import { ComfyWidgets } from "../../../scripts/widgets.js";

app.registerExtension({
	name: "cg.customnodes.combo",
	version: 1,
	async beforeRegisterNodeDef(nodeType, nodeData, app) {
		if (nodeData.description.includes('combo')) {
			const onConnectionsChange = nodeType.prototype.onConnectionsChange;
            const onExecuted = nodeType.prototype.onExecuted;
			nodeType.prototype.onConnectionsChange = function (side,slot,connect,link_info,output) {
				onConnectionsChange?.apply(side,slot,connect,link_info,output);
                if (side==2 && connect) { // LiteGraph.OUTPUT connected
                    const target_id = link_info.target_id;
                    const target_slot = link_info.target_slot;
                    const input = this.graph._nodes_by_id[target_id].inputs[target_slot];
                    this.outputs[slot].type = input.type;
                    this.outputs[slot].name = input.name;
                    this.widgets[0].options.values = input.widget.config[0];
                    this.widgets[0].value = input.widget.config[0][0];
                    this.onResize?.(this.size);
                }
			};

            nodeType.prototype.onExecuted = function (message) {
				onExecuted?.apply(this, arguments);
                var index = this.widgets[0].options.values.findIndex((v) => v === this.widgets[0].value);
                index = index + 1;
                if (index === this.widgets[0].options.values.length) { index = 0; }
                this.widgets[0].value = this.widgets[0].options.values[index];
				this.onResize?.(this.size);
			}


		}
	},
});
