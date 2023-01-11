import java.net.*;
import java.io.*;
import java.util.concurrent.*;


public class Server {
	//Server class which a client will connect to in order to be placed on a separate thread and handled by the client handler
	public static void main( String[] args ) {
		//creates state variables for the server class to be assigned later
		ServerSocket server = null;
		ExecutorService service = null;

		try {
			//creates a socket listening on port 8001 for the client to connect to
			server = new ServerSocket(8001);
		} catch (IOException e) {
			System.err.println("Could not listen on port: 8001.");
		}

		service = Executors.newFixedThreadPool(15);
		
		while(true) {
			try {
				//accepts the clients connection
				Socket client = server.accept();
				//passes the handling of the client to a new instance of the client handler class
				service.submit((new ClientHandler(client)));
			} catch (IOException e) {
				System.err.println("An IOException has occurred when accepting the client's connection");
			} catch (NullPointerException q ) {
				System.err.println("The Server has attempted to submit a null task");
			} catch (RejectedExecutionException z) {
				System.err.println("The submitted task could not be scheduled");
			}
		}
	}
}