import { app } from "../../../scripts/app.js";
import { ComfyWidgets } from "../../../scripts/widgets.js";

const version = 2;
const name = "cg.customnodes.ShowText";
const index = app.extensions.findIndex((ext) => ext.name === name);
var install = true;
if (index>=0) {
	const installed = app.extensions[index].version;
	if (installed >= version) { install = false; }
	else { app.extensions.splice(index,1); }
}

if (install) {
	app.registerExtension({
		name: name,
		version: version,
		async beforeRegisterNodeDef(nodeType, nodeData, app) {
			if (nodeData.output_name.findIndex((n) => n==="text_displayed") >= 0 || nodeData.description === 'displays_text') {
				const onExecuted = nodeType.prototype.onExecuted;
				const onExecutionStart = nodeType.prototype.onExecutionStart;

				nodeType.prototype.onExecuted = function (message) {
					onExecuted?.apply(this, arguments);
					var text = message.text_displayed.join('');
					var w = this.widgets?.find((w) => w.name === "text_display");
					if (w === undefined) {
						w = ComfyWidgets["STRING"](this, "text_display", ["STRING", { multiline: true }], app).widget;
						w.inputEl.readOnly = true;
						w.inputEl.style.opacity = 0.6;
					}
					w.value = text;
					this.onResize?.(this.size);
				}
					
				nodeType.prototype.onExecutionStart = function () {
					onExecutionStart?.apply(this);
					var w = this.widgets?.find((w) => w.name === "text_display"); 
					if (w !== undefined) {
						w.value = '';
						this.onResize?.(this.size);
					}
				};
			}
		},
	});
}