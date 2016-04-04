package eu.tnova.rundeck.plugin.node;

import com.dtolabs.rundeck.core.common.INodeEntry;
import com.dtolabs.rundeck.core.common.INodeSet;
import com.dtolabs.rundeck.core.execution.workflow.steps.FailureReason;
import com.dtolabs.rundeck.core.execution.workflow.steps.node.NodeStepException;
import com.dtolabs.rundeck.core.execution.workflow.steps.node.NodeStepFailureReason;
import com.dtolabs.rundeck.core.plugins.Plugin;
import com.dtolabs.rundeck.core.plugins.configuration.AbstractBaseDescription;
import com.dtolabs.rundeck.core.plugins.configuration.Describable;
import com.dtolabs.rundeck.core.plugins.configuration.Description;
import com.dtolabs.rundeck.core.plugins.configuration.Property;
import com.dtolabs.rundeck.core.plugins.configuration.PropertyUtil;
import com.dtolabs.rundeck.plugins.descriptions.PluginDescription;
import com.dtolabs.rundeck.plugins.step.NodeStepPlugin;
import com.dtolabs.rundeck.plugins.step.PluginStepContext;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collection;
import java.util.Collections;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

@Plugin(service = "WorkflowNodeStep", name = "httpCommandNodeStep")
@PluginDescription(title = "A http Command NodeStep",
		description = "Description of this http Command NodeStep")
public class HttpCommandNodeStep implements NodeStepPlugin, Describable {
	public static final String TYPE = "httpCommandNodeStep";
	static final Map<String, String> CONFIG_MAPPING;
	static final Map<String, String> CONFIG_MAPPING_FWK;
	static final List<Property> properties = new ArrayList();

	static {
		List<String> selectMethodsValues = Arrays.asList("POST", "PUT",
				"DELETE");

		properties.add(PropertyUtil.select("method", "METHOD",
				"Method to  call", true, "POST", selectMethodsValues));

		properties.add(PropertyUtil.string("url", "URL", "Choose the URL",
				true, ""));

		properties.add(PropertyUtil.string("user", "User",
				"Authenticated User", true, ""));

		properties.add(PropertyUtil.string("password", "Password", "Password",
				true, ""));

		Map<String, String> mapping = new HashMap();
		mapping.put("method", "plugin.httpCommandNodeStep.default.command");
		mapping.put("url", "plugin.httpCommandNodeStep.default.shell");
		CONFIG_MAPPING = Collections.unmodifiableMap(mapping);
		CONFIG_MAPPING_FWK = Collections.unmodifiableMap(mapping);
	}

	public static final Description DESC = new AbstractBaseDescription() {
		public String getName() {
			return "httpCommandNodeStep";
		}

		public String getTitle() {
			return "HTTP call";
		}

		public String getDescription() {
			return "Make a HTTP call";
		}

		public List<Property> getProperties() {
			return HttpCommandNodeStep.properties;
		}

		public Map<String, String> getPropertiesMapping() {
			return HttpCommandNodeStep.CONFIG_MAPPING;
		}

		public Map<String, String> getFwkPropertiesMapping() {
			return HttpCommandNodeStep.CONFIG_MAPPING_FWK;
		}

	};

	public static enum Reason implements FailureReason {
		CopyFileFailed;

		private Reason() {
		}
	}

	public void executeNodeStep(PluginStepContext context,
			Map<String, Object> configuration, INodeEntry entry)
			throws NodeStepException {

		try {
			context.getLogger().log(2, "hostname = " + entry.extractHostname());
			context.getLogger().log(2, "nodename = " + entry.getNodename());
			context.getLogger().log(2,
					"description = " + entry.getDescription());

			context.getLogger().log(2, "HttpCommands.send...");

			INodeSet nodeSet = context.getNodes();
			Collection<String> nodesNames = nodeSet.getNodeNames();
			for (String snodeName : nodesNames) {
				context.getLogger().log(2, "snodeName=" + snodeName);
			}

			/*
			 * String sFramework = context.getFramework().toString();
			 * context.getLogger().log(2, "executeNodeStep.sFramework = " +
			 * sFramework);
			 * 
			 * String sFrameworkProject = context.getFrameworkProject();
			 * context.getLogger().log(2, "executeNodeStep.sFrameworkProject = "
			 * + sFrameworkProject);
			 */

			// context.getLogger().log(
			// 2,
			// "executeNodeStep.configuration.toString() = "
			// + configuration.toString());

			String method = (String) configuration.get("method");
			String url = (String) configuration.get("url");
			String user = (String) configuration.get("user");
			String password = (String) configuration.get("password");

			context.getLogger().log(2, "method = " + method);
			context.getLogger().log(2, "url = " + url);

			HttpRequests httpRequests = new HttpRequests();

			switch (method) {
			case "POST":
				httpRequests
						.send(HttpRequests.Method.post, url, user, password);
				break;
			case "PUT":
				httpRequests.send(HttpRequests.Method.put, url, user, password);
				break;
			case "DELETE":
				httpRequests.send(HttpRequests.Method.delete, url, user,
						password);
				break;
			default:
				System.out.println("HttpCommands.invalid method");
			}

		} catch (Exception e) {
			context.getLogger().log(0, "FALLITO: " + e.getMessage());
			throw new NodeStepException(e,
					NodeStepFailureReason.ConnectionFailure,
					entry.getNodename());
		}
	}

	public void send_post(String url, String user, String password)
			throws Exception {
		System.out.println("httpCall.send_post.start");
		HttpRequests httpRequests = new HttpRequests();
		httpRequests.send(HttpRequests.Method.post, url, user, password);
		System.out.println("httpCall.send_post.stop");
	}

	public void send_put(String url, String user, String password)
			throws Exception {
		System.out.println("httpCall.send_put.start");
		HttpRequests httpRequests = new HttpRequests();
		httpRequests.send(HttpRequests.Method.put, url, user, password);
		System.out.println("httpCall.send_put.stop");
	}

	public void send_delete(String url, String user, String password)
			throws Exception {
		System.out.println("httpCall.send_delete.start");
		HttpRequests httpRequests = new HttpRequests();
		httpRequests.send(HttpRequests.Method.delete, url, user, password);
		System.out.println("httpCall.send_delete.stop");
	}

	public static void main(String[] args) throws Exception {
		System.out.println("HttpCommands.start");
		HttpCommandNodeStep httpCommandNodeStep = new HttpCommandNodeStep();
		httpCommandNodeStep
				.send_post(
						"http://localhost:8080/examples/servlets/servlet/doGetdoPostdoPutServlet",
						"davide", "password");
		httpCommandNodeStep
				.send_put(
						"http://localhost:8080/examples/servlets/servlet/doGetdoPostdoPutServlet",
						"davide", "password");
		httpCommandNodeStep
				.send_delete(
						"http://localhost:8080/examples/servlets/servlet/doGetdoPostdoPutServlet",
						"davide", "password");
		System.out.println("HttpCommands.stop");
	}

	@Override
	public Description getDescription() {
		return DESC;
	}

}
