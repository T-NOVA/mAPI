package eu.tnova.rundeck.plugin.node;

import java.io.IOException;
import java.io.InputStream;

//import org.apache.commons.httpclient.HttpVersion;
//import org.apache.http.impl.client.DefaultHttpClient;
//import org.apache.http.client.HttpClient;
//import org.apache.http.client.methods.HttpPost;
//import org.apache.http.params.CoreProtocolPNames;

import com.google.api.client.http.GenericUrl;
import com.google.api.client.http.HttpContent;
import com.google.api.client.http.HttpRequest;
import com.google.api.client.http.HttpRequestFactory;
import com.google.api.client.http.HttpResponse;
import com.google.api.client.http.javanet.NetHttpTransport;

public class HttpRequests {
	//
	// public void sendPostRequest(String url, String user, String password)
	// throws Exception {
	// GenericUrl genUrl = new GenericUrl(url);
	// NetHttpTransport transport = new NetHttpTransport();
	// try {
	// HttpRequestFactory httpRequestFactory = transport
	// .createRequestFactory();
	// HttpContent content = null;
	// HttpRequest request = httpRequestFactory.buildPostRequest(genUrl,
	// content);
	// request.getHeaders().setBasicAuthentication(user, password);
	//
	// // Attende la risposta fino ad un max di 100 sec.
	// request.setReadTimeout(100000);
	//
	// // --request.setClientAuthentication(authentication);
	// request.setRequestMethod("POST");
	// request.getHeaders().setAccept("application/json");
	//
	// System.out.println("HttpRequest url: " + request.getUrl());
	// System.out.println("HttpRequest header: "
	// + request.getHeaders().toString());
	// HttpResponse response = request.execute();
	// int statusCode = response.getStatusCode();
	// InputStream resp_content = response.getContent();
	// String sResponse = org.apache.commons.io.IOUtils.toString(
	// resp_content, "UTF-8");
	//
	// System.out.println("response status code: " + statusCode);
	// System.out.println("HttpResponse body: " + sResponse);
	// } catch (IOException e) {
	// // e.printStackTrace();
	// throw new Exception("http command failed!");
	// }
	// }
	//
	// public void sendPutRequest(String url, String user, String password)
	// throws Exception {
	// GenericUrl genUrl = new GenericUrl(url);
	// NetHttpTransport transport = new NetHttpTransport();
	// try {
	// HttpContent content = null; // todo add json?
	// HttpRequest request = transport.createRequestFactory()
	// .buildPutRequest(genUrl, content);
	// request.getHeaders().setBasicAuthentication(user, password);
	//
	// // Attende la risposta fino ad un max di 100 sec.
	// request.setReadTimeout(100000);
	// request.setRequestMethod("PUT");
	// request.getHeaders().setAccept("application/json");
	//
	// /*
	// * if (jsonBody != null && !jsonBody.isEmpty()) {
	// * request.setContent(new InputStreamContent("application/json",
	// * IOUtils.toInputStream(jsonBody, "UTF-8"))); }
	// */
	//
	// System.out.println("HttpRequest url: " + request.getUrl());
	// System.out.println("HttpRequest header: "
	// + request.getHeaders().toString());
	// HttpResponse response = request.execute();
	// int statusCode = response.getStatusCode();
	// InputStream resp_content = response.getContent();
	// String sResponse = org.apache.commons.io.IOUtils.toString(
	// resp_content, "UTF-8");
	//
	// System.out.println("response status code: " + statusCode);
	// System.out.println("HttpResponse body: " + sResponse);
	// // todo
	// } catch (IOException e) {
	// // e.printStackTrace();
	// throw new Exception("http command failed!");
	// }
	// }
	//
	// public void sendDeleteRequest(String url, String user, String password)
	// throws Exception {
	// GenericUrl genUrl = new GenericUrl(url);
	// NetHttpTransport transport = new NetHttpTransport();
	// try {
	// HttpRequest request = transport.createRequestFactory()
	// .buildDeleteRequest(genUrl);
	// request.getHeaders().setBasicAuthentication(user, password);
	//
	// // Attende la risposta fino ad un max di 100 sec.
	// request.setReadTimeout(100000);
	// request.setRequestMethod("DELETE");
	// request.getHeaders().setAccept("application/json");
	//
	// System.out.println("HttpRequest url: " + request.getUrl());
	// System.out.println("HttpRequest header: "
	// + request.getHeaders().toString());
	// HttpResponse response = request.execute();
	// int statusCode = response.getStatusCode();
	// InputStream resp_content = response.getContent();
	// String sResponse = org.apache.commons.io.IOUtils.toString(
	// resp_content, "UTF-8");
	//
	// System.out.println("response status code: " + statusCode);
	// System.out.println("HttpResponse body: " + sResponse);
	// // todo
	// } catch (IOException e) {
	// // e.printStackTrace();
	// throw new Exception("http command failed!");
	// }
	// }

	public void send(Method method, String url, String user, String password)
			throws Exception {
		HttpContent content = null;
		GenericUrl genUrl = new GenericUrl(url);
		NetHttpTransport transport = new NetHttpTransport();
		try {
			HttpRequest request = null;
			if (method == Method.post) {
				request = transport.createRequestFactory().buildPostRequest(
						genUrl, content);
				request.setRequestMethod("POST");
			} else if (method == Method.put) {
				request = transport.createRequestFactory().buildPutRequest(
						genUrl, content);
				request.setRequestMethod("PUT");
			} else if (method == Method.delete) {
				request = transport.createRequestFactory().buildDeleteRequest(
						genUrl);
				request.setRequestMethod("DELETE");
			} else {
				System.out.println("Error: invalid http method!");
			}

			if (request != null) {
				if (user != null && password != null && !("".equals(user))
						&& !("".equals(password))) {
					request.getHeaders().setBasicAuthentication(user, password);
				}

				// Wait max 100 sec.
				request.setReadTimeout(100000);

				request.getHeaders().setAccept("application/json");

				System.out.println("HttpRequest url: " + request.getUrl());
				System.out.println("HttpRequest header: "
						+ request.getHeaders().toString());
				HttpResponse response = request.execute();
				int statusCode = response.getStatusCode();
				InputStream resp_content = response.getContent();
				String sResponse = org.apache.commons.io.IOUtils.toString(
						resp_content, "UTF-8");

				System.out.println("response status code: " + statusCode);
				System.out.println("HttpResponse body: " + sResponse);
			}
		} catch (IOException e) {
			// e.printStackTrace();
			throw new Exception("http command failed!");
		}
	}

	public enum Method {
		post,
		put,
		delete
	}

	public static void main(String[] args) throws Exception {
		System.out.println("HttpCommands.start");

		String urlPost = "http://localhost:8080/examples/servlets/servlet/doGetdoPostdoPutServlet";
		String urlPut = "http://localhost:8080/examples/servlets/servlet/doGetdoPostdoPutServlet";
		String urlDelete = "http://localhost:8080/examples/servlets/servlet/doGetdoPostdoPutServlet";

		String user = "davide";
		String password = "password";

		HttpRequests httpRequests = new HttpRequests();
		System.out.println("HttpCommands.sendPost");
		// httpRequests.sendPostRequest(urlPost, user, password);
		httpRequests.send(Method.post, urlPost, user, password);
		System.out.println("--------------------------------------");
		System.out.println("HttpCommands.sendPut");
		// httpRequests.sendPutRequest(urlPut, user, password);
		httpRequests.send(Method.put, urlPut, user, password);
		System.out.println("--------------------------------------");
		System.out.println("HttpCommands.sendDelete");
		// httpRequests.sendDeleteRequest(urlDelete, user, password);
		httpRequests.send(Method.delete, urlDelete, user, password);
	}
}
