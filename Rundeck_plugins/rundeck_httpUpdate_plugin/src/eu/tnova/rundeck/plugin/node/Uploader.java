package eu.tnova.rundeck.plugin.node;

import java.io.FileInputStream;

import javax.ws.rs.core.MediaType;
import javax.ws.rs.core.Response;

import org.apache.cxf.jaxrs.client.WebClient;
import org.apache.cxf.jaxrs.ext.multipart.Attachment;
import org.apache.cxf.jaxrs.ext.multipart.ContentDisposition;
import org.apache.cxf.jaxrs.ext.multipart.MultipartBody;

public class Uploader {

	// public void send_post(String url, String source, String destination) {
	// try (FileInputStream stream = new FileInputStream(source);) {
	// WebClient webClient = WebClient.create(url);
	// webClient.encoding("UTF-8");
	// webClient.type(MediaType.MULTIPART_FORM_DATA);
	// // webClient.type(MediaType.MULTIPART_FORM_DATA_TYPE);
	// ContentDisposition cd = new ContentDisposition(
	// "attachment;filename=" + destination);
	// Attachment att = new Attachment("root", stream, cd);
	// Response response = webClient.post(new MultipartBody(att));
	// System.out.println(response.readEntity(String.class));
	// } catch (Exception ex) {
	// ex.printStackTrace();
	// }
	// }
	//
	// public void send_put(String url, String source, String destination) {
	// try (FileInputStream stream = new FileInputStream(source);) {
	// WebClient webClient = WebClient.create(url);
	// webClient.encoding("UTF-8");
	// webClient.type(MediaType.MULTIPART_FORM_DATA);
	// // webClient.type(MediaType.MULTIPART_FORM_DATA_TYPE);
	// ContentDisposition cd = new ContentDisposition(
	// "attachment;filename=" + destination);
	// Attachment att = new Attachment("root", stream, cd);
	// Response response = webClient.put(new MultipartBody(att));
	// System.out.println(response.readEntity(String.class));
	// } catch (Exception ex) {
	// ex.printStackTrace();
	// }
	// }

	public void send(Method method, String url, String source,
			String destination, String user, String password) throws Exception {
		try (FileInputStream stream = new FileInputStream(source);) {

			WebClient webClient = null;
			if (user == null || password == null || "".equals(user)
					|| "".equals(password)) {
				webClient = WebClient.create(url); // without
													// authentication
			} else {
				webClient = WebClient.create(url, user, password, null);
			}
			webClient.encoding("UTF-8");
			webClient.type(MediaType.MULTIPART_FORM_DATA);
			ContentDisposition cd = new ContentDisposition(
					"attachment;filename=" + destination);
			Attachment att = new Attachment("root", stream, cd);

			System.out.println("Uploader.send");
			System.out.println(" - method = " + method.toString());
			System.out.println(" - url = " + url);
			System.out.println(" - source = " + source);
			System.out.println(" - destination = " + destination);
			System.out.println(" - user = " + user);
			System.out.println(" - password = " + password);

			Response response = null;
			if (method == Uploader.Method.post) {
				response = webClient.post(new MultipartBody(att));
			} else if (method == Uploader.Method.put) {
				response = webClient.put(new MultipartBody(att));
			}

			if (response != null) {
				System.out.println(" - response = " + response.toString());
			}
			// System.out.println(response.readEntity(String.class));
		} catch (Exception ex) {
			ex.printStackTrace();
			throw new Exception("Upload file failed!");
		}
	}

	public enum Method {
		post,
		put
	}

	// public void send1() {
	//
	// try (FileInputStream stream = new FileInputStream("D:\\RunDeck\\c.txt");)
	// {
	// WebClient webClient = WebClient
	// .create("http://localhost:18081/My_HttpResponses_Sender/doGetdoPostdoPutServlet/");
	// webClient.encoding("UTF-8");
	// webClient.type(MediaType.MULTIPART_FORM_DATA);
	// ContentDisposition cd = new ContentDisposition(
	// "attachment;filename=paperoga2.txt");
	// System.out.println("send 1");
	// Attachment att = new Attachment("root", stream, cd);
	// System.out.println("send 2");
	// Response response = webClient.post(new MultipartBody(att));
	// System.out.println("send 3");
	// System.out.println(response.readEntity(String.class));
	// System.out.println("send 4");
	//
	// } catch (Exception ex) {
	// ex.printStackTrace();
	// }
	// }

	public static void main(String[] args) throws Exception {
		Uploader ul = new Uploader();

		/*
		 * ul.send(Method.post,
		 * "http://localhost:18081/My_HttpResponses_Sender/doGetdoPostdoPutServlet/"
		 * , "D:\\RunDeck\\c1.txt", "paperoga39.1.txt", "davide", "password");
		 * ul.send(Method.post,
		 * "http://localhost:18081/My_HttpResponses_Sender/doGetdoPostdoPutServlet/"
		 * , "D:\\RunDeck\\c1.txt", "paperoga39.2.txt", null, null);
		 * ul.send(Method.put,
		 * "http://localhost:18081/My_HttpResponses_Sender/doGetdoPostdoPutServlet/"
		 * , "D:\\RunDeck\\c1.txt", "paperoga39.3.txt", "davide", "password");
		 * ul.send(Method.put,
		 * "http://localhost:18081/My_HttpResponses_Sender/doGetdoPostdoPutServlet/"
		 * , "D:\\RunDeck\\c1.txt", "paperoga39.4.txt", null, null);
		 */
		ul.send(Method.post,
				"http://localhost:18081/My_HttpResponses_Sender/doGetdoPostdoPutServlet/",
				"D:\\RunDeck\\c1.txt", "paperoga39.1.txt", "davide", "123");

	}
}