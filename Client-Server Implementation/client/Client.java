import java.net.*;
import java.io.*;
import java.util.*;

public class Client {
  //the client class sends the requests to the server and receieves the response data
  //initialises all the client's state variables
	private static Socket fileSocket = null;
	private static PrintWriter output = null;
	private static DataInputStream input = null;
  private Boolean success = null;

  public Client() {
    try {
      fileSocket = new Socket("localhost", 8001);
      output = new PrintWriter(fileSocket.getOutputStream(), true);
      input = new DataInputStream(fileSocket.getInputStream());
    } catch (UnknownHostException e) {
      System.out.println("Host could not be identified");
      System.exit(-1);
    } catch (IOException e) {
      System.err.println("IOException when retrieving streams from the socket");
      System.exit(-1);
    }
  }

	public void sendFile(String[] commands) {
    //sendFIle() will get the argument given by the client and display the requested results
    if (commands.length == 0) {
      System.err.println("Please give a command. Either list or get filename");
      System.exit(-1);
    }
    String command = commands[0];
    output.println(Integer.toString(commands.length));
    String argument = null;
    for (int i = 0; i < commands.length; i++) {
      output.println(commands[i]);
    }
    if (command.equals("get") && commands.length == 2) {
      argument = commands[1];
    } else if (command.equals("list") && commands.length > 1) {
      System.err.println("Please only enter list");
      System.exit(-1);
    } else if (command.equals("get") && commands.length < 2) {
      System.err.println("Please enter a filename");
      System.exit(-1);
    } else if (command.equals("get") && commands.length > 2) {
      System.err.println("Please only enter one filename");
      System.exit(-1);
    }

    try {
      success = input.readBoolean();
    } catch (IOException e) {
      System.err.println("Success code could not be recieved");
    }
    if (success == false) {
      System.err.println(command + " was not understood by the server. Please enter either list or get fname");
      System.exit(-1);
    }
    //if the entered command equals get
    if (command.equals("get") && commands.length == 2) {
      //recieves the size of the input that the server is about to send
      int size = 0;
      try{
        size = input.readInt(); 
      } catch (IOException p) {
        System.err.println(argument+" could not be found");
        System.exit(-1);
      } 
      System.out.println("size: "+size);
      //creates a new byte[] array of that size in which to write the incoming data
      byte[] data = new byte[size];
      try{
        //reads the data that the server has written to the inputstream
        input.read(data);
      } catch (IOException f) {
        System.err.println(argument+" could not be found");
        System.exit(-1);
      }
      //creates a new file with the requested name
      System.out.println(argument);
      File location = new File("./"+argument);
      if (location.exists() && !location.isDirectory()) {
        //checks if the file already exists in the client's directory, and that the filename entered is not a directory
        System.err.print("A file with this name already exists in your local directory");
        System.exit(-1);
      } else {
        //if the file does not exist then create it to be written to
        try{
          location.createNewFile();
        } catch (IOException j) {
          System.err.println(argument+" could not be created on the local system");
          System.exit(-1);
        }
      }
      try {
        //opens a FileOutputStream to the newly created file to write the recieved data to
        FileOutputStream to_file = new FileOutputStream(location);
        //writes the data and then closes the FileStream
        try{
          to_file.write(data);
          to_file.close();
        } catch (IOException z) {
          System.err.println("The data could not be written to the local file");
          System.exit(-1);
        }
      } catch (FileNotFoundException e) {
        //if there was an error creating the file and it cannot be found when opening the stream, throw an error
        System.err.println("The file could not be found when opening the FileOutputStream");
        System.exit(-1);
      }

    } else if(command.equals("list")) {
      //if the command entered by list
      byte[] file_num = new byte[1];
      try{
        input.read(file_num);
      } catch (IOException r) {
        System.err.println("Number of files was not recieved from server");
        System.exit(-1);
      }
      System.out.println("Number of files: " + file_num[0]);
      int to_read = 0;
      try{
        to_read = input.available();
      } catch (IOException l) {
        System.err.println("Input buffer was empty (no data sent from server");
        System.exit(-1);
      }
      byte[] data = new byte[to_read];
      try {
        input.read(data);
      } catch (IOException h) {
        System.err.println("The list of files was not recieved from the server.");
        System.exit(-1);
      }
      String as_string = new String(data);
      String[] listed = as_string.split(":");
      for (int i = 0; i <listed.length; i++){
        System.out.println(listed[i]);
      }
    } 
    try {
      output.close();
      input.close();
      fileSocket.close();
    } catch (IOException k) {
      System.err.println("There was an error closing a stream");
      System.exit(-1);
    }
  }

    public static void main(String[] args) {
      //creates a new client instance and runs sendFile() with the user inputted arguments
      Client client = new Client();
      client.sendFile(args);
    }

}

