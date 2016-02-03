package eu.tnova.rundeck.plugin.node;

import com.dtolabs.rundeck.core.common.INodeEntry;
import com.dtolabs.rundeck.core.common.INodeSet;
import com.dtolabs.rundeck.core.execution.workflow.steps.FailureReason;
import com.dtolabs.rundeck.core.execution.workflow.steps.node.NodeStepException;
import com.dtolabs.rundeck.core.execution.workflow.steps.node.NodeStepResult;
import com.dtolabs.rundeck.core.plugins.Plugin;
import com.dtolabs.rundeck.core.plugins.configuration.AbstractBaseDescription;
import com.dtolabs.rundeck.core.plugins.configuration.Describable;
import com.dtolabs.rundeck.core.plugins.configuration.Description;
import com.dtolabs.rundeck.core.plugins.configuration.Property;
import com.dtolabs.rundeck.core.plugins.configuration.PropertyUtil;
import com.dtolabs.rundeck.plugins.descriptions.PluginDescription;
import com.dtolabs.rundeck.plugins.step.NodeStepPlugin;
import com.dtolabs.rundeck.plugins.step.PluginStepContext;

//import eu.tnova.rundesk.HttpCommands;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.net.MalformedURLException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collection;
import java.util.Collections;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import javax.ws.rs.core.MediaType;
import javax.ws.rs.core.Response;

import org.apache.cxf.jaxrs.client.WebClient;
import org.apache.cxf.jaxrs.ext.multipart.Attachment;
import org.apache.cxf.jaxrs.ext.multipart.ContentDisposition;
import org.apache.cxf.jaxrs.ext.multipart.MultipartBody;

@Plugin(service = "WorkflowNodeStep", name = "httpUploadNodeStep")
@PluginDescription(title = "A http file copy NodeStep",
		description = "Description of this http upload NodeStep")
public class HttpUploadNodeStep implements NodeStepPlugin, Describable {
	public static final String TYPE = "httpUploadNodeStep";
	static final Map<String, String> CONFIG_MAPPING;
	static final Map<String, String> CONFIG_MAPPING_FWK;
	static final List<Property> properties = new ArrayList();

	static {
		List<String> selectMethodsValues = Arrays.asList("POST", "PUT");

		properties
				.add(PropertyUtil
						.string("sourcePath",
								"Source Path\\File",
								"Choose the file, with complete path  (e.g.: c:\\myProjects\\RunDeck\\File1.txt)",
								true, ""));

		properties.add(PropertyUtil.string("destinationFileName",
				"Destination File Name", "Destination File Name", true, ""));

		properties.add(PropertyUtil.select("method", "Method",
				"Method to  call", true, "POST", selectMethodsValues));

		properties.add(PropertyUtil.string("url", "URL", "Choose the URL",
				true, ""));

		properties.add(PropertyUtil.string("user", "User",
				"Authenticated User", true, ""));

		properties.add(PropertyUtil.string("password", "Password", "Password",
				true, ""));

		Map<String, String> mapping = new HashMap();
		mapping.put("method", "plugin.httpUploadNodeStep.default.command");
		mapping.put("url", "plugin.httpUploadNodeStep.default.shell");
		// mapping.put("directory", "plugin.http-call.default.dir");
		CONFIG_MAPPING = Collections.unmodifiableMap(mapping);

		/*
		 * Map<String, String> mapping2 = new HashMap(); mapping2.put("command",
		 * "plugin.http-call.default.command"); mapping2.put("interpreter",
		 * "plugin.http-call.default.shell"); mapping2.put("directory",
		 * "plugin.http-call.default.dir");
		 */

		CONFIG_MAPPING_FWK = Collections.unmodifiableMap(mapping);
	}

	public static final Description DESC = new AbstractBaseDescription() {
		public String getName() {
			return "httpUploadNodeStep";
		}

		public String getTitle() {
			return "HTTP File Upload";
		}

		public String getDescription() {
			return "Make a HTTP File Upload";
		}

		public List<Property> getProperties() {
			return HttpUploadNodeStep.properties;
		}

		public Map<String, String> getPropertiesMapping() {
			return HttpUploadNodeStep.CONFIG_MAPPING;
		}

		public Map<String, String> getFwkPropertiesMapping() {
			return HttpUploadNodeStep.CONFIG_MAPPING_FWK;
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

			// context.getLogger().log(2, "hostname = " +
			// entry.extractHostname());
			// context.getLogger().log(2, "nodename = " + entry.getNodename());
			// context.getLogger().log(2, "toString = " + entry.toString());
			// context.getLogger().log(2,
			// "description = " + entry.getDescription());

			context.getLogger().log(2, "HttpUploadNodeStep.upload...");

			INodeSet nodeSet = context.getNodes();
			Collection<String> nodesNames = nodeSet.getNodeNames();
			for (String snodeName : nodesNames) {
				context.getLogger().log(2, "on node = " + snodeName); // +
																		// nodeSet.getNode(snodeName));
			}

			// !!
			// context.getLogger().log(
			// 2,
			// "httpUpload.configuration.toString() = "
			// + configuration.toString());

			String sourcePath = (String) configuration.get("sourcePath");
			String destinationFileName = (String) configuration
					.get("destinationFileName");
			String method = (String) configuration.get("method");
			String url = (String) configuration.get("url");
			String user = (String) configuration.get("user");
			String password = (String) configuration.get("password");

			context.getLogger().log(2, "sourcePath = " + sourcePath);
			context.getLogger().log(2,
					"destinationFileName = " + destinationFileName);
			context.getLogger().log(2, "method = " + method);
			context.getLogger().log(2, "url = " + url);
			context.getLogger().log(2, "user = " + user);
			// context.getLogger().log(2, "password = " + password);
			context.getLogger().log(2, "password = ???");

			// File file = new File(sourcePath);
			// HttpUploadNodeStep httpUploadNodeStep = new HttpUploadNodeStep();

			switch (method) {
			case "POST":
				send_post(url, sourcePath, destinationFileName, user, password);
				break;
			case "PUT":
				send_put(url, sourcePath, destinationFileName, user, password);
				break;
			default:
				System.out.println("httpUpload.invalid method");
			}

		} catch (Exception e) {
			// context.getLogger().log(0, "FALLITO: " + e.getMessage());
			throw new NodeStepException(e, Reason.CopyFileFailed,
					entry.getNodename());
		}
	}

	public void send_post(String url, String sourcePath, String destination,
			String user, String password) throws Exception {
		System.out.println("httpUpload.send_post.start");
		Uploader ul = new Uploader();
		ul.send(Uploader.Method.post, url, sourcePath, destination, user,
				password);
		System.out.println("httpUpload.send_post.stop");
	}

	public void send_put(String url, String sourcePath, String destination,
			String user, String password) throws Exception {
		System.out.println("httpUpload.send_put.start");
		Uploader ul = new Uploader();
		ul.send(Uploader.Method.put, url, sourcePath, destination, user,
				password);
		System.out.println("httpUpload.send_put.stop");
	}

	public static void main(String[] args) throws Exception {
		String url = "http://localhost:18081/My_HttpResponses_Sender/doGetdoPostdoPutServlet/";
		String sourcePath = "D:\\RunDeck\\c.txt";

		System.out.println("HttpUploadNodeStep.start");

		System.out.println("HttpUploadNodeStep.sendPost.start");
		HttpUploadNodeStep httpUploadNodeStep = new HttpUploadNodeStep();
		httpUploadNodeStep.send_post(url, sourcePath, "gastone5.txt", null,
				null);
		httpUploadNodeStep.send_post(url, sourcePath, "gastone5.txt", "davide",
				"password");
		System.out.println("HttpUploadNodeStep.sendPost.stop");

		System.out.println("HttpUploadNodeStep.sendPut.start");
		httpUploadNodeStep.send_post(url, sourcePath, "gastone6.txt", null,
				null);
		httpUploadNodeStep.send_post(url, sourcePath, "gastone6.txt", "davide",
				"password");
		System.out.println("HttpUploadNodeStep.sendPut.stop");

		System.out.println("HttpUploadNodeStep.stop");
	}

	@Override
	public Description getDescription() {
		return DESC;
	}

}
